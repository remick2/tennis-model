"""Pre-match Kalshi prices for settled Challenger / WTA125 matches (for the Challenger backtest).

Kalshi markets keep trading in-play and its 'occurrence' time isn't a reliable start time, so the
pre-match price = the last hourly candle ending >= 3h before the market settled (matches run
~1.5-2.5h). Saves the winner-side market's bid/ask; cached in data/kalshi_prices.csv.
"""
import json
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "kalshi_prices.csv"
API = "https://api.elections.kalshi.com/trade-api/v2"
SERIES = ["KXATPCHALLENGERMATCH", "KXWTACHALLENGERMATCH"]


SESSION = requests.Session()


def _get(url, params):
    """Kalshi rate-limits bursts (429, no Retry-After): short waits work better than long backoff.
    Network errors are retried too, so one dropped connection doesn't kill a long download."""
    for a in range(25):
        try:
            r = SESSION.get(url, params=params, timeout=30)
        except requests.RequestException:
            time.sleep(2); continue
        if r.status_code == 200:
            return r.json()
        time.sleep(1.0 if r.status_code == 429 else 3.0)
    return None


def settled(series):
    ms, cur = [], None
    while True:
        p = {"series_ticker": series, "status": "settled", "limit": 1000}
        if cur: p["cursor"] = cur
        d = _get(f"{API}/markets", p) or {}
        ms += d.get("markets", []); cur = d.get("cursor")
        if not cur or not d.get("markets"):
            return ms
        time.sleep(0.5)


def main():
    done = set(pd.read_csv(OUT).event) if OUT.exists() else set()
    for series in SERIES:
        winners = [m for m in settled(series) if m.get("result") == "yes" and m["event_ticker"] not in done]
        print(series, len(winners), "to fetch", flush=True)
        buf = []
        for i, m in enumerate(winners):
            close = pd.Timestamp(m["close_time"]).timestamp()
            d = _get(f"{API}/series/{series}/markets/{m['ticker']}/candlesticks",
                     {"start_ts": int(close - 36 * 3600), "end_ts": int(close), "period_interval": 60})
            row = {"event": m["event_ticker"], "series": series, "ticker": m["ticker"],
                   "close_time": m["close_time"], "bid": None, "ask": None, "candle_end": None, "vol_24h": None}
            if d and d.get("candlesticks"):
                c = [x for x in d["candlesticks"] if x["end_period_ts"] <= close - 3 * 3600]
                if c:
                    x = c[-1]
                    row.update(bid=float((x.get("yes_bid") or {}).get("close_dollars") or "nan"),
                               ask=float((x.get("yes_ask") or {}).get("close_dollars") or "nan"),
                               candle_end=x["end_period_ts"],
                               vol_24h=sum(float(y.get("volume_fp", y.get("volume", 0)) or 0) for y in c[-24:]))
            buf.append(row)
            time.sleep(0.1)
            if len(buf) >= 200 or i == len(winners) - 1:
                pd.DataFrame(buf).to_csv(OUT, mode="a", header=not OUT.exists(), index=False)
                buf = []
                print(f"  {i + 1}/{len(winners)}", flush=True)


if __name__ == "__main__":
    main()
