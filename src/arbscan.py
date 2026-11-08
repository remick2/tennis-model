"""1-minute arb scanner: Kalshi + Polymarket US, pre-match AND in-play (PAPER ONLY).

Why: hourly snapshots can't see gaps that last minutes. Both venues share settlement rules (walkover =
last fair price, retirement = official winner), so buying player A on one venue and player B on the
other for < $1 all-in is close to a locked profit.

Each scan (default every 10s; well under Kalshi's ~20 req/s and Polymarket US's 25 req/s limits):
  - pull every open tennis match market on Kalshi (4 series) and Polymarket US (atp + wta leagues)
  - match the same match across venues, take the cheapest ask for each player, add taker fees
    (Kalshi 0.07*p*(1-p), Polymarket US 0.0695*p*(1-p))
  - if a cross-venue combo costs < $1: re-check both order books for size at those prices, then again
    at +1s and +3s (simulating a bot that fires both orders at once): bot_ok = still >= MIN_LOCK at +1s
  - log one summary row per scan, every sub-$1 combo, and how long each arb lasted
  - open a GitHub issue (phone alert) for a NEW executable arb that locks >= MIN_LOCK dollars
Commits data every 15 min; hands off to a new GitHub run before the 6h job limit.

Run: python arbscan.py --minutes 340 [--interval 60] [--once]
"""
import argparse
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

from snapshot import canonical

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "arbscan"
KALSHI = "https://api.elections.kalshi.com/trade-api/v2"
POLYUS = "https://gateway.polymarket.us"
K_SERIES = ["KXATPMATCH", "KXWTAMATCH", "KXATPCHALLENGERMATCH", "KXWTACHALLENGERMATCH"]
FEE = {"kalshi": 0.07, "polyus": 0.0695}
MIN_LOCK = 1.00          # dollars locked before an alert is worth it
RUN = os.environ.get("GITHUB_RUN_ID", "local")  # each run writes its own files (no git conflicts between runs)
S = requests.Session()


def now():
    return datetime.now(timezone.utc)


def get(url, params=None, tries=3):
    for i in range(tries):
        try:
            r = S.get(url, params=params, timeout=20)
            if r.status_code == 200:
                return r.json()
        except requests.RequestException:
            pass
        time.sleep(1 + i)
    return None


# ------------------------------------------------------------------ venues
def kalshi_rows():
    rows = []
    for series in K_SERIES:
        d = get(f"{KALSHI}/markets", {"series_ticker": series, "status": "open", "limit": 1000}) or {}
        by_ev = {}
        for m in d.get("markets", []):
            by_ev.setdefault(m["event_ticker"], []).append(m)
        for ev, pair in by_ev.items():
            if len(pair) != 2:
                continue
            for i, m in enumerate(pair):
                bid, ask = float(m.get("yes_bid_dollars") or 0), float(m.get("yes_ask_dollars") or 0)
                if not (0 < ask < 1):
                    continue
                rows.append({"source": "kalshi", "series": series, "ref": m["ticker"], "event": ev,
                             "player": m.get("yes_sub_title"), "opp": pair[1 - i].get("yes_sub_title"),
                             "bid": bid, "ask": ask})
    return rows


def polyus_rows():
    rows = []
    for lg in ("atp", "wta"):
        d = get(f"{POLYUS}/v2/leagues/{lg}/events", {"limit": 500}) or {}
        for e in d.get("events", []):
            if e.get("closed") or e.get("ended"):
                continue
            for m in e.get("markets", []):
                if m.get("sportsMarketType") != "tennis_match_winner" or m.get("closed"):
                    continue
                names = json.loads(m.get("outcomes") or "[]")
                bq, aq = m.get("bestBidQuote") or {}, m.get("bestAskQuote") or {}
                if len(names) != 2 or not bq.get("value") or not aq.get("value"):
                    continue
                bb, ba = float(bq["value"]), float(aq["value"])
                for i, (bid, ask) in enumerate([(bb, ba), (round(1 - ba, 4), round(1 - bb, 4))]):
                    if 0 < ask < 1:
                        rows.append({"source": "polyus", "series": lg, "ref": f"{m['slug']}#{i}",
                                     "event": e.get("slug"), "player": names[i], "opp": names[1 - i],
                                     "bid": bid, "ask": ask, "live": bool(e.get("live"))})
    return rows


def depth(src, ref, price):
    """(shares on offer at <= price for buying this side, best ask in the book) or (None, None)."""
    try:
        if src == "kalshi":
            ob = (get(f"{KALSHI}/markets/{ref}/orderbook") or {}).get("orderbook_fp") or {}
            lv = [(1 - float(p), float(q)) for p, q in (ob.get("no_dollars") or [])]
        else:
            slug, idx = ref.rsplit("#", 1)
            b = (get(f"{POLYUS}/v1/markets/{slug}/book") or {}).get("marketData") or {}
            if idx == "0":
                lv = [(float(a["px"]["value"]), float(a["qty"])) for a in (b.get("offers") or b.get("asks") or [])]
            else:
                lv = [(1 - float(a["px"]["value"]), float(a["qty"])) for a in b.get("bids", [])]
        best = round(min(p for p, _ in lv), 4) if lv else None
        return sum(q for p, q in lv if p <= price + 1e-9), best
    except Exception:
        return None, None


# ------------------------------------------------------------------ scan
def scan():
    t0 = now()
    rows = kalshi_rows() + polyus_rows()
    if not rows:
        return t0, pd.DataFrame(), pd.DataFrame()
    df = pd.DataFrame(rows)
    df["live"] = df.get("live", False).fillna(False) if "live" in df else False
    df["cost"] = df.ask + df.source.map(FEE) * df.ask * (1 - df.ask)
    df["key"], df["side"] = canonical(df)
    df["key"] = df.key.map(lambda k: " v ".join(sorted(k)))
    combos = []
    for key, g in df.groupby("key"):
        if g.source.nunique() < 2 or g.side.nunique() != 2:
            continue
        a_side, b_side = sorted(g.side.unique())
        A, B = g[g.side == a_side], g[g.side == b_side]
        for ra in A.itertuples():
            for rb in B.itertuples():
                if ra.source == rb.source:
                    continue  # same-venue pairs can't be < $1 after the spread
                combos.append({"key": key, "live": bool(ra.live or rb.live),
                               "leg_a": ra.player, "src_a": ra.source, "ref_a": ra.ref, "px_a": ra.ask,
                               "leg_b": rb.player, "src_b": rb.source, "ref_b": rb.ref, "px_b": rb.ask,
                               "total": ra.cost + rb.cost})
    c = pd.DataFrame(combos)
    if len(c):
        c = c.drop_duplicates(["key", "leg_a", "src_a", "ref_a", "leg_b", "src_b", "ref_b"])
    return t0, df, c


def log(path, rows):
    if not len(rows):
        return
    rows = pd.DataFrame(rows)
    old = pd.read_csv(path) if path.exists() else pd.DataFrame()
    pd.concat([old, rows], ignore_index=True).to_csv(path, index=False)


def alert(r):
    """Paper alert as a GitHub issue: bet, price, size, cutoff up front."""
    mt = pd.Timestamp(r["ts"]).tz_convert("America/Denver").strftime("%a %-I:%M%p MT")
    body = (f"**PAPER ARB ({'LIVE' if r['live'] else 'pre-match'}) · locks ${r['locked']:.2f}**\n\n"
            f"- **Buy {r['leg_a']} on {r['src_a'].upper()} @ {r['px_a']:.2f}**\n"
            f"- **Buy {r['leg_b']} on {r['src_b'].upper()} @ {r['px_b']:.2f}**\n"
            f"- **Size: {int(r['size'])} shares each** · all-in ${r['total']:.3f} per pair "
            f"→ {100 * (1 - r['total']):.1f}¢ locked per $1\n"
            f"- Seen {mt}. Still there 1s later (simulated bot): **{'YES' if r.get('bot_ok') else 'NO'}** "
            f"(${r.get('locked_1s', 0):.2f} locked at +1s, ${r.get('locked_3s', 0):.2f} at +3s).\n\n"
            "Both venues settle walkovers at the last fair price and retirements to the official winner.")
    if os.environ.get("GH_TOKEN"):
        subprocess.run(["gh", "issue", "create", "--title", f"Paper ARB: {r['leg_a']} / {r['leg_b']} "
                        f"({100 * (1 - r['total']):.1f}¢, ${r['locked']:.0f})", "--body", body], check=False)
    else:
        print(body)


def commit(msg):
    cmd = ("git add data/arbscan && (git diff --cached --quiet || git commit -qm \"%s\"); "
           "for i in 1 2 3 4 5; do "
           "  if git pull --rebase -q origin main && git push -q origin HEAD:main; then echo pushed; break; fi; "
           "  git rebase --abort 2>/dev/null; echo \"push attempt $i failed\"; sleep $((i*20)); "
           "done") % msg
    subprocess.run(["bash", "-c", cmd], cwd=ROOT, check=False)


def dispatch_next():
    for i in range(8):
        if subprocess.run(["gh", "workflow", "run", "arbscan.yml", "--ref", "main"], cwd=ROOT).returncode == 0:
            print("next scanner run requested"); return True
        time.sleep(30 * (i + 1))
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=340)
    ap.add_argument("--interval", type=int, default=10)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--no-git", action="store_true")
    a = ap.parse_args()
    if not a.no_git:  # GitHub checks out the commit from when the run was *requested* (up to 1h earlier)
        subprocess.run(["bash", "-c", "git fetch -q origin main && git checkout -q -B main origin/main"],
                       cwd=ROOT, check=False)
    OUT.mkdir(parents=True, exist_ok=True)
    start, open_arbs, open_exec, alerted, handed_off, last_commit = time.time(), {}, {}, set(), False, time.time()
    while True:
        t0, df, c = scan()
        day = t0.strftime("%Y-%m-%d")
        ts = t0.isoformat(timespec="seconds")
        summ = {"ts": ts, "kalshi_sides": int((df.source == "kalshi").sum()) if len(df) else 0,
                "polyus_sides": int((df.source == "polyus").sum()) if len(df) else 0,
                "matched": int(c.key.nunique()) if len(c) else 0,
                "live_matched": int(c[c.live].key.nunique()) if len(c) else 0,
                "best_total": round(float(c.total.min()), 4) if len(c) else None,
                "best_key": c.loc[c.total.idxmin(), "key"] if len(c) else None}
        found = []
        if len(c):
            for r in c[c.total < 1.0].sort_values("total").itertuples():
                tc = t_detect = time.time()
                (sa, ba), (sb, bb) = depth(r.src_a, r.ref_a, r.px_a), depth(r.src_b, r.ref_b, r.px_b)
                tc = round(time.time() - tc, 1)
                book_total = (round(ba + FEE[r.src_a] * ba * (1 - ba) + bb + FEE[r.src_b] * bb * (1 - bb), 4)
                              if ba is not None and bb is not None else None)
                size = min(x for x in (sa, sb) if x is not None) if (sa is not None and sb is not None) else 0
                rec = {"ts": ts, "key": r.key, "live": r.live, "leg_a": r.leg_a, "src_a": r.src_a, "px_a": r.px_a,
                       "leg_b": r.leg_b, "src_b": r.src_b, "px_b": r.px_b, "total": round(r.total, 4),
                       "size_a": sa, "size_b": sb, "size": size, "locked": round(size * (1 - r.total), 2),
                       "book_a": ba, "book_b": bb, "book_total": book_total, "check_secs": tc}
                found.append(rec)
                k = (r.key, r.leg_a, r.src_a, r.leg_b, r.src_b)
                open_arbs.setdefault(k, [ts, ts])[1] = ts
                rec["first_seen"] = open_arbs[k][0]
                if rec["locked"] >= MIN_LOCK:
                    open_exec.setdefault(k, [ts, ts])[1] = ts
                    # bot simulation: both orders fire at once ~1s after detection. Re-read both books at +1s
                    # and +3s: is the combo still under $1 with real size on BOTH legs?
                    for lag in (1, 3):
                        time.sleep(max(0.0, t_detect + lag - time.time()))
                        (sa2, _), (sb2, _) = depth(r.src_a, r.ref_a, r.px_a), depth(r.src_b, r.ref_b, r.px_b)
                        sz2 = min(sa2 or 0, sb2 or 0)
                        rec[f"size_{lag}s"] = sz2
                        rec[f"locked_{lag}s"] = round(sz2 * (1 - r.total), 2)
                    rec["bot_ok"] = rec["locked_1s"] >= MIN_LOCK  # what the arb gate counts
                if rec["locked"] >= MIN_LOCK and (r.key, day) not in alerted:
                    alerted.add((r.key, day)); alert(rec)
        # arbs that closed since the last scan: log their lifetime. minutes = upper bound (first seen ->
        # first scan without it); min_minutes = lower bound (first -> last scan with it). kind "exec" tracks
        # only the scans where it was executable (>= MIN_LOCK locked), which is what the gate's median uses.
        live_keys = {(f["key"], f["leg_a"], f["src_a"], f["leg_b"], f["src_b"]) for f in found}
        exec_keys = {(f["key"], f["leg_a"], f["src_a"], f["leg_b"], f["src_b"]) for f in found
                     if f["locked"] >= MIN_LOCK}
        closed = []
        for kind, book, still in (("any", open_arbs, live_keys), ("exec", open_exec, exec_keys)):
            for k in [k for k in book if k not in still]:
                first, last = book.pop(k)
                closed.append({"key": k[0], "legs": f"{k[1]}@{k[2]} + {k[3]}@{k[4]}", "first_seen": first,
                               "closed_by": ts, "kind": kind,
                               "minutes": round((pd.Timestamp(ts) - pd.Timestamp(first)).total_seconds() / 60, 1),
                               "min_minutes": round((pd.Timestamp(last) - pd.Timestamp(first)).total_seconds() / 60, 1)})
        summ["arbs_under_1"] = len(found)
        log(OUT / f"{day}_{RUN}_scans.csv", [summ])
        log(OUT / f"{day}_{RUN}_arbs.csv", found)
        log(OUT / f"{day}_{RUN}_lifetimes.csv", closed)
        print(f"{ts} k={summ['kalshi_sides']} pu={summ['polyus_sides']} matched={summ['matched']} "
              f"(live {summ['live_matched']}) best={summ['best_total']} arbs={len(found)}", flush=True)
        if a.once:
            break
        elapsed = (time.time() - start) / 60
        if not a.no_git and time.time() - last_commit > 15 * 60:
            commit(f"arbscan {ts[:16]}Z"); last_commit = time.time()
        if not a.no_git and not handed_off and elapsed > a.minutes - 60:
            handed_off = dispatch_next()
        if elapsed > a.minutes:
            break
        time.sleep(max(0, a.interval - (now() - t0).total_seconds()))
    if not a.no_git:
        if not handed_off:
            dispatch_next()
        commit(f"arbscan {now().isoformat(timespec='minutes')[:16]}Z")


if __name__ == "__main__":
    main()
