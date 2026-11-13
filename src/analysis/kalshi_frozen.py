"""For every gate_ok arb occasion, count trades on the Kalshi leg's market within +/-5 min of detection.

Zero trades in a live match while the other venue moves is a sign the Kalshi book was frozen (resting orders
nobody could hit), so the arb probably could not have filled. Analysis only: does not change gate_ok.
Run from the repo root: python src/analysis/kalshi_frozen.py
"""
import glob
import time

import pandas as pd
import requests

K = "https://api.elections.kalshi.com/trade-api/v2"
SERIES = ["KXATPMATCH", "KXWTAMATCH", "KXATPCHALLENGERMATCH", "KXWTACHALLENGERMATCH"]
BANKROLL = 690


def gate_occasions():
    a = pd.concat([pd.read_csv(f) for f in glob.glob("data/arbscan/*_arbs.csv")], ignore_index=True)
    a["ts"] = pd.to_datetime(a.ts, utc=True, format="mixed")
    bp = a.apply(lambda r: min(r.size_1s, BANKROLL / r.total) * (1 - r.total) - 0.02
                 if pd.notna(r.get("size_1s")) else float("nan"), axis=1)
    a["bp"] = a["bankroll_profit"].fillna(bp) if "bankroll_profit" in a else bp
    ok = a.bot_ok.astype(str).str.lower().isin(["true", "1", "1.0"]) & (a.bp >= 1)
    g = a[ok].sort_values("ts")
    return g.groupby(["key", "first_seen"], sort=False).first().reset_index()


def kalshi_markets(since):
    out = []
    for s in SERIES:
        cur = None
        while True:
            p = {"series_ticker": s, "limit": 1000, "min_close_ts": int(since.timestamp())}
            if cur:
                p["cursor"] = cur
            d = requests.get(f"{K}/markets", params=p, timeout=30).json()
            out += d.get("markets", [])
            cur = d.get("cursor")
            if not cur or not d.get("markets"):
                break
    return out


def main():
    g = gate_occasions()
    mk = kalshi_markets(g.ts.min() - pd.Timedelta("1D"))
    rows = []
    for r in g.itertuples():
        leg = r.leg_a if r.src_a == "kalshi" else r.leg_b
        c = [m for m in mk if m.get("yes_sub_title") == leg
             and pd.Timestamp(m["open_time"]) <= r.ts <= pd.Timestamp(m["close_time"])]
        n = None
        if c:
            t = int(r.ts.timestamp())
            d = requests.get(f"{K}/markets/trades", params={"ticker": c[0]["ticker"], "limit": 1000,
                             "min_ts": t - 300, "max_ts": t + 300}, timeout=20).json()
            n = len(d.get("trades") or [])
            time.sleep(0.1)
        rows.append({"ts": r.ts.strftime("%Y-%m-%d %H:%M"), "key": r.key, "live": r.live, "total": r.total,
                     "bankroll_profit": round(r.bp, 2), "kalshi_trades_10min": n})
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    traded = df[df.kalshi_trades_10min.fillna(0) > 0]
    print(f"\n{len(df)} gate_ok occasions on {df.ts.str[:10].nunique()} days; "
          f"{len(traded)} on {traded.ts.str[:10].nunique()} days had Kalshi trades around detection.")


if __name__ == "__main__":
    main()
