"""Polymarket copy-consensus paper tracker. PAPER TRACKING ONLY: nothing is ever bet.

Each run:
  1. pulls open positions for 15 profitable Polymarket sports traders (data-api),
  2. logs games where 2+ of them hold $1k+ on the same side -> consensus/signals.csv,
  3. grades finished entries from Polymarket's market prices (gamma-api),
  4. rewrites consensus/summary.md,
  5. writes alert files into the folder given as argv[1] (consensus/cycle.sh turns each one into a
     GitHub issue -> phone notification; line 1 of each file is the issue title):
       play.md   NEW pre-game "Paper play" signals (3+ agree, 0 against)
       report-*  official reports: old-roster final (Mon Nov 10), then new-roster reports every Friday
                 from Nov 13
       health.md daily roster health check: warns when a trader starts looking like Multicoloured-Serf
                 (too many bets, in too many agreements) or ethanaz (betting both sides), or stops betting
No end date: it keeps running until the workflow is disabled.

Tiers (judged across all 15): Paper play = 3+ agree and nobody against; Track only = exactly 2
agree and nobody against; Split = 2+ agree but 1+ of the 15 is on the other side.
Each row also stores the agreeing/opposing names, so the core-10-only version can be graded too.
Results are 1 unit flat at the price when the signal was logged (not the traders' entries).
"""
import csv
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "signals.csv"
SUMMARY = ROOT / "summary.md"
REPORTS_SENT = ROOT / "reports_sent.txt"   # ids of official reports already opened as issues
HEALTH = ROOT / "health.json"               # last daily roster health check + which warnings were sent

DATA = "https://data-api.polymarket.com"
GAMMA = "https://gamma-api.polymarket.com"
UA = {"User-Agent": "consensus-paper-tracker/1.0"}

START_DATE = "2026-11-03"   # tracking started
MIN_STAKE = 1000            # a trader counts on a side only with $1k+ in it

# Roster 2 (Serf, googleplay, ethanaz, 0xd4aa6f8e, scootergene out) went live with the 6:40pm MT check
# on Nov 7; its swap commit landed 00:54Z Nov 8. Rows logged before this are "old roster".
ROSTER2_START = "2026-11-08T01:00:00Z"
OLD_CORE10 = ["monkeymashingkeyboard", "googleplay", "jakepaulthegoat2008", "0xb4F978BE", "chongchong37",
              "yabanci", "drainedandpoor", "ethanaz", "0x9f15613e", "ic4cream"]
OLD_REPORT_DATE = date(2026, 11, 10)   # old roster's final report (Mon)
NEW_REPORT_FIRST = date(2026, 11, 13)  # new roster's first report; then every Friday

# Roster health (7-day window). "warn" = symptoms starting to leak in; "alert" = the Serf/ethanaz level.
HEALTH_DAYS = 7
HEALTH_RULES = [  # (key, label, kind, warn, alert)
    ("per_day", "directional bets/day too high (Serf-style)", "high", 17, 20),
    ("share", "share of all agreements (Serf-style)", "high", 0.33, 0.40),
    ("both_pct", "% of markets bet on both sides (ethanaz-style)", "high", 10, 15),
    ("per_day", "directional bets/day too low (below 5)", "low", 5, 3),
]
MIN_AGREEMENTS_FOR_SHARE = 10
MT = ZoneInfo("America/Denver")

# name -> proxy wallet. The first 10 are the "core 10".
TRADERS = {
    "monkeymashingkeyboard": "0x684baa57c338c2549aec0aa3f034f695d72a8409",
    "purplegatto": "0x032eb1bc893940263ad0b01889f262fc232f2a9e",  # Nov 7, replaced googleplay (2.4/day)
    "jakepaulthegoat2008": "0x6ac5bb06a9eb05641fd5e82640268b92f3ab4b6e",
    "0xb4F978BE": "0xb4f978be63cdf75554b0b46a4262a6db597cc9a7",
    "chongchong37": "0x2879ded7fe05df00eddbb2fba412a0d30964411a",
    "yabanci": "0x285faa3e3d1465cf3ff1bff1e1d14891f5b8495f",
    "drainedandpoor": "0x5e6e2c3f06686f2607b86c90e35f536e81a1be00",
    "999585": "0x88a6c8e00c4752a8c70d24025fa781fa046a7e77",  # Nov 7, replaced ethanaz (both sides of 29% of markets)
    "0x9f15613e": "0x9f15613ebf1f36d4bc679e1211d1fc567cf9bdb3",
    "ic4cream": "0x27f738fe203827445690339104aae35b20bc44b0",
    # Nov 7: replaced Multicoloured-Serf (~22 directional mkts/day, both sides of 20% of markets; he was in
    # over half of all agreements) with BreakTheBank (#1 monthly sports PnL, ~6/day, never both sides)
    "BreakTheBank": "0xf0318c32136c2db7fec88b84869aee6a1106c80c",
    "ch27er": "0x61a3f1ef9c9618f532eb49f0cb260486c168e508",
    # Nov 8: replaced darkumbreon88 (in 50% of new-roster agreements, mostly in-play EPL with ch27er)
    "ianf2026": "0x81d972dbea298a5064d4ba51031e0386182fe9c9",
    "JoeyAroyyOO": "0xc3744a19f42266ce6fa2736f52eae6e178b20f3e",  # Nov 7, replaced scootergene (0.4/day)
    "Kyn008": "0xd29312e2446a746bbd94408e1c475f1ec6d7d683",  # Nov 7, replaced 0xd4aa6f8e (2.1/day)
}
CORE10 = list(TRADERS)[:10]

# Bench: pre-screened swaps (Nov 7 consensus-screen, 7-day window), named in roster warnings for that trader.
BENCH = {
    "0x9f15613e": ("AppleTiiime", "0x951634357346bb291df117f9ac410100feea2104",
                   "#99 sports PnL, NBA, 7.7 bets/day, active 7/7 days, never both sides; "
                   "no second backup left; run consensus-screen"),
}

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


def get_retry(url, **params):
    for i in range(4):
        try:
            return get(url, **params)
        except Exception:
            if i == 3:
                raise
            import time
            time.sleep(2 * (i + 1))


def buys(wallet, since_ts):
    """BUY trades on dated (sports) events since since_ts (unix seconds)."""
    out, cursor = [], None
    for _ in range(10):
        p = {"user": wallet, "limit": 500}
        if cursor:
            p["cursor"] = cursor
        j = get_retry(f"{DATA}/v2/activity", **p)
        d = j.get("data") or []
        out += d
        cursor = (j.get("pagination") or {}).get("next_cursor")
        if not cursor or not d or d[-1]["timestamp"] < since_ts:
            break
    return [a for a in out if a["timestamp"] >= since_ts and a.get("type") == "TRADE" and a.get("side") == "BUY"
            and re.search(r"\d{4}-\d{2}-\d{2}$", a.get("event_slug") or "")]


def trader_stats(wallet, since_ts, days):
    """Directional markets/day ($1k+, 75%+ on one side), active days, % of markets bet both sides, top sports."""
    mk, leagues, active = {}, {}, set()
    for a in buys(wallet, since_ts):
        m = mk.setdefault(a["condition_id"], {})
        m[a["outcome_index"]] = m.get(a["outcome_index"], 0.0) + float(a["usdc_size"])
        lg = a["event_slug"].split("-")[0]
        leagues[lg] = leagues.get(lg, 0.0) + float(a["usdc_size"])
        active.add(datetime.fromtimestamp(a["timestamp"], MT).date())
    both = sum(len(m) > 1 for m in mk.values())
    directional = [m for m in mk.values() if sum(m.values()) >= MIN_STAKE and max(m.values()) >= 0.75 * sum(m.values())]
    return {"per_day": round(len(directional) / days, 1), "days": len(active), "markets": len(mk),
            "both_pct": round(100 * both / len(mk)) if mk else 0,
            "stake": round(sum(sum(m.values()) for m in directional) / len(directional)) if directional else 0,
            "leagues": ",".join(k for k, _ in sorted(leagues.items(), key=lambda x: -x[1])[:3])}


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


def side_label(title, outcome):
    """Readable side incl. the line: 'Jaguars (-9.5)', 'Over 52.5', 'Real Madrid win: No'."""
    period = re.match(r"(?:.*?\b)?(1H|2H|1Q|2Q|3Q|4Q)\b", title)
    pre = f"{period.group(1)} " if period else ""
    sp = re.search(r"Spread: (.+?) \(([-+]?\d+(?:\.\d+)?)\)", title)
    if sp:
        team, line = sp.group(1), float(sp.group(2))
        line = line if outcome == team else -line
        return f"{pre}{outcome} ({line:+g})"
    tot = re.search(r"O/U (\d+(?:\.\d+)?)", title)
    if outcome in ("Over", "Under") and tot:
        who = re.match(r"(.+?) Team Total", title)
        return f"{pre}{who.group(1) + ' ' if who else ''}{outcome} {tot.group(1)}"
    if outcome not in ("Yes", "No"):
        return f"{pre}{outcome}"
    m = re.match(r"Will (.+?) win\b", title)
    if m:
        return f"{m.group(1)} win: {outcome}"
    if re.search(r"\bdraw\b", title, re.I):
        return f"Draw: {outcome}"
    return f"{title.rstrip('?')}: {outcome}"


def market_label(title, outcome):
    t = title.lower()
    if outcome.split(" ")[0] in ("Over", "Under") or re.search(r"\b(Over|Under) \d", outcome):
        return "Total"
    if "map handicap" in t or "game handicap" in t:
        return "Map handicap"
    if "spread" in t:
        return "Spread"
    if re.search(r"game \d winner|map \d winner", t):
        return "Single game"
    if t.startswith("will "):
        return "3-way"
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
            # one bucket per market (e.g. the moneyline, or the -3.5 spread), never across markets:
            # mixing them let a spread position's price leak into a moneyline alert
            g = games.setdefault((slug, p["condition_id"]), {})
            s = g.setdefault(p["outcome"], {"who": {}, "size": {}, "best": None})
            s["who"][name] = s["who"].get(name, 0.0) + float(p["total_cost_usdc"])
            s["size"][name] = s["size"].get(name, 0.0) + float(p.get("current_size") or 0)
            if s["best"] is None or p["total_cost_usdc"] > s["best"]["total_cost_usdc"]:
                s["best"] = p
    # A trader counts only on the side holding 75%+ of their money on that game; hedgers count nowhere.
    for sides in games.values():
        for name in {n for s in sides.values() for n in s["who"]}:
            stakes = {o: s["who"].get(name, 0.0) for o, s in sides.items()}
            top = max(stakes, key=stakes.get)
            for o, s in sides.items():
                if name in s["who"] and (o != top or stakes[top] < 0.75 * sum(stakes.values())):
                    s["who"].pop(name)
                    s["size"].pop(name, None)
    for sides in games.values():
        for s in sides.values():
            s["cost"], s["shares"] = sum(s["who"].values()), sum(s["size"].values())
    found = []
    for (slug, _), sides in games.items():
        for outcome, s in sides.items():
            if len(s["who"]) < 2:
                continue
            against = sorted({n for o, s2 in sides.items() if o != outcome for n in s2["who"]})
            agree = sorted(s["who"], key=list(TRADERS).index)
            b = s["best"]
            found.append({
                "event_slug": slug, "title": b["title"], "side": side_label(b["title"], outcome),
                "agree": agree, "against": against,
                "condition_id": b["condition_id"], "outcome_index": int(b["outcome_index"]),
                "price": round(float(b["current_price"]), 4),
                "entry": round(s["cost"] / s["shares"], 3) if s["shares"] else None,
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
        # only new-roster rows count as "already logged"; old-roster rows keep grading on their own
        existing = next((r for r in rows if roster(r) == "new" and r["condition_id"] == s["condition_id"]
                         and str(r["outcome_index"]) == str(s["outcome_index"])), None)
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
        rid = f"{day.replace('-', '')}-{s['event_slug']}-{re.sub(r'[^a-z0-9]+', '-', s['side'].lower()).strip('-')}"
        if any(r["id"] == rid for r in rows):
            rid += "-r2"
        row = {
            "id": rid,
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


def roster(r):
    return "new" if r["logged_at"] >= ROSTER2_START else "old"


def core10_tier(r):
    core = CORE10 if roster(r) == "new" else OLD_CORE10
    agree = [n for n in r["agree"].split("; ") if n in core]
    against = [n for n in (r["against"] or "").split("; ") if n in core]
    if len(agree) < 2:
        return None
    return tier(len(agree), len(against))


def in_play(r):
    """True if the game had already started when the signal was first logged (not bettable pre-game)."""
    return "in progress when logged" in (r.get("note") or "")


def record_table(rows):
    """One row per rule and group, with pre-game (bettable) and in-play results side by side."""
    lines = ["| Rule | Group | Pre-game record | Pre-game units | In-play record | In-play units | Open |",
             "|---|---|---|---|---|---|---|"]
    for group, pick in (("all 15", lambda r, t: r["tier"] == t), ("core 10 only", lambda r, t: core10_tier(r) == t)):
        for t in ("Paper play", "Track only", "Split"):
            sel = [r for r in rows if pick(r, t)]
            pre_rec, pre_u, pre_o = record([r for r in sel if not in_play(r)])
            live_rec, live_u, live_o = record([r for r in sel if in_play(r)])
            lines.append(f"| {t} | {group} | {pre_rec} | {pre_u} | {live_rec} | {live_u} | {pre_o + live_o} |")
    return lines


RULES = ("Paper play = 3+ agree, nobody against. Track only = exactly 2 agree, nobody against. "
         "Split = 2+ agree but someone in the group is on the other side. "
         "Pre-game = logged before the game started (what you could actually bet off an alert); "
         "in-play = the agreement only showed up after the start, graded at the live price when logged.")


def health_table(stats):
    lines = ["| Trader | Bets/day | Active days | Both-sides % | Share of agreements | Avg stake | Top sports |",
             "|---|---|---|---|---|---|---|"]
    for n in TRADERS:
        t = stats.get(n)
        if not t:
            lines.append(f"| {n} | — | — | — | — | — | (pull failed) |")
            continue
        share = f"{t['share'] * 100:.0f}% of {t['agreements']}" if t.get("agreements") else "—"
        lines.append(f"| {n} | {t['per_day']} | {t['days']} | {t['both_pct']}% | {share} | ${t['stake']:,} | {t['leagues']} |")
    return lines


def write_summary(rows, now):
    new = [r for r in rows if roster(r) == "new"]
    old = [r for r in rows if roster(r) == "old"]
    lines = [f"# Consensus paper tracker — {now.astimezone(MT):%a %b %-d, %-I:%M%p} MT", "",
             "Paper tracking only. 1 unit flat at the price when each signal was logged.", "",
             "## New roster (since Nov 7, 6:40pm MT)", "",
             "In: BreakTheBank, purplegatto, 999585, Kyn008, JoeyAroyyOO. 'Core 10' = the first 10 slots. "
             "Official reports every Friday from Nov 13.", "", *record_table(new), "",
             "## Old roster (Nov 3 – Nov 7, closed)", "",
             "Included Multicoloured-Serf, googleplay, ethanaz, 0xd4aa6f8e and scootergene. Rows logged before "
             "the Nov 5 per-market fix are flagged 'old grouping'. Final report Mon Nov 10.", "",
             *record_table(old), "", RULES, ""]
    if HEALTH.exists():
        h = json.loads(HEALTH.read_text())
        lines += [f"## Roster health (last {HEALTH_DAYS} days, checked {h.get('date', '?')})", "",
                  *health_table(h.get("stats", {})), ""]
    lines += ["## Open signals", "", "| Roster | Date | League | Game | Side | Rule | Timing | Agree | Against | Logged at |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r["status"] == "open":
            lines.append(f"| {roster(r)} | {r['game_date']} | {r['league']} | {r['game']} | {r['side']} ({r['market']}) | "
                         f"{r['tier']} | {'in-play' if in_play(r) else 'pre-game'} | {r['agree']} | "
                         f"{r['against'] or '—'} | {float(r['price_at_log']) * 100:.1f}c |")
    SUMMARY.write_text("\n".join(lines) + "\n")


def alert(new_plays):
    out = [f"Consensus paper play: {datetime.now(MT):%a %b %-d %-I:%M%p} MT"]
    for r, st in new_plays:
        when = st.astimezone(MT).strftime("%a %-I:%M%p MT") if st else "start time unknown"
        out.append(f"**PAPER PLAY: {r['side']} {r['market']} ({r['game']}) @ {float(r['price_at_log']) * 100:.1f}c "
                   f"· 1u paper · starts {when}**")
        out.append(f"Agree ({r['agree_n']}): {r['agree']}")
        out.append("")
    return "\n".join(out)


def roster_health(rows, now):
    """Once a day after 8am MT: 7-day stats per trader. Returns (stats, warning markdown or '')."""
    local = now.astimezone(MT)
    state = json.loads(HEALTH.read_text()) if HEALTH.exists() else {}
    if local.hour < 8 or state.get("date") == local.date().isoformat():
        return None, ""
    since = now - timedelta(days=HEALTH_DAYS)
    stats = {}
    for n, w in TRADERS.items():
        try:
            stats[n] = trader_stats(w, since.timestamp(), HEALTH_DAYS)
        except Exception as e:
            print(f"health pull failed for {n}: {type(e).__name__}", file=sys.stderr)
    recent = [r for r in rows if roster(r) == "new" and r["logged_at"] >= since.strftime("%Y-%m-%dT%H:%M:%SZ")]
    for n, t in stats.items():
        t["agreements"] = len(recent)
        t["share"] = round(sum(n in r["agree"].split("; ") for r in recent) / len(recent), 3) if recent else 0.0
    sent = state.get("sent", {})
    flags = []
    for n, t in stats.items():
        for key, label, kind, warn, alarm in HEALTH_RULES:
            if key == "share" and t["agreements"] < MIN_AGREEMENTS_FOR_SHARE:
                continue
            if key == "per_day" and kind == "low" and t["days"] == 0 and t["markets"] == 0:
                level = "alert"
            elif kind == "high":
                level = "alert" if t[key] > alarm else "warn" if t[key] > warn else None
            else:
                level = "alert" if t[key] < alarm else "warn" if t[key] < warn else None
            if not level:
                continue
            k = f"{n}|{label}|{level}"
            last = sent.get(k)
            if last and date.fromisoformat(last) > local.date() - timedelta(days=7):
                continue  # same warning already sent this week
            sent[k] = local.date().isoformat()
            val = f"{t[key] * 100:.0f}% of {t['agreements']}" if key == "share" else f"{t[key]}"
            limit = (f"{alarm * 100:.0f}%" if key == "share" else alarm) if level == "alert" else \
                    (f"{warn * 100:.0f}%" if key == "share" else warn)
            bench = f"{BENCH[n][0]} ({BENCH[n][2]})" if n in BENCH else "run consensus-screen"
            flags.append(f"| {'🔴 ALERT' if level == 'alert' else '🟡 early warning'} | {n} | {label} | {val} | "
                         f"{'over' if kind == 'high' else 'under'} {limit} | {bench} |")
    HEALTH.write_text(json.dumps({"date": local.date().isoformat(), "stats": stats, "sent": sent}, indent=1) + "\n")
    if not flags:
        return stats, ""
    names = sorted({f.split(" | ")[1] for f in flags})
    return stats, "\n".join([
        f"Consensus roster warning: {', '.join(names)}",
        f"Daily roster health check ({HEALTH_DAYS}-day window). Each warning is sent at most once a week.", "",
        "| Level | Trader | Symptom | Now | Limit | Swap candidate |", "|---|---|---|---|---|---|", *flags, "",
        "Full roster stats are in `consensus/summary.md`. To look for a replacement, run the "
        "`consensus-screen` workflow (Actions tab) or ask Claude.",
    ]) + "\n"


def due_reports(rows, now, stats):
    """Official reports due now: old-roster final (Nov 10), then new roster every Friday from Nov 13."""
    local = now.astimezone(MT)
    if local.hour < 8:
        return []
    sent = set(REPORTS_SENT.read_text().split()) if REPORTS_SENT.exists() else set()
    d = local.date()
    out = []
    if d >= OLD_REPORT_DATE and "old-final" not in sent:
        old = [r for r in rows if roster(r) == "old"]
        clean = [r for r in old if "old grouping" not in (r.get("note") or "")]
        out.append(("old-final", "\n".join([
            "Consensus old roster: final report (Nov 3–7)",
            "**Old roster, final.** Included Multicoloured-Serf, googleplay, ethanaz, 0xd4aa6f8e and scootergene; "
            "retired Nov 7 6:40pm MT. Paper tracking, 1 unit flat at the logged price.", "",
            "### All old-roster signals", "", *record_table(old), "",
            "### After the Nov 5 per-market fix only (cleanest data)", "", *record_table(clean), "",
            f"Still open: {sum(r['status'] == 'open' for r in old)}. New-roster reports start Fri Nov 13.", "", RULES,
        ]) + "\n"))
    friday = d - timedelta(days=(d.weekday() - 4) % 7)
    if friday >= NEW_REPORT_FIRST and f"new-{friday}" not in sent:
        new = [r for r in rows if roster(r) == "new"]
        wk = [r for r in new if r["logged_at"] >= (friday - timedelta(days=7)).isoformat()]
        h = stats or (json.loads(HEALTH.read_text()).get("stats", {}) if HEALTH.exists() else {})
        n = (friday - NEW_REPORT_FIRST).days // 7 + 1
        out.append((f"new-{friday}", "\n".join([
            f"Consensus new roster: report #{n} ({friday:%b %-d})",
            f"**New roster, report #{n}.** Roster live since Nov 7 6:40pm MT. Paper tracking, 1 unit flat at the "
            "logged price.", "",
            f"### Last 7 days (logged since {friday - timedelta(days=7):%b %-d})", "", *record_table(wk), "",
            "### Since the new roster started", "", *record_table(new), "", RULES, "",
            f"### Roster health (last {HEALTH_DAYS} days)", "", *health_table(h), "",
            "Watch for: >17 bets/day or >33% of agreements (Serf-style), >10% both sides (ethanaz-style), <5 bets/day.",
        ]) + "\n"))
    return out


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    now = datetime.now(timezone.utc)
    rows = load()
    found, failed = scan(now)
    new_plays = merge(rows, found, now)
    graded = grade(rows)
    save(rows)
    stats, warning = roster_health(rows, now)
    write_summary(rows, now)
    print(f"logged {len(rows)} total, {len(new_plays)} new paper plays, graded {graded} this run, "
          f"failed traders: {', '.join(failed) or 'none'}")
    if new_plays:
        (out / "play.md").write_text(alert(new_plays))
    if warning:
        (out / "health.md").write_text(warning)
    reports = due_reports(rows, now, stats)
    for rid, body in reports:
        (out / f"report-{rid}.md").write_text(body)
    if reports:
        sent = REPORTS_SENT.read_text() if REPORTS_SENT.exists() else ""
        REPORTS_SENT.write_text(sent + "".join(rid + "\n" for rid, _ in reports))
    if len(failed) > 5:
        raise SystemExit(f"{len(failed)} of {len(TRADERS)} trader pulls failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
