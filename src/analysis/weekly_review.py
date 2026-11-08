"""Weekly review (analysis only, PAPER): arb scanner deep dive, price-flag near-misses, data quality.

Run: python src/analysis/weekly_review.py  -> prints markdown and writes data/weekly_review.md

Maker-order assumptions (sensitivity only, not a decision): Kalshi maker fee 0.0175*p*(1-p);
Polymarket US maker rebate given as a share of its 0.0695*p*(1-p) taker fee (0% and 25% shown).
A maker leg is "post 1c above the current bid"; nothing here says it would have filled.
"""
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import scorecard  # noqa: E402

US = {"kalshi", "polyus"}
TAKER = {"kalshi": 0.07, "polyus": 0.0695}
K_MAKER = 0.0175


def fee(src, p, maker=False, rebate=0.0):
    if not maker:
        return TAKER[src] * p * (1 - p)
    return K_MAKER * p * (1 - p) if src == "kalshi" else -rebate * TAKER["polyus"] * p * (1 - p)


def mt_hour(ts):
    return pd.to_datetime(ts, utc=True, format="ISO8601").dt.tz_convert("America/Denver").dt.hour


def se(x):
    x = pd.Series(x).dropna()
    return x.std() / np.sqrt(len(x)) if len(x) > 1 else np.nan


def table(df):
    return df.to_markdown(index=False, floatfmt=".3f") if len(df) else "_(none)_"


# ------------------------------------------------------------------ arbs
def levels(snap):
    k = snap[snap.source == "kalshi"][["key", "event"]].drop_duplicates("key")
    k["level"] = np.where(k.event.str.contains("CHALLENGER"), "challenger", "main")
    return dict(zip(k.key, k.level))


def hourly_arbs(lvl):
    files = sorted(glob.glob(str(ROOT / "data/arbs/20*.csv")))
    a = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    a = a[a.src_a.isin(US) & a.src_b.isin(US) & (a.src_a != a.src_b)].copy()
    a["ts"] = pd.to_datetime(a.ts, utc=True, format="ISO8601")
    a["start"] = pd.to_datetime(a.start, utc=True, errors="coerce", format="ISO8601")
    a["phase"] = np.where(a.ts >= a.start, "live/started", "pre-match")
    a["level"] = a.key.map(lvl).fillna("unknown")
    a["fav_venue"] = np.where(a.ask_a >= a.ask_b, a.src_a, a.src_b)
    best = a.sort_values("total").drop_duplicates(["ts", "key"])  # best combo per match per run
    return best


def arb_section(lvl):
    out = ["## Arb scanner deep dive", ""]
    b = hourly_arbs(lvl)
    out.append(f"Hourly snapshots, US venues only (Kalshi + Polymarket US): {len(b)} match-runs, "
               f"{b.key.nunique()} matches.")
    q = b.total.quantile([0.01, 0.05, 0.25, 0.5]).round(4)
    out.append(f"Best all-in total per match-run: p1 {q[0.01]}, p5 {q[0.05]}, p25 {q[0.25]}, median {q[0.5]}.")
    out.append("")
    rows = []
    for name, g in [("all", b)] + [(f"{c}={v}", g) for c in ("phase", "level", "fav_venue")
                                   for v, g in b.groupby(c)]:
        rows.append({"slice": name, "n": len(g), "under_1": int((g.total < 1).sum()),
                     "within_0.5c": int((g.total < 1.005).sum()), "within_1c": int((g.total < 1.01).sum()),
                     "best": g.total.min()})
    out += [table(pd.DataFrame(rows)), ""]
    h = b.assign(h=b.ts.dt.tz_convert("America/Denver").dt.hour)
    th = h.groupby("h").agg(n=("total", "size"), within_1c=("total", lambda x: int((x < 1.01).sum())),
                            best=("total", "min")).reset_index().rename(columns={"h": "hour_MT"})
    out += ["By hour (MT):", "", table(th), ""]

    # 1-minute scanner
    sc = sorted(glob.glob(str(ROOT / "data/arbscan/*_scans.csv")))
    if sc:
        s = pd.concat([pd.read_csv(f) for f in sc], ignore_index=True)
        ar = pd.concat([pd.read_csv(f) for f in glob.glob(str(ROOT / "data/arbscan/*_arbs.csv"))] or [pd.DataFrame()],
                       ignore_index=True)
        lt = pd.concat([pd.read_csv(f) for f in glob.glob(str(ROOT / "data/arbscan/*_lifetimes.csv"))]
                       or [pd.DataFrame()], ignore_index=True)
        out.append(f"1-minute scanner: {len(s)} scans ({s.ts.min()[:16]} to {s.ts.max()[:16]}Z), median "
                   f"{s.matched.median():.0f} matched matches/scan, best {s.best_total.min()}; "
                   f"scans with best < $1.01: {int((s.best_total < 1.01).sum())}, < $1.005: "
                   f"{int((s.best_total < 1.005).sum())}.")
        if len(ar):
            ex = ar[ar.locked >= 1]
            out.append(f"Sub-$1 combo rows: {len(ar)} ({int(ar.live.sum())} live); executable (≥ $1 locked): "
                       f"{len(ex)} rows on {ex.key.nunique()} matches. Rows with zero verified depth: "
                       f"{int((ar['size'] == 0).sum())} (quote moved before the book check).")
        if len(lt):
            if "kind" not in lt:
                lt["kind"] = "any"
            lt["kind"] = lt.kind.fillna("any")
            for kind, g in lt.groupby("kind"):
                lo = g.min_minutes.median() if "min_minutes" in g and g.min_minutes.notna().any() else np.nan
                out.append(f"Lifetimes ({kind}): n={len(g)}, median upper bound {g.minutes.median()} min, "
                           f"lower bound {lo} min.")
        out.append("")

    # maker one leg: post 1c over the bid on venue X for side A, take side B on the other venue
    snap = scorecard.load()
    m = snap[snap.source.isin(US) & snap.bid.notna() & snap.ask.notna()].copy()
    res = []
    for rebate in (0.0, 0.25):
        hits = []
        for (ts, key), g in m.groupby(["ts", "key"]):
            if g.source.nunique() < 2:
                continue
            for r1 in g.itertuples():
                for r2 in g.itertuples():
                    if r1.source == r2.source or scorecard.same(r1.player, r2.player):
                        continue
                    p1 = min(r1.bid + 0.01, r1.ask - 0.01)
                    if p1 <= 0:
                        continue
                    tot = p1 + fee(r1.source, p1, True, rebate) + r2.ask + fee(r2.source, r2.ask)
                    hits.append({"maker": r1.source, "total": tot, "key": key})
        hd = pd.DataFrame(hits)
        if len(hd):
            for v, g in hd.groupby("maker"):
                res.append({"polyus_rebate": f"{int(rebate * 100)}%", "maker_venue": v, "pairs": len(g),
                            "under_1": int((g.total < 1).sum()), "under_0.99": int((g.total < 0.99).sum()),
                            "median_total": g.total.median()})
    out += ["Maker on one leg (post bid+1c, take the other venue; hourly snapshots, fills NOT modeled):", "",
            table(pd.DataFrame(res)), ""]
    return out, snap


# ------------------------------------------------------------------ price flags
def flag_section(snap, lvl):
    out = ["## Price-flag near-misses (price edge 0–2c) and CLV slices", ""]
    pin = snap[snap.source == "pinnacle"].sort_values("ts")
    mk = snap[snap.source.isin(US | {"poly"}) & snap.pin_fair.notna() & snap.cost.notna()].copy()
    mk = mk.sort_values("ts").drop_duplicates(["key", "player", "source"])  # first sighting
    close = {}
    for r in pin.itertuples():
        if pd.notna(r.start) and r.ts < r.start:
            close[(r.key, r.player)] = r.fair  # last pre-start pull wins (sorted)

    def cl(r):
        for (k, p), v in close.items():
            if k == r.key and scorecard.same(p, r.player):
                return v
        return np.nan
    mk["close"] = [cl(r) for r in mk.itertuples()]
    mk["clv"] = mk.close - mk.cost
    mk["level"] = mk.key.map(lvl).fillna("unknown")
    mk["hrs"] = (mk.start - mk.ts).dt.total_seconds() / 3600
    mk["hrs_b"] = pd.cut(mk.hrs, [-1e9, 0, 3, 12, 1e9], labels=["started", "0-3h", "3-12h", "12h+"])
    mk["role"] = np.where(mk.pin_fair >= 0.5, "favorite", "underdog")
    near = mk[(mk.price_edge >= 0) & (mk.price_edge < 0.02)]
    out.append(f"First-sighting sides with Pinnacle fair: {len(mk)} ({mk.key.nunique()} matches); near-misses "
               f"(edge 0–2c): {len(near)}, of which US venues: {int(near.source.isin(US).sum())}.")
    out.append("")
    rows, n_tested = [], 0
    for col in ("source", "tour", "level", "hrs_b", "role"):
        for v, g in mk.groupby(col, observed=True):
            g = g.dropna(subset=["clv"])
            if len(g) < 5:
                continue
            n_tested += 1
            pm = g.groupby("key").clv.mean()  # per-match clustering
            rows.append({"slice": f"{col}={v}", "sides": len(g), "matches": len(pm),
                         "avg_clv_c": 100 * pm.mean(), "se_c": 100 * se(pm),
                         "beat_close_%": 100 * (g.clv > 0).mean(),
                         "near_miss": int(((g.price_edge >= 0) & (g.price_edge < 0.02)).sum())})
    out += [table(pd.DataFrame(rows)), "",
            f"Slices tested: {n_tested}. With that many, expect ~{n_tested * 0.025:.1f} to look 2 SE good by chance.", ""]
    return out, mk


# ------------------------------------------------------------------ data quality
def dq_section(snap, mk):
    out = ["## Data quality", ""]
    last = snap[snap.ts == snap.ts.max()]
    by = last[last.source.isin(US | {"poly", "pinnacle"})].groupby("source").key.apply(set)
    if "kalshi" in by and "polyus" in by:
        k_only, p_only = by["kalshi"] - by["polyus"], by["polyus"] - by["kalshi"]
        out.append(f"Latest snapshot: Kalshi {len(by['kalshi'])} matches, Polymarket US {len(by['polyus'])}, "
                   f"matched {len(by['kalshi'] & by['polyus'])}; Kalshi-only {len(k_only)}, Polymarket-US-only "
                   f"{len(p_only)}.")
        # possible name mismatches: same date, one shared surname token
        tok = lambda k: set(k.replace(" v ", " ").split())
        sus = [(a, b) for a in k_only for b in p_only if len(tok(a) & tok(b)) == 1]
        out.append(f"Possible unmatched name pairs (one shared surname): {len(sus)}"
                   + (": " + "; ".join(f"{a} ~ {b}" for a, b in sus[:8]) if sus else ""))
    miss = snap[snap.source.isin(US)]
    out.append(f"US-venue rows missing ask: {int(miss.ask.isna().sum())} of {len(miss)}; missing start time: "
               f"{int(miss.start.isna().sum())}.")
    for src in ("kalshi", "polyus"):
        st = snap[(snap.source == src) & snap.start.notna()].groupby("key").start.agg(["min", "max"])
        drift = (st["max"] - st["min"]).dt.total_seconds() / 3600
        out.append(f"{src}: start time moved > 2h between snapshots for {int((drift > 2).sum())} of {len(st)} "
                   "matches (order-of-play changes; 'hours before start' uses the first-sighting start).")
    pk = snap[snap.source == "pinnacle"].copy()
    if "book_update" in pk:
        age = (pk.ts - pd.to_datetime(pk.book_update, utc=True, errors="coerce")).dt.total_seconds() / 60
        out.append(f"Pinnacle quote age at pull: median {age.median():.0f} min, >60 min: {int((age > 60).sum())}.")
    out.append("")
    return out


def main():
    snap0 = scorecard.load()
    lvl = levels(snap0)
    a, snap = arb_section(lvl)
    f, mk = flag_section(snap, lvl)
    d = dq_section(snap, mk)
    txt = "\n".join([f"# Weekly review ({pd.Timestamp.now(tz='America/Denver'):%a %b %d %Y})", ""] + a + f + d)
    (ROOT / "data/weekly_review.md").write_text(txt)
    print(txt)


if __name__ == "__main__":
    main()
