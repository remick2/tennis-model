"""Weekly review on FRESH data only (paper; analysis, changes no decision).

Only rows with fresh=True logged since Nov 14 21:20 UTC count (older rows used Polymarket US books up to 30s
stale and are not evidence of anything). Prints markdown.

Run: python3 src/analysis/fresh_week.py
"""
import glob
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
START = pd.Timestamp("2026-11-14T21:20:00Z")
TOO_GOOD = 0.03  # sanity rule: an edge above 3c per $1 is a data bug until two raw sources agree


def load(kind):
    fs = sorted(glob.glob(str(ROOT / f"data/bot/*_{kind}.csv")))
    if not fs:
        return pd.DataFrame()
    d = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
    d["ts"] = pd.to_datetime(d.ts, utc=True, format="ISO8601")
    d = d[d.ts >= START]
    if "fresh" in d:
        d = d[d.fresh.astype(str) == "True"]
    return d


def se(x):
    x = pd.Series(x).dropna()
    return x.std() / np.sqrt(len(x)) if len(x) > 1 else np.nan


def main():
    out = ["# Fresh-data weekly review (paper only)", ""]
    c = load("cycles")
    if len(c):
        s = c[["cycles", "sub1_cycles", "cands", "no_book", "list_checks", "list_mismatch", "poly_stale", "poly_limited"]].sum()
        out += ["## Bot cycles", "",
                f"- 2s cycles: {int(s.cycles):,}; with some pair under $1: {int(s.sub1_cycles):,} "
                f"({s.sub1_cycles / max(s.cycles, 1):.1%})",
                f"- candidate checks: {int(s.cands)}, no Polymarket US book: {int(s.no_book)}",
                f"- two-source check (Polymarket US list vs uncached book, >0.5c apart): "
                f"{int(s.list_mismatch)} of {int(s.list_checks)} ({s.list_mismatch / max(s.list_checks, 1):.0%})",
                f"- best single fire would have netted: ${c.best_exec.max():.2f}", ""]
    f = load("fires")
    if len(f):
        f["edge"] = 1 - f.total
        f["too_good"] = f.edge > TOO_GOOD
        for col in ("alive_1s", "alive_3s"):
            f[col] = f[col].astype(str) == "True"
        out += ["## Paper fires", "",
                f"- fires {len(f)}, alive at +1s {f.alive_1s.sum()}, at +3s {f.alive_3s.sum()}",
                f"- simulated profit ${f.sim_profit.sum():.2f} (mean ${f.sim_profit.mean():.2f} ± {se(f.sim_profit):.2f})",
                f"- fires with edge > 3c/$1 (suspect until two raw sources agree): {f.too_good.sum()} "
                f"worth ${f.loc[f.too_good, 'sim_profit'].sum():.2f}; the rest: ${f.loc[~f.too_good, 'sim_profit'].sum():.2f}",
                f"- matches firing 2+ times: {', '.join(f'{k} ({n})' for k, n in f.key.value_counts().items() if n > 1) or 'none'}",
                "", f[["ts", "key", "live", "shares", "total", "sim_profit", "alive_1s", "alive_3s", "too_good"]]
                .to_markdown(index=False, floatfmt=".4f"), ""]
    m = load("maker")
    if len(m):
        m["phase"] = np.where(m.live.astype(str) == "True", "live", "pre-match")
        m["venue"] = m.maker.str.split(":").str[0]
        g = (m.groupby(["venue", "phase", "at_touch"]).pnl
             .agg(fills="size", total="sum", mean="mean", se=se).reset_index())
        r = (m.assign(rested=pd.cut(m.rested_secs, [0, 2, 5, 60, 1e9], labels=["<=2s", "2-5s", "5-60s", ">60s"]))
             .groupby("rested", observed=True).pnl.agg(fills="size", mean="mean").reset_index())
        out += ["## Maker test", "", f"- fills {len(m)}, total ${m.pnl.sum():.2f}, per fill ${m.pnl.mean():.2f} ± {se(m.pnl):.2f}",
                "", g.to_markdown(index=False, floatfmt=".2f"), "", r.to_markdown(index=False, floatfmt=".2f"), ""]
    print("\n".join(out))


if __name__ == "__main__":
    main()
