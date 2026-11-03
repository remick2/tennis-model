"""Phase 2 scorecard: did the prices we saw actually beat the market?

For every Kalshi/Polymarket side that had a Pinnacle fair price, take the FIRST snapshot where it
qualified for a group (realistic alert time), then grade it against:
  CLV  = Pinnacle's last no-vig fair price before the start  -  our all-in cost   (cents; + = good)
  ROI  = settled result on $1 at our all-in cost (Kalshi settlement; Polymarket via the same match)
Groups:
  price flag   : price edge >= 2c (Pinnacle fair - all-in cost), model ignored
  model+price  : the alert rule (price edge >= 2c AND model edge >= 2c)
  all          : every side at first sighting (baseline: what buying at random costs you)
CLV is the fast signal (every match counts, no luck from results). ROI needs hundreds of bets.
Note: Pinnacle is pulled every 4h, so "close" can be up to ~4h before the start.
Writes data/scorecard.md.
"""
import glob
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from snapshot import _toks

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.elections.kalshi.com/trade-api/v2/markets"
SERIES = ["KXATPMATCH", "KXWTAMATCH", "KXATPCHALLENGERMATCH", "KXWTACHALLENGERMATCH"]
MIN_EDGE = 0.02


def same(a, b):
    x, y = _toks(a), _toks(b)
    return bool(x) and bool(y) and (x <= y or y <= x)


def settled(since_ts):
    """Kalshi event -> winner name (yes_sub_title of the market that settled yes)."""
    win = {}
    for s in SERIES:
        cur = None
        while True:
            p = {"series_ticker": s, "status": "settled", "limit": 1000, "min_close_ts": int(since_ts)}
            if cur: p["cursor"] = cur
            for _ in range(10):
                try:
                    r = requests.get(API, params=p, timeout=30)
                    if r.status_code == 200: break
                except requests.RequestException:
                    pass
                time.sleep(2)
            d = r.json()
            for m in d.get("markets", []):
                if m.get("result") == "yes":
                    win[m["event_ticker"]] = m.get("yes_sub_title")
            cur = d.get("cursor")
            if not cur or not d.get("markets"):
                break
    return win


def load():
    d = pd.concat([pd.read_csv(f, low_memory=False) for f in sorted(glob.glob(str(ROOT / "data/snapshots/20*.csv")))],
                  ignore_index=True)
    d["ts"] = pd.to_datetime(d.ts, utc=True, format="ISO8601")
    d["start"] = pd.to_datetime(d.start, utc=True, errors="coerce", format="ISO8601")
    return d


def grade(d, win):
    pin = d[d.source == "pinnacle"]
    mk = d[d.source.isin(["kalshi", "poly"]) & d.pin_fair.notna() & d.cost.notna()].copy()
    # Kalshi event for every row (Polymarket rows borrow the Kalshi event of the same match in that run)
    kev = d[d.source == "kalshi"][["ts", "key", "event"]].drop_duplicates(["ts", "key"])
    mk = mk.merge(kev.rename(columns={"event": "kalshi_event"}), on=["ts", "key"], how="left")
    mk.loc[mk.source == "kalshi", "kalshi_event"] = mk.event

    def close_fair(r):
        p = pin[(pin.key == r.key) & (pin.ts < r.start)]
        p = p[[same(x, r.player) for x in p.player]]
        return p.sort_values("ts").fair.iloc[-1] if len(p) else np.nan

    def won(r):
        w = win.get(r.kalshi_event)
        return np.nan if w is None else float(same(w, r.player))

    groups = {"price flag (price edge >= 2c)": mk.price_edge >= MIN_EDGE,
              "model+price flag (alert rule)": (mk.price_edge >= MIN_EDGE) & (mk.model_edge >= MIN_EDGE),
              "all sides (baseline)": pd.Series(True, index=mk.index)}
    out, detail = [], []
    for name, m in groups.items():
        g = mk[m].sort_values("ts").drop_duplicates(["key", "player", "source"])  # first time it qualified
        if g.empty:
            out.append({"group": name, "sides": 0}); continue
        g = g.copy()
        g["close"] = [close_fair(r) for r in g.itertuples()]
        g["clv"] = g.close - g.cost
        g["won"] = [won(r) for r in g.itertuples()]
        g["pnl"] = np.where(g.won == 1, 1 / g.cost - 1, np.where(g.won == 0, -1.0, np.nan))
        c, s = g.clv.dropna(), g.pnl.dropna()
        out.append({"group": name, "sides": len(g), "avg_price_edge_c": 100 * g.price_edge.mean(),
                    "with_close": len(c), "avg_clv_c": 100 * c.mean() if len(c) else np.nan,
                    "clv_se_c": 100 * c.std() / np.sqrt(len(c)) if len(c) > 1 else np.nan,
                    "beat_close_%": 100 * (c > 0).mean() if len(c) else np.nan,
                    "settled": len(s), "won": int(g.won.sum()), "roi_%": 100 * s.mean() if len(s) else np.nan,
                    "roi_se_%": 100 * s.std() / np.sqrt(len(s)) if len(s) > 1 else np.nan})
        if name.startswith("price"):
            detail = g
    return pd.DataFrame(out), detail


def arb_summary():
    files = sorted(glob.glob(str(ROOT / "data/arbs/20*.csv")))
    if not files:
        return pd.DataFrame()
    a = pd.concat([pd.read_csv(f) for f in files])
    a["day"] = a.ts.str[:10]
    return a.groupby("day").agg(runs=("ts", "nunique"), best_total=("total", "min"),
                                under_1=("total", lambda t: int((t < 1).sum())),
                                under_1_005=("total", lambda t: int((t < 1.005).sum()))).reset_index()


def main():
    d = load()
    win = settled(d.ts.min().timestamp() - 86400)
    summ, detail = grade(d, win)
    lines = [f"# Phase 2 scorecard  ({pd.Timestamp.now(tz='America/Denver'):%a %b %-d %-I:%M%p} MT)", "",
             f"Snapshots: {d.ts.nunique()} runs, {d.ts.min():%b %-d} to {d.ts.max():%b %-d %H:%M}Z. "
             "Phase 3 gate: price flags beat the close on average (CLV > 0 by ~2 SE) over 100+ graded sides.", "",
             summ.round(2).to_markdown(index=False), ""]
    if len(detail):
        cols = ["ts", "source", "player", "opp", "cost", "pin_fair", "close", "clv", "won"]
        dd = detail[cols].copy(); dd["ts"] = dd.ts.dt.tz_convert("America/Denver").dt.strftime("%b %-d %-I:%M%p")
        lines += ["## Price flags (most recent 25)", "", dd.tail(25).round(3).to_markdown(index=False), ""]
    arbs = arb_summary()
    if len(arbs):
        lines += ["## Kalshi + Polymarket arbitrage check (best combo per match, all-in)", "",
                  arbs.round(4).to_markdown(index=False), ""]
    (ROOT / "data" / "scorecard.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
