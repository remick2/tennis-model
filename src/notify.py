"""Build a short alert for new flags in the latest snapshot. Prints markdown (empty if nothing new).
De-dupes on (match, side, source) so the same flag doesn't alert every run."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "data" / "snapshots"
SEEN = ROOT / "data" / "notified.csv"
BANKROLL = 700.0      # Phase 3 hard cap (Fullstar + Kalshi + Polymarket combined)
KELLY_FRAC = 0.25     # quarter Kelly
MAX_PCT = 0.02        # never more than 2% of bankroll on one bet


def stake(p_fair, cost):
    """Quarter-Kelly stake for a $1-payout contract bought at all-in `cost`, sized off Pinnacle's
    fair prob (not the model). Returns (dollars, shares)."""
    f = KELLY_FRAC * (p_fair - cost) / (1 - cost)
    dollars = max(0.0, min(f, MAX_PCT)) * BANKROLL
    return dollars, int(dollars // cost)


def arb_alerts():
    """New true arbs (total < $1 all-in) in the latest run."""
    files = sorted((ROOT / "data" / "arbs").glob("20*.csv"))
    if not files:
        return []
    a = pd.read_csv(files[-1])
    a = a[(a.ts == a.ts.max()) & (a.total < 1.0)]
    seen_f = ROOT / "data" / "notified_arbs.csv"
    seen = set(pd.read_csv(seen_f).key) if seen_f.exists() else set()
    new = a[~a.key.isin(seen)]
    if new.empty:
        return []
    pd.concat([pd.read_csv(seen_f) if seen_f.exists() else pd.DataFrame(columns=["key"]), new[["key"]]]
              ).to_csv(seen_f, index=False)
    lines = ["**ARB CHECK (paper): both sides for under $1 all-in.**"]
    for r in new.itertuples():
        lines.append(f"- **Buy {r.leg_a} + {r.leg_b}** → total {r.total:.3f}, locks "
                     f"**{r.profit_per_dollar * 100:.1f}¢ per $1** | Kalshi size at ask: {r.kalshi_size}")
    lines.append("Verify both prices live first; they move fast. Walkover rules differ between venues.")
    return lines


def main():
    extra = arb_alerts()
    files = sorted(SNAP.glob("20*.csv"))
    if not files:
        return
    d = pd.read_csv(files[-1])
    d = d[(d.ts == d.ts.max()) & (d.flag == True)]
    seen = pd.read_csv(SEEN) if SEEN.exists() else pd.DataFrame(columns=["key", "player", "source"])
    ids = set(zip(seen.key, seen.player, seen.source))
    new = d[[(k, p, s) not in ids for k, p, s in zip(d.key, d.player, d.source)]]
    if new.empty:
        if extra:
            print("\n".join(extra))
        return
    start = pd.to_datetime(new.start, utc=True).dt.tz_convert("America/Denver").dt.strftime("%a %-I:%M%p MT")
    lines = ["**PAPER ONLY. Log it, don't bet it (Phase 2).**", ""]
    day = pd.read_csv(files[-1])
    for r, st in zip(new.itertuples(), start):
        dollars, shares = stake(r.pin_fair, r.cost)
        # line move on this side since first seen today (Pinnacle fair if we have it)
        hist = day[(day.key == r.key) & (day.player == r.player) & (day.source == "pinnacle")].sort_values("ts")
        move = (hist.fair.iloc[-1] - hist.fair.iloc[0]) if len(hist) > 1 else 0.0
        warns = [w for w in [r.warn if isinstance(r.warn, str) else "",
                             f"Pinnacle moved {move * 100:+.0f}c on this side since {hist.ts.iloc[0][11:16]}Z (market may know something)"
                             if move <= -0.04 else ""] if w]
        agree = "model agrees" if r.model_edge == r.model_edge and r.model_edge >= 0.02 else "model doesn't agree"
        lines.append(f"- **{r.player} to win** vs {r.opp} | **{r.source.upper()} @ {r.ask:.2f}** | "
                     f"**paper size: {shares} shares (~${shares * r.ask:.2f})** | start {st}  \n"
                     f"  all-in {r.cost:.3f} · Pinnacle fair {r.pin_fair:.3f} · edge {100 * r.price_edge:.1f}c · "
                     f"model {r.p_model:.3f} ({agree}, info only)")
        for w in warns:
            lines.append(f"  ⚠️ {w}. Check official ATP/WTA news before logging it.")
    lines += ["", f"Flag = Pinnacle fair − all-in cost ≥ 2¢ (price only; model is info). "
                  f"Snapshot {d.ts.max()[:16]}Z. Prices may have moved since."]
    print("\n".join(lines + ([""] + extra if extra else [])))
    pd.concat([seen, new[["key", "player", "source"]]]).to_csv(SEEN, index=False)


if __name__ == "__main__":
    main()
