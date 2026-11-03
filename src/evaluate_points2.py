"""Point model v2: adds a spread multiplier (kappa), day-to-day form noise (sig_rel) and a
serve-level shift (delta). Tuned on 2022-24 totals/margins, scored on 2025-26.

Point probs per match:  c = (la+lb)/2 + delta,  d = kappa*(la-lb)/2,  pa = sig(c+d), pb = sig(c-d)
then averaged over form noise.
"""
import itertools
import json
import sys
import warnings

import numpy as np
import pandas as pd

import backtest as b
import elo
import pointmodel as pm
from evaluate_points import link, rps
from load import MAIN_LEVELS, games

warnings.filterwarnings("ignore")
DATA = b.DATA
LR, LR_SURF = 0.12, 0.1


def adj(pa, pb, kappa, delta):
    la, lb = pm.logit(pa), pm.logit(pb)
    c, d = (la + lb) / 2 + delta, kappa * (la - lb) / 2
    return pm.sig(c + d), pm.sig(c - d)


def supports(bo):
    return (range(12, 66) if bo == 5 else range(12, 40)), range(-30, 31)


def score_rows(rows, kappa, sig_rel, delta):
    out = []
    for pa, pb, bo, sc in rows:
        g = games(sc)
        a, c = adj(pa, pb, kappa, delta)
        p, td, md = pm.match_dist_mix(a, c, bo, sig_rel)
        st, sm = supports(bo)
        out.append((pm.logit(p) if p < 1 else 9, -np.log(max(p, 1e-9)),
                    rps(td, g[0] + g[1], st), rps(md, g[0] - g[1], sm),
                    sum(k * v for k, v in td.items()) - (g[0] + g[1])))
    o = np.array(out)
    return {"ll_win": o[:, 1].mean(), "rps_total": o[:, 2].mean(), "rps_margin": o[:, 3].mean(),
            "bias_total": o[:, 4].mean()}


def market_shift_mix(pa, pb, bo, target, sig_rel):
    la, lb = pm.logit(pa), pm.logit(pb)
    lo, hi = -1.5, 1.5
    for _ in range(12):
        mid = (lo + hi) / 2
        p = pm.match_dist_mix(pm.sig(la + mid), pm.sig(lb - mid), bo, sig_rel)[0]
        lo, hi = (mid, hi) if p < target else (lo, mid)
    d = (lo + hi) / 2
    return pm.sig(la + d), pm.sig(lb - d)


def main(tour):
    stream, odds = elo.build_stream(tour)
    sk = pm.run_skills(stream, lr=LR, lr_surf=LR_SURF)
    assert sk[["s_w", "r_w"]].notna().all().all(), "NaN skills"
    v = sk[(sk.date >= "2022-01-01") & (sk.date < "2025-01-01") & (sk.status == "done")
           & sk.level.isin(MAIN_LEVELS) & (sk.npt_w > 800) & (sk.npt_l > 800)]
    v = v[[games(s) is not None for s in v.score]].sample(1500, random_state=0)
    pa, pb = pm.point_probs(v)
    rows = list(zip(pa, pb, v.best_of.fillna(3).astype(int), v.score))

    # naive baseline on the tuning set (distribution by best_of from all 2022-24 main rows)
    allv = sk[(sk.date >= "2022-01-01") & (sk.date < "2025-01-01") & (sk.status == "done") & sk.level.isin(MAIN_LEVELS)]
    naive = {}
    for bo, g in allv.groupby("best_of"):
        gg = [games(s) for s in g.score]; gg = [x for x in gg if x]
        naive[int(bo)] = pd.Series([x[0] + x[1] for x in gg]).value_counts(normalize=True).to_dict()
        m = pd.Series([x[0] - x[1] for x in gg])
        naive[f"m{int(bo)}"] = pd.concat([m, -m]).value_counts(normalize=True).to_dict()

    grid = []
    for kappa, sig_rel, delta in itertools.product([1.0, 1.4, 1.8], [0.0, 0.2, 0.35, 0.5], [-0.1, 0.0, 0.1]):
        r = score_rows(rows, kappa, sig_rel, delta)
        r.update(kappa=kappa, sig_rel=sig_rel, delta=delta, obj=r["rps_total"] + r["rps_margin"])
        grid.append(r); print(tour, {k: round(x, 4) for k, x in r.items()}, flush=True)
    G = pd.DataFrame(grid)
    best = G.loc[G.obj.idxmin()]
    kappa, sig_rel, delta = float(best.kappa), float(best.sig_rel), float(best.delta)

    # ---------- test 2025-26
    idx = link(stream, odds)
    t = odds.loc[idx.index].copy(); t["sidx"] = idx.values
    t = b.test_set(t.assign(p_model=1.0))
    t = t[[games(s) is not None for s in t.score]]
    s = sk.loc[t.sidx]
    pa, pb = pm.point_probs(s)
    res = []
    for (a0, b0, bo, sc, pc) in zip(pa, pb, t.best_of.fillna(3).astype(int), t.score, t.p_close):
        g = games(sc); tot, mar = g[0] + g[1], g[0] - g[1]
        st, sm = supports(bo)
        a, c = adj(a0, b0, kappa, delta)
        p, td, md = pm.match_dist_mix(a, c, bo, sig_rel)
        ma, mb = market_shift_mix(a, c, bo, pc, sig_rel)
        _, tdm, mdm = pm.match_dist_mix(ma, mb, bo, sig_rel)
        line = 22.5 if bo == 3 else 38.5
        res.append({"best_of": bo, "total": tot, "p_win": p, "p_close": pc,
                    "rps_t_model": rps(td, tot, st), "rps_t_mkt": rps(tdm, tot, st), "rps_t_naive": rps(naive[bo], tot, st),
                    "rps_m_model": rps(md, mar, sm), "rps_m_mkt": rps(mdm, mar, sm), "rps_m_naive": rps(naive[f"m{bo}"], mar, sm),
                    "pred_t_model": sum(k * x for k, x in td.items()), "pred_t_mkt": sum(k * x for k, x in tdm.items()),
                    "pover_model": sum(x for k, x in td.items() if k > line),
                    "pover_mkt": sum(x for k, x in tdm.items() if k > line),
                    "pover_naive": sum(x for k, x in naive[bo].items() if k > line),
                    "over": float(tot > line)})
    R = pd.DataFrame(res)
    R["tour"] = tour
    R.to_parquet(f"{DATA}/points2_test_{tour}.parquet")
    summ = R.groupby("best_of").agg(
        n=("total", "size"), avg_total=("total", "mean"),
        pred_model=("pred_t_model", "mean"), pred_mkt=("pred_t_mkt", "mean"),
        rps_total_model=("rps_t_model", "mean"), rps_total_mkt=("rps_t_mkt", "mean"), rps_total_naive=("rps_t_naive", "mean"),
        rps_margin_model=("rps_m_model", "mean"), rps_margin_mkt=("rps_m_mkt", "mean"), rps_margin_naive=("rps_m_naive", "mean"))
    for nm in ("model", "mkt", "naive"):
        summ[f"brier_over_{nm}"] = R.groupby("best_of").apply(lambda d: ((d[f"pover_{nm}"] - d.over) ** 2).mean())
    summ["ll_win_point"] = R.groupby("best_of").apply(lambda d: b.ll(d.p_win).mean())
    summ["ll_win_market"] = R.groupby("best_of").apply(lambda d: b.ll(d.p_close).mean())
    out = {"tour": tour, "params": {"kappa": kappa, "sig_rel": sig_rel, "delta": delta},
           "tune_best": best.to_dict()}
    json.dump(out, open(f"{DATA}/points2_{tour}.json", "w"), indent=1, default=float)
    print(json.dumps(out, indent=1, default=float))
    print(summ.round(4).T.to_string())


if __name__ == "__main__":
    main(sys.argv[1])
