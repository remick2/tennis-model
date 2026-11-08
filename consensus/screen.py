"""One-off screen for consensus-tracker replacements. Read-only; prints a markdown table.

For the top N monthly sports-profit traders (plus everyone currently tracked), looks at the last
7 days of BUY trades on dated sports events and counts *directional* markets: a market where the
trader put $1k+ in, with 75%+ of their money on one side. Reports markets/day, active days,
the share of their markets they traded both sides of, and average stake per market.
"""
import sys
import time
from collections import defaultdict

import requests

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from consensus import DATA, TRADERS, UA  # noqa: E402

DAYS = 7
TOP = int(sys.argv[1]) if len(sys.argv) > 1 else 100


def get(url, **params):
    for i in range(4):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception:
            time.sleep(2 * (i + 1))
    return {}


def leaderboard(n):
    out, cursor = [], None
    while len(out) < n:
        p = {"category": "SPORTS", "timePeriod": "MONTH", "orderBy": "PNL", "limit": 50}
        if cursor:
            p["cursor"] = cursor
        j = get(f"{DATA}/v2/leaderboard", **p)
        out += j.get("data") or []
        cursor = (j.get("pagination") or {}).get("next_cursor")
        if not cursor:
            break
    return out[:n]


def trades(wallet, since):
    out, cursor = [], None
    for _ in range(10):
        p = {"user": wallet, "limit": 500}
        if cursor:
            p["cursor"] = cursor
        j = get(f"{DATA}/v2/activity", **p)
        d = j.get("data") or []
        out += d
        cursor = (j.get("pagination") or {}).get("next_cursor")
        if not cursor or not d or d[-1]["timestamp"] < since:
            break
    return [a for a in out if a["timestamp"] >= since and a.get("type") == "TRADE" and a.get("side") == "BUY"
            and a.get("event_slug", "")[-10:-8] == "20"]


def stats(wallet, since):
    mk = defaultdict(lambda: defaultdict(float))
    days = set()
    for a in trades(wallet, since):
        mk[a["condition_id"]][a["outcome_index"]] += float(a["usdc_size"])
        days.add(time.strftime("%Y-%m-%d", time.gmtime(a["timestamp"] - 7 * 3600)))
    both = sum(len(s) > 1 for s in mk.values())
    directional = [s for s in mk.values() if sum(s.values()) >= 1000 and max(s.values()) >= 0.75 * sum(s.values())]
    stake = sum(sum(s.values()) for s in directional) / len(directional) if directional else 0
    return {"per_day": len(directional) / DAYS, "days": len(days), "markets": len(mk),
            "both_pct": round(100 * both / len(mk)) if mk else 0, "stake": stake}


def main():
    since = time.time() - DAYS * 86400
    lb = leaderboard(TOP)
    tracked = {w.lower(): n for n, w in TRADERS.items()}
    rows = []
    for u in lb:
        w = u["user_id"].lower()
        s = stats(w, since)
        rows.append((u, s, tracked.get(w)))
    seen = {u["user_id"].lower() for u in lb}
    for n, w in TRADERS.items():  # tracked traders who fell off the board, for reference
        if w.lower() not in seen:
            rows.append(({"rank": "-", "user_name": n, "user_id": w, "pnl": 0, "volume": 0}, stats(w, since), n))
    print(f"# Consensus replacement screen ({DAYS} days, top {TOP} monthly sports PnL)\n")
    print("| Rank | Trader | Wallet | Month PnL | Directional mkts/day | Active days | Both-sides % | Avg stake | Tracked |")
    print("|---|---|---|---|---|---|---|---|---|")
    for u, s, t in rows:
        print(f"| {u['rank']} | {u['user_name'][:28]} | {u['user_id']} | {float(u['pnl']) / 1000:,.0f}k | "
              f"{s['per_day']:.1f} | {s['days']} | {s['both_pct']} | ${s['stake']:,.0f} | {t or ''} |")


if __name__ == "__main__":
    main()
