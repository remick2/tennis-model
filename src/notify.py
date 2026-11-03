"""Build a short alert for new flags in the latest snapshot. Prints markdown (empty if nothing new).
De-dupes on (match, side, source) so the same flag doesn't alert every run."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "data" / "snapshots"
SEEN = ROOT / "data" / "notified.csv"


def main():
    files = sorted(SNAP.glob("20*.csv"))
    if not files:
        return
    d = pd.read_csv(files[-1])
    d = d[(d.ts == d.ts.max()) & (d.flag == True)]
    seen = pd.read_csv(SEEN) if SEEN.exists() else pd.DataFrame(columns=["key", "player", "source"])
    ids = set(zip(seen.key, seen.player, seen.source))
    new = d[[(k, p, s) not in ids for k, p, s in zip(d.key, d.player, d.source)]]
    if new.empty:
        return
    start = pd.to_datetime(new.start, utc=True).dt.tz_convert("America/Denver").dt.strftime("%a %-I:%M%p MT")
    lines = ["**PAPER ONLY. Log it, don't bet it (Phase 2).**", ""]
    for r, st in zip(new.itertuples(), start):
        lines.append(f"- **{r.player} to win** vs {r.opp} | **{r.source.upper()} @ {r.ask:.2f}** "
                     f"(all-in {r.cost:.3f}) | Pinnacle fair {r.pin_fair:.3f} | model {r.p_model:.3f} | "
                     f"start {st}")
    lines += ["", f"Price edge = Pinnacle fair − all-in cost; model edge = model − all-in cost; both ≥ 2¢. "
                  f"Snapshot {d.ts.max()[:16]}Z. Prices may have moved since."]
    print("\n".join(lines))
    pd.concat([seen, new[["key", "player", "source"]]]).to_csv(SEEN, index=False)


if __name__ == "__main__":
    main()
