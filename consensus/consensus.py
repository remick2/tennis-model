"""Polymarket copy-consensus paper tracker. PAPER TRACKING ONLY: nothing is ever bet.

Each run:
  1. pulls open positions for 15 profitable Polymarket sports traders (data-api),
  2. logs games where 2+ of them hold $1k+ on the same side -> consensus/signals.csv,
  3. grades finished entries from Polymarket's market prices (gamma-api),
  4. rewrites consensus/summary.md,
  5. prints a markdown alert for NEW pre-game "Paper play" signals (3+ agree, 0 against).
     The workflow turns non-empty output into a GitHub issue (phone notification).

Tiers (judged across all 15): Paper play = 3+ agree and nobody against; Track only = exactly 2
agree and nobody against; Split = 2+ agree but 1+ of the 15 is on the other side.
Each row also stores the agreeing/opposing names, so the core-10-only version can be graded too.
Results are 1 unit flat at the price when the signal was logged (not the traders' entries).
"""
import csv
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "signals.csv"
SUMMARY = ROOT / "summary.md"
FINAL_SENT = ROOT / ".final_sent"

DATA = "https://data-api.polymarket.com"
GAMMA = "https://gamma-api.polymarket.com"
UA = {"User-Agent": "consensus-paper-tracker/1.0"}

END_DATE = "2026-11-10"   # last day of the tracking week (Mountain Time)
MIN_STAKE = 1000          # a trader counts on a side only with $1k+ in it
MT = timezone(timedelta(hours=-7))  # MST; Colorado is on standard time all of this week

# name -> proxy wallet. The first 10 are the "core 10".
TRADERS = {
    "monkeymashingkeyboard": "0x684baa57c338c2549aec0aa3f034f695d72a8409",
    "googleplay": "0xe9b710551dd82a44e79203c2394a2b10163ace7b",
    "jakepaulthegoat2008": "0x6ac5bb06a9eb05641fd5e82640268b92f3ab4b6e",
    "0xb4F978BE": "0xb4f978be63cdf75554b0b46a4262a6db597cc9a7",
    "chongchong37": "0x2879ded7fe05df00eddbb2fba412a0d30964411a",
    "yabanci": "0x285faa3e3d1465cf3ff1bff1e1d14891f5b8495f",
    "drainedandpoor": "0x5e6e2c3f06686f2607b86c90e35f536e81a1be00",
    "ethanaz": "0xf28e42d20e4826f2b10a24bc952001697947cab2",
    "0x9f15613e": "0x9f15613ebf1f36d4bc679e1211d1fc567cf9bdb3",
    "ic4cream": "0x27f738fe203827445690339104aae35b20bc44b0",
    "Multicoloured-Serf": "0x958bdb8aa30b8e5bd1fe4ee071f309c84e97f826",
    "ch27er": "0x61a3f1ef9c9618f532eb49f0cb260486c168e508",
    "darkumbreon88": "0x0235dc24b38772bf3339a9e5ec5db3d3a05fcee5",
    "scootergene": "0xf3a6ac44c5c90ff2b4afa4459f71acc2e57971bd",
    "0xd4aa6f8e": "0x709e8dcb133555794decc598e07f2c923b8366f5",
}
CORE10 = list(TRADERS)[:10]

FIELDS = ["id", "logged_at", "game_date", "league", "game", "event_slug", "side", "market",
          "agree", "against", "agree_n", "against_n", "core10_n", "their_entry", "price_at_log",
          "tier", "status", "units", "condition_id", "outcome_index", "note"]

LEAGUES = {"nba": "NBA", "nfl": "NFL", "nhl": "NHL", "mlb": "MLB", "cfb": "CFB", "cbb": "CBB",
           "wnba": "WNBA", "lol": "LoL", "cs2": "CS2", "val": "Valorant", "dota2": "Dota 2",
           "atp": "ATP", "wta": "WTA", "itf": "ITF", "ufc": "UFC", "epl": "EPL", "ucl": "UCL",
           "uel": "UEL", "sea": "Serie A", "lal": "La Liga", "bun": "Bundesliga", "fl1": "Ligue 1",
           "mls": "MLS", "elc": "Championship", "efl": "EFL"}


def get(url, **params):
    r = requests.get(url, params=params, headers=UA, timeout=30)
    r.raise_for_status()
    return r.json()


def positions(wallet):
    out, cursor = [], None
    for _ in range(6):
        p = {"user": wallet, "limit": 500}
        if cursor:
            p["cursor"] = cursor
        j = get(f"{DATA}/v2/positions", **p)
        out += j.get("data") or []
        cursor = (j.get("pagination") or {}).get("next_cursor")
        if not cursor or not j.get("data"):
            break
    return out


def side_group(p):
    if p["outcome"] in ("Over", "Under"):
        return "tot"
    if p["outcome"] in ("Yes", "No"):
        return "yn:" + p["title"]
    return "team"


def market_label(title, outcome):
    t = title.lower()
    if outcome in ("Over", "Under"):
        return "Total"
    if "map handicap" in t or "game handicap" in t:
        return "Map handicap"
    if "spread" in t:
        return "Spread"
    if re.search(r"game \d winner|map \d winner", t):
        return "Single game"
    return "Moneyline"


def scan(now):
    since = (now - timedelta(hours=31)).astimezone(MT).strftime("%Y-%m-%d")
    games = {}
    failed = []
    for name, wallet in TRADERS.items():
        try:
            ps = positions(wallet)
        except Exception as e:  # one trader failing shouldn't kill the run
            failed.append(f"{name} ({type(e).__name__})")
            continue
        for p in ps:
            slug = p.get("event_slug") or ""
            if not (p.get("status") == "OPEN" and not p.get("redeemable")
                    and 0.03 < float(p.get("current_price") or 0) < 0.97
                    and re.search(r"\d{4}-\d{2}-\d{2}$", slug) and slug[-10:] >= since
                    and float(p.get("total_cost_usdc") or 0) >= MIN_STAKE):
                continue
            g = games.setdefault((slug, side_group(p)), {})
            s = g.setdefault(p["outcome"], {"who": set(), "cost": 0.0, "size": 0.0, "best": None})
            s["who"].add(name)
            s["cost"] += float(p["total_cost_usdc"])
            s["size"] += float(p.get("current_size") or 0)
            if s["best"] is None or p["total_cost_usdc"] > s["best"]["total_cost_usdc"]:
                s["best"] = p
    found = []
    for (slug, _), sides in games.items():
        for outcome, s in sides.items():
            if len(s["who"]) < 2:
                continue
            against = sorted({n for o, s2 in sides.items() if o != outcome for n in s2["who"]})
            agree = sorted(s["who"], key=list(TRADERS).index)
            b = s["best"]
            found.append({
                "event_slug": slug, "title": b["title"], "side": outcome, "agree": agree, "against": against,
                "condition_id": b["condition_id"], "outcome_index": int(b["outcome_index"]),
                "price": round(float(b["current_price"]), 4),
                "entry": round(s["cost"] / s["size"], 3) if s["size"] else None,
            })
    return found, failed


def tier(agree_n, against_n):
    if against_n:
        return "Split"
    return "Paper play" if agree_n >= 3 else "Track only"


_events = {}


def event_info(slug):
    if slug not in _events:
        try:
            e = get(f"{GAMMA}/events", slug=slug)
            _events[slug] = e[0] if e else {}
        except Exception:
            _events[slug] = {}
    return _events[slug]


def start_time(slug):
    st = event_info(slug).get("startTime")
    try:
        return datetime.fromisoformat(st.replace("Z", "+00:00")) if st else None
    except ValueError:
        return None


def load():
    if not LOG.exists():
        return []
    with LOG.open() as f:
        return list(csv.DictReader(f))


def save(rows):
    with LOG.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def merge(rows, found, now):
    new_plays = []
    for s in found:
        agree_n, against_n = len(s["agree"]), len(s["against"])
        t = tier(agree_n, against_n)
        st = start_time(s["event_slug"])
        started = st is not None and st <= now
        game = event_info(s["event_slug"]).get("title") or s["title"].split(":")[0]
        game = re.sub(r"\s*-\s*(Game|Map) \d+ Winner$", "", game)
        existing = next((r for r in rows if (r["condition_id"] == s["condition_id"]
                                             and str(r["outcome_index"]) == str(s["outcome_index"]))
                         or (r.get("event_slug") == s["event_slug"] and r["side"] == s["side"])), None)
        if existing:
            if (t == "Paper play" and existing["tier"] != "Paper play" and existing["status"] == "open"
                    and not started):
                existing.update(tier=t, agree="; ".join(s["agree"]), against="; ".join(s["against"]),
                                agree_n=agree_n, against_n=against_n,
                                core10_n=sum(n in CORE10 for n in s["agree"]),
                                price_at_log=s["price"],
                                note=(existing["note"] + "; " if existing["note"] else "")
                                + f"upgraded to paper play at {s['price'] * 100:.1f}c on {now:%Y-%m-%d}")
                new_plays.append((existing, st))
            continue
        day = (st or now).astimezone(MT).strftime("%Y-%m-%d")
        prefix = s["event_slug"].split("-")[0]
        row = {
            "id": f"{day.replace('-', '')}-{s['event_slug']}-{re.sub(r'[^a-z0-9]+', '-', s['side'].lower()).strip('-')}",
            "logged_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "game_date": day,
            "league": LEAGUES.get(prefix, prefix.upper()), "game": game, "event_slug": s["event_slug"],
            "side": s["side"], "market": market_label(s["title"], s["side"]),
            "agree": "; ".join(s["agree"]), "against": "; ".join(s["against"]),
            "agree_n": agree_n, "against_n": against_n, "core10_n": sum(n in CORE10 for n in s["agree"]),
            "their_entry": s["entry"], "price_at_log": s["price"], "tier": t, "status": "open", "units": "",
            "condition_id": s["condition_id"], "outcome_index": s["outcome_index"],
            "note": "in progress when logged" if started else "",
        }
        rows.append(row)
        if t == "Paper play" and not started:
            new_plays.append((row, st))
    return new_plays


def grade(rows):
    graded = 0
    for r in rows:
        if r["status"] != "open":
            continue
        m = None
        for closed in ("true", "false"):
            try:
                j = get(f"{GAMMA}/markets", condition_ids=r["condition_id"], closed=closed)
            except Exception:
                j = []
            if j:
                m = j[0]
                break
        if not m:
            continue
        try:
            p = float(json.loads(m.get("outcomePrices") or "[]")[int(r["outcome_index"])])
        except (ValueError, IndexError, TypeError):
            continue
        price = float(r["price_at_log"])
        if p >= 0.98:
            r["status"], r["units"] = "W", round((1 - price) / price, 2)
            graded += 1
        elif p <= 0.02:
            r["status"], r["units"] = "L", -1.0
            graded += 1
    return graded


def record(rows):
    w = sum(r["status"] == "W" for r in rows)
    l = sum(r["status"] == "L" for r in rows)
    u = sum(float(r["units"]) for r in rows if r["units"] not in ("", None))
    o = sum(r["status"] == "open" for r in rows)
    return f"{w}-{l}", f"{u:+.2f}", o


def core10_tier(r):
    agree = [n for n in r["agree"].split("; ") if n in CORE10]
    against = [n for n in (r["against"] or "").split("; ") if n in CORE10]
    if len(agree) < 2:
        return None
    return tier(len(agree), len(against))


def write_summary(rows, now):
    lines = [f"# Consensus paper tracker — {now.astimezone(MT):%a %b %-d, %-I:%M%p} MT", "",
             "Paper tracking only. 1 unit flat at the price when each signal was logged.", "",
             "| Rule | Group | Record | Units | Open |", "|---|---|---|---|---|"]
    for t in ("Paper play", "Track only", "Split"):
        rec, u, o = record([r for r in rows if r["tier"] == t])
        lines.append(f"| {t} | all 15 | {rec} | {u} | {o} |")
    for t in ("Paper play", "Track only", "Split"):
        rec, u, o = record([r for r in rows if core10_tier(r) == t])
        lines.append(f"| {t} | core 10 only | {rec} | {u} | {o} |")
    lines += ["", "Paper play = 3+ agree, nobody against. Track only = exactly 2 agree, nobody against. "
              "Split = 2+ agree but someone in the group is on the other side.", "",
              "## Open signals", "", "| Date | League | Game | Side | Rule | Agree | Against | Logged at |",
              "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r["status"] == "open":
            lines.append(f"| {r['game_date']} | {r['league']} | {r['game']} | {r['side']} ({r['market']}) | "
                         f"{r['tier']} | {r['agree']} | {r['against'] or '—'} | {float(r['price_at_log']) * 100:.1f}c |")
    SUMMARY.write_text("\n".join(lines) + "\n")


def alert(new_plays):
    out = []
    for r, st in new_plays:
        when = st.astimezone(MT).strftime("%a %-I:%M%p MT") if st else "start time unknown"
        out.append(f"**PAPER PLAY: {r['side']} {r['market']} ({r['game']}) @ {float(r['price_at_log']) * 100:.1f}c "
                   f"· 1u paper · starts {when}**")
        out.append(f"Agree ({r['agree_n']}): {r['agree']}")
        out.append("")
    return "\n".join(out)


def main():
    now = datetime.now(timezone.utc)
    rows = load()
    today = now.astimezone(MT).strftime("%Y-%m-%d")
    new_plays, failed = [], []
    if today <= END_DATE:
        found, failed = scan(now)
        new_plays = merge(rows, found, now)
    graded = grade(rows)
    save(rows)
    write_summary(rows, now)
    print(f"logged {len(rows)} total, graded {graded} this run, failed traders: {', '.join(failed) or 'none'}",
          file=sys.stderr)
    if len(failed) > 5:
        raise SystemExit(f"{len(failed)} of {len(TRADERS)} trader pulls failed: {', '.join(failed)}")
    if new_plays:
        print(alert(new_plays))
    elif today > END_DATE and not FINAL_SENT.exists():
        FINAL_SENT.write_text(now.isoformat())
        print("**Tracking week is over.** Final record:\n")
        print(SUMMARY.read_text().split("## Open signals")[0])
        print("You can disable the `consensus` workflow in the Actions tab.")


if __name__ == "__main__":
    main()
