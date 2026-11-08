"""One-off screen for consensus-tracker replacements. Read-only; prints a markdown table.

For the top N monthly sports-profit traders (plus everyone currently tracked), looks at the last
7 days of BUY trades on dated sports events and counts *directional* markets: a market where the
trader put $1k+ in, with 75%+ of their money on one side. Reports markets/day, active days,
the share of their markets they traded both sides of, and average stake per market.
"""
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from consensus import DATA, TRADERS, get_retry, trader_stats  # noqa: E402

DAYS = 7
TOP = int(sys.argv[1]) if len(sys.argv) > 1 else 100


def leaderboard(n):
    out, cursor = [], None
    while len(out) < n:
        p = {"category": "SPORTS", "timePeriod": "MONTH", "orderBy": "PNL", "limit": 50}
        if cursor:
            p["cursor"] = cursor
        j = get_retry(f"{DATA}/v2/leaderboard", **p)
        out += j.get("data") or []
        cursor = (j.get("pagination") or {}).get("next_cursor")
        if not cursor:
            break
    return out[:n]


def stats(wallet, since):
    try:
        return trader_stats(wallet, since, DAYS)
    except Exception:
        return {"per_day": 0, "days": 0, "markets": 0, "both_pct": 0, "stake": 0, "leagues": "(pull failed)"}


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
    print("| Rank | Trader | Wallet | Month PnL | Directional mkts/day | Active days | Both-sides % | Avg stake | Top sports | Tracked |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for u, s, t in rows:
        print(f"| {u['rank']} | {u['user_name'][:28]} | {u['user_id']} | {float(u['pnl']) / 1000:,.0f}k | "
              f"{s['per_day']:.1f} | {s['days']} | {s['both_pct']} | ${s['stake']:,.0f} | {s['leagues']} | {t or ''} |")


if __name__ == "__main__":
    main()
