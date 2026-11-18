"""The one report that says where the arb test stands. Writes data/gate.md (read this) and data/gate.json
(read by live.py: live trading is impossible unless "pass" is true).

Only FRESH data counts: rows with fresh == True, logged since START, when every Polymarket US book read
became uncached. Everything before that compared live Kalshi books with Polymarket US books up to 30s old
and is not evidence (see README, Nov 14).

THE GATE (Remick's Nov 10 definition, unchanged, re-run on fresh data through END):
  arbs a ready bot is expected to profit from (both legs still there at +1s at the quoted prices, >= $1 at
  his bankroll), counted from the scanner (gate_ok) or the paper bot (both legs filled, alive at +1s, >= $1),
  on >= 10 occasions (one per match per UTC day) across >= 5 UTC days,
  AND the paper bot's simulated fills net positive, AND the Polymarket US feed stayed fresh.
"""
import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
START = pd.Timestamp("2026-11-14T21:20:00Z")
END = pd.Timestamp("2026-11-22T00:00:00Z")
NEED_OCC, NEED_DAYS = 10, 5


def load(pattern):
    fs = sorted(glob.glob(str(ROOT / pattern)))
    out = []
    for f in fs:
        try:
            out.append(pd.read_csv(f, low_memory=False))
        except Exception:
            pass
    if not out:
        return pd.DataFrame()
    d = pd.concat(out, ignore_index=True)
    if "ts" not in d:
        return pd.DataFrame()
    d["t"] = pd.to_datetime(d.ts, utc=True, format="ISO8601", errors="coerce")
    d = d[(d.t >= START) & (d.t < END)].copy()
    d["day"] = d.t.dt.strftime("%Y-%m-%d")
    return d


def num(d, c):
    return pd.to_numeric(d[c], errors="coerce") if len(d) and c in d else pd.Series(dtype=float)


def truthy(d, c):
    return d[c].astype(str).str.lower().eq("true") if len(d) and c in d else pd.Series(False, index=d.index)


def main():
    now = pd.Timestamp.now(tz="UTC")
    arbs, fires = load("data/arbscan/2026-11-*_arbs.csv"), load("data/bot/*_fires.csv")
    maker, cyc, scans = load("data/bot/*_maker.csv"), load("data/bot/*_cycles.csv"), load("data/arbscan/2026-11-*_scans.csv")

    # 1) scanner: gate_ok on fresh books, one occasion per match per day
    g = arbs[truthy(arbs, "fresh") & truthy(arbs, "gate_ok")] if len(arbs) else arbs
    g = g.sort_values("t").drop_duplicates(["key", "day"]) if len(g) else g
    occ_profit = float(num(g, "bankroll_profit").sum()) if len(g) else 0.0

    # 2) paper bot on fresh books
    f = fires[truthy(fires, "fresh")] if len(fires) else fires
    traded = f[(num(f, "filled_a") > 0) | (num(f, "filled_b") > 0)] if len(f) else f
    # The same definition measured by the bot (it reads fresh books for every match; the scanner detects from
    # Kalshi's market list, which lags up to 15s and can miss a real arb): both legs fully filled one round
    # trip later, still fillable at +1s, and >= $1 locked. An occasion is one match on one UTC day, from
    # either source.
    bq = f[(num(f, "filled_a") >= num(f, "shares")) & (num(f, "filled_b") >= num(f, "shares"))
           & (num(f, "sim_profit") >= 1.0) & truthy(f, "alive_1s")] if len(f) else f
    occ_keys = set(zip(g.key, g.day)) if len(g) else set()
    occ_keys |= set(zip(bq.key, bq.day)) if len(bq) else set()
    occ, days = len(occ_keys), len({d for _, d in occ_keys})
    sim = float(num(traded, "sim_profit").sum()) if len(traded) else 0.0
    short = int((num(traded, "filled_a") != num(traded, "filled_b")).sum()) if len(traded) else 0
    alive1 = truthy(f, "alive_1s").mean() if len(f) and "alive_1s" in f else float("nan")

    # 3) feed freshness
    reads = float(num(cyc, "poly_reads").sum() + num(scans, "poly_reads").sum())
    stale = float(num(cyc, "poly_stale").sum() + num(scans, "poly_stale").sum())
    stale_pct = 100 * stale / reads if reads else 0.0
    max_age = float(max(num(cyc, "poly_max_age").max() if len(cyc) and "poly_max_age" in cyc else 0,
                        num(scans, "poly_max_age").max() if len(scans) and "poly_max_age" in scans else 0) or 0)
    unknown = float(num(cyc, "poly_unknown_age").sum())
    bot_reads = float(num(cyc, "poly_reads").sum())
    unverified = bool(bot_reads and unknown > 0.5 * bot_reads)   # no Last-Modified header: freshness can't be checked
    feed_ok = stale_pct < 5 and not unverified
    # coverage: could the bot actually see? (Polymarket US rate-limits book reads; lists can fail)
    cands, no_book = float(num(cyc, "cands").sum()), float(num(cyc, "no_book").sum())
    limited = float(num(cyc, "poly_limited").sum() + num(scans, "poly_limited").sum())
    list_fail, cycles = float(num(cyc, "list_fail").sum()), float(num(cyc, "cycles").sum())
    checks, mism = float(num(cyc, "list_checks").sum()), float(num(cyc, "list_mismatch").sum())
    blind = bool(cands and no_book > 0.3 * cands) or bool(cycles and list_fail > 0.1 * cycles)

    # 4) maker-quote paper test
    mp = num(maker, "pnl").dropna()
    m_n, m_sum = len(mp), float(mp.sum()) if len(mp) else 0.0
    m_mean = float(mp.mean()) if len(mp) else float("nan")
    m_se = float(mp.std() / np.sqrt(len(mp))) if len(mp) > 1 else float("nan")
    maker_edge = bool(m_n >= 30 and m_mean - 2 * m_se > 0)

    passed = bool(occ >= NEED_OCC and days >= NEED_DAYS and sim > 0 and feed_ok)
    status = "PASSED" if passed else ("RUNNING" if now < END else "FAILED")
    json.dump({"pass": passed, "status": status, "as_of": now.isoformat(timespec="minutes"),
               "occasions": occ, "days": days, "bot_traded": len(traded), "bot_sim_profit": round(sim, 2),
               "poly_stale_pct": round(stale_pct, 2), "maker_fills": m_n, "maker_pnl": round(m_sum, 2),
               "maker_edge": maker_edge}, open(ROOT / "data" / "gate.json", "w"), indent=1)

    verdict = {
        "PASSED": "**PASSED on fresh data.** Next step is Remick's: confirm he wants live trading at $25 per venue per "
                  "arb. Nobody else turns it on.",
        "RUNNING": f"**NOT PASSED YET** ({occ}/{NEED_OCC} occasions, {days}/{NEED_DAYS} days). Test ends "
                   f"{END:%b %-d} 00:00 UTC. Live trading is off and stays off.",
        "FAILED": "**FAILED.** Cross-venue taker arbitrage between Kalshi and Polymarket US is closed as a strategy: "
                  "on fresh data the gaps aren't there. Live trading stays off. Tell Remick plainly; unless the maker "
                  "test below shows an edge, the honest recommendation is to withdraw the money.",
    }[status]
    L = [f"# Arb test status ({now.tz_convert('America/Denver'):%a %b %-d %-I:%M%p} MT)", "",
         f"Fresh data only, since {START:%b %-d %H:%M} UTC. " + verdict, "",
         "| Check | Now | Needed |", "|---|---|---|",
         f"| Arbs a ready bot would profit from (occasions: one per match per day) | {occ} | {NEED_OCC} |",
         f"| ...on different UTC days | {days} | {NEED_DAYS} |",
         f"| ...found by the scanner / by the paper bot | {len(g)} / {len(bq)} | - |",
         f"| ...scanner total at the $690 bankroll | ${occ_profit:.2f} | - |",
         f"| Paper bot: fires / traded / one leg short | {len(f)} / {len(traded)} / {short} | - |",
         f"| Paper bot: simulated profit on traded fires | ${sim:+.2f} | > $0 |",
         f"| Paper bot: fires still fillable 1s later | {'n/a' if alive1 != alive1 else f'{alive1:.0%}'} | - |",
         f"| Polymarket US reads refused as stale | {stale_pct:.1f}% (oldest {max_age:.0f}s) | < 5% |", ""]
    L += [f"Coverage: {int(cands)} candidate checks (list prices showed an arb), {int(no_book)} got no Polymarket US "
          f"book; {int(limited)} rate-limit hits; {int(list_fail)} failed list refreshes in {int(cycles):,} cycles; "
          f"list vs book disagreed on {int(mism)} of {int(checks)} checks.", ""]
    if blind:
        L += ["**COVERAGE WARNING: the bot is missing too many Polymarket US reads to trust a 'no arbs' result. "
              "Run the feed-diagnostics workflow (diag.yml) and fix the read budget in arbscan.py.**", ""]
    if checks >= 10 and mism > 0.3 * checks:
        # Not a data warning: candidates are picked BECAUSE the list shows an arb, so at those moments the list
        # often disagrees with the book. Every fire is re-decided on a fresh, age-checked Polymarket US book,
        # so this costs detections (recall), not accuracy.
        L += [f"Note: at candidate moments the Polymarket US list disagreed with its book {mism / checks:.0%} of the "
              "time. Every fire is re-checked on the real book, so this means missed detections, not false fires.", ""]
    if unverified:
        L += ["**DATA WARNING: Polymarket US stopped sending the header the freshness check uses, so freshness is "
              "UNVERIFIED and nothing can pass. Fix arbscan.polyus_book before trusting any arb.**", ""]
    if len(cyc):
        mins = len(cyc)
        sub1 = int(num(cyc, "sub1_cycles").sum()) if "sub1_cycles" in cyc else 0
        be = num(cyc, "best_exec")
        L += [f"Bot coverage: {mins:,} minutes watched. Cycles (2s each) where some pair cost under $1: **{sub1:,}**. "
              f"Best a single fire would have netted: **${be.max():.2f}**." if len(be.dropna()) else
              f"Bot coverage: {mins:,} minutes watched. Cycles where some pair cost under $1: **{sub1:,}**.", ""]
    L += ["## Maker test (rest a bid on one venue, hedge on the other if it fills)", "",
          f"Fills: **{m_n}** · total **${m_sum:+.2f}** · per fill "
          + (f"${m_mean:+.2f} ± {m_se:.2f}" if m_n > 1 else "n/a") + ". "
          + ("**Shows an edge** (30+ fills, mean above zero by 2 standard errors): worth a proposal to Remick. Paper only."
             if maker_edge else "No edge shown (needs 30+ fills with the mean above zero by 2 standard errors)."), ""]
    if len(maker) and m_n:
        mk = maker.assign(pnl=num(maker, "pnl"), venue=maker.maker.str.split(":").str[0])
        t = mk.groupby(["venue", "live"]).pnl.agg(fills="count", total="sum", mean="mean").round(2).reset_index()
        L += [t.to_markdown(index=False), ""]
    by = {}
    for name, d, col in (("scanner gate_ok", g, None), ("bot fires", f, None), ("bot traded", traded, None),
                         ("maker fills", maker if m_n else maker.iloc[0:0], None)):
        if len(d):
            by[name] = d.groupby("day").size()
    if len(traded):
        by["bot sim $"] = traded.assign(v=num(traded, "sim_profit")).groupby("day").v.sum().round(2)
    if m_n:
        by["maker $"] = maker.assign(v=num(maker, "pnl")).groupby("day").v.sum().round(2)
    if by:
        L += ["## By UTC day", "", pd.DataFrame(by).fillna(0).reset_index().rename(columns={"index": "day"}).to_markdown(index=False), ""]
    if len(g):
        cols = [c for c in ["ts", "key", "live", "total", "size_1s", "locked_1s", "bankroll_profit"] if c in g]
        L += ["## Scanner arbs that count", "", g[cols].tail(20).to_markdown(index=False), ""]
    (ROOT / "data" / "gate.md").write_text("\n".join(L) + "\n")
    return status


if __name__ == "__main__":
    print(main())
    print((ROOT / "data" / "gate.md").read_text())
