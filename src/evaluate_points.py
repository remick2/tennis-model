"""Tune the point model on 2022-24, then score 2025-26:
  - match winner: point model vs Elo vs blend vs closing market
  - total games + game margin: point model vs naive baseline vs 'market-implied' point model
    (serve probs shifted until the model's win prob equals the closing moneyline)
No historical totals/handicap ODDS exist in our data, so totals are scored on accuracy only.
"""
import itertools
import json
import warnings

import numpy as np
import pandas as pd

import backtest as b
import elo
import pointmodel as pm
from load import MAIN_LEVELS, SACKMANN_END, games

warnings.filterwarnings("ignore")
DATA = b.DATA
SWITCH = pd.Timestamp(str(SACKMANN_END))


def point_deviance(df):
    """Binomial log-loss per serve point on rows with stats (tuning target)."""
    d = df[(df.w_svpt > 0) & (df.l_svpt > 0) & (df.status == "done")]
    pw, pl = pm.point_probs(d)
    ll = -(d.w_spw * np.log(pw) + (d.w_svpt - d.w_spw) * np.log(1 - pw)
           + d.l_spw * np.log(pl) + (d.l_svpt - d.l_spw) * np.log(1 - pl))
    return float(ll.sum() / (d.w_svpt.sum() + d.l_svpt.sum()))


def link(stream, odds):
    """For each odds row, the index of the same match in the stream."""
    post = odds[odds.date >= SWITCH].reset_index().merge(
        stream[stream.src == "odds"].reset_index()[["index", "match_id"]].rename(columns={"index": "sidx"}),
        on="match_id")
    pre = odds[odds.date < SWITCH].reset_index()
    sk = stream[stream.src == "sack"].reset_index()[["index", "w_id", "l_id", "date"]].rename(
        columns={"index": "sidx", "date": "sdate"})
    m = pre.merge(sk, on=["w_id", "l_id"])
    m = m[(m.date - m.sdate).abs() <= pd.Timedelta(days=8)].sort_values("index").drop_duplicates("index")
    return pd.concat([m[["index", "sidx"]], post[["index", "sidx"]]]).set_index("index").sidx


def rps(dist, actual, support):
    """Ranked probability score over an ordered support (lower = better)."""
    cdf = np.cumsum([dist.get(k, 0.0) for k in support])
    obs = np.array([1.0 if k >= actual else 0.0 for k in support])
    return float(np.mean((cdf - obs) ** 2))


def market_shift(pa, pb, bo, target):
    """Shift serve probs (A up, B down, in logit space) until P(A wins) == target."""
    la, lb = pm.logit(pa), pm.logit(pb)
    lo, hi = -1.5, 1.5
    for _ in range(18):
        mid = (lo + hi) / 2
        p = pm.match_dist_fast(pm.sig(la + mid), pm.sig(lb - mid), bo)[0]
        lo, hi = (mid, hi) if p < target else (lo, mid)
    d = (lo + hi) / 2
    return pm.sig(la + d), pm.sig(lb - d)


def main():
    out = {"tuning": {}}
    test_rows = []
    for tour in ("atp", "wta"):
        stream, odds = elo.build_stream(tour)
        # ---------- tune learning rates on 2022-24 point deviance
        best = None
        for lr, lrs in itertools.product([0.03, 0.06, 0.12], [0.0, 0.05, 0.1]):
            sk = pm.run_skills(stream, lr=lr, lr_surf=lrs)
            v = sk[(sk.date >= "2022-01-01") & (sk.date < "2025-01-01")]
            dev = point_deviance(v)
            print(tour, lr, lrs, round(dev, 5), flush=True)
            if best is None or dev < best[0]:
                best = (dev, lr, lrs, sk)
        dev, lr, lrs, sk = best
        out["tuning"][tour] = {"lr": lr, "lr_surf": lrs, "point_dev": dev}

        # ---------- Elo (best variant) on the same stream, same row order
        ep, _, _ = elo.run(stream, mov=True, level_k=True, layoff=True)
        eprm = b.tune(ep)
        sk["p_elo"] = elo.prob(ep, eprm["w_blend"], eprm["scale"])
        sk["n_w_elo"], sk["n_l_elo"] = ep.n_w, ep.n_l

        # ---------- point-model win prob for tuning window + blend weight
        def add_pwin(df):
            pw, pl = pm.point_probs(df)
            df = df.copy()
            df["pa"], df["pb"] = pw, pl
            df["p_pt"] = [pm.match_dist_fast(a, c, bo)[0] for a, c, bo in zip(pw, pl, df.best_of.fillna(3))]
            return df
        v = sk[(sk.date >= "2022-01-01") & (sk.date < "2025-01-01") & (sk.status == "done")
               & sk.level.isin(MAIN_LEVELS) & (sk.n_w_elo >= 10) & (sk.n_l_elo >= 10)]
        v = add_pwin(v)
        best_w = min(np.arange(0, 1.01, 0.1),
                     key=lambda w: b.ll(pm.sig(w * pm.logit(v.p_pt) + (1 - w) * pm.logit(v.p_elo))).mean())
        out["tuning"][tour].update({"blend_w_point": float(best_w),
                                    "tune_ll_point": float(b.ll(v.p_pt).mean()),
                                    "tune_ll_elo": float(b.ll(v.p_elo).mean())})
        # naive totals baseline: empirical distribution by best_of, from 2022-24 main tour
        naive = {}
        for bo, g in v.groupby("best_of"):
            tg = [games(s) for s in g.score]
            tg = pd.Series([x[0] + x[1] for x in tg if x])
            naive[int(bo)] = (tg.value_counts(normalize=True).to_dict())
            mg = pd.Series([x[0] - x[1] for x in (games(s) for s in g.score) if x])
            # margin from winner's side; symmetrise for an orientation-free baseline
            naive[f"m{int(bo)}"] = pd.concat([mg, -mg]).value_counts(normalize=True).to_dict()

        # ---------- test rows
        idx = link(stream, odds)
        t = odds.loc[idx.index].copy()
        t["sidx"] = idx.values
        t = b.test_set(t.assign(p_model=1.0))  # same filters as the Elo backtest
        s = sk.loc[t.sidx]
        s = add_pwin(s)
        for c in ("pa", "pb", "p_pt", "p_elo"):
            t[c] = s[c].values
        t["p_blend"] = pm.sig(best_w * pm.logit(t.p_pt) + (1 - best_w) * pm.logit(t.p_elo))
        t["naive"] = [naive for _ in range(len(t))]
        test_rows.append(t)

    t = pd.concat(test_rows, ignore_index=True)
    # ---------- winner metrics
    win = {}
    for tour, g in t.groupby("tour"):
        win[tour] = {k: float(b.ll(g[c]).mean()) for k, c in
                     [("point", "p_pt"), ("elo", "p_elo"), ("blend", "p_blend"), ("market", "p_close")]}
        win[tour]["n"] = len(g)
    out["winner_logloss"] = win

    # ---------- totals + margins (complete matches only)
    res = []
    for r in t.itertuples():
        g = games(r.score)
        if not g:
            continue
        bo = int(r.best_of)
        total, margin = g[0] + g[1], g[0] - g[1]
        supp_t = range(12, 66) if bo == 5 else range(12, 40)
        supp_m = range(-30, 31)
        _, td, md = pm.match_dist_fast(r.pa, r.pb, bo)
        ma, mb = market_shift(r.pa, r.pb, bo, r.p_close)
        _, tdm, mdm = pm.match_dist_fast(ma, mb, bo)
        nt, nm = r.naive[bo], r.naive[f"m{bo}"]
        mean = lambda d: sum(k * v for k, v in d.items())
        res.append({
            "tour": r.tour, "best_of": bo, "total": total,
            "rps_t_model": rps(td, total, supp_t), "rps_t_mkt": rps(tdm, total, supp_t), "rps_t_naive": rps(nt, total, supp_t),
            "rps_m_model": rps(md, margin, supp_m), "rps_m_mkt": rps(mdm, margin, supp_m), "rps_m_naive": rps(nm, margin, supp_m),
            "exp_t_model": mean(td), "exp_t_mkt": mean(tdm), "exp_t_naive": mean(nt),
            "pover_model": sum(v for k, v in td.items() if k > (22.5 if bo == 3 else 38.5)),
            "pover_mkt": sum(v for k, v in tdm.items() if k > (22.5 if bo == 3 else 38.5)),
        })
    R = pd.DataFrame(res)
    R["over"] = (R.total > np.where(R.best_of == 3, 22.5, 38.5)).astype(float)
    summ = R.groupby(["tour", "best_of"]).agg(
        n=("total", "size"),
        rps_total_model=("rps_t_model", "mean"), rps_total_mkt=("rps_t_mkt", "mean"), rps_total_naive=("rps_t_naive", "mean"),
        rps_margin_model=("rps_m_model", "mean"), rps_margin_mkt=("rps_m_mkt", "mean"), rps_margin_naive=("rps_m_naive", "mean"),
        mae_model=("exp_t_model", lambda x: np.nan), avg_total=("total", "mean"),
        avg_pred_model=("exp_t_model", "mean"), avg_pred_mkt=("exp_t_mkt", "mean"))
    for col, pred in [("mae_model", "exp_t_model"), ("mae_mkt", "exp_t_mkt"), ("mae_naive", "exp_t_naive")]:
        summ[col] = R.groupby(["tour", "best_of"]).apply(lambda d: (d[pred] - d.total).abs().mean())
    for col, pred in [("brier_over_model", "pover_model"), ("brier_over_mkt", "pover_mkt")]:
        summ[col] = R.groupby(["tour", "best_of"]).apply(lambda d: ((d[pred] - d.over) ** 2).mean())
    summ["brier_over_naive"] = R.groupby(["tour", "best_of"]).apply(lambda d: ((d.over.mean() - d.over) ** 2).mean())
    R.to_parquet(f"{DATA}/points_test.parquet")
    t.drop(columns="naive").to_parquet(f"{DATA}/points_test_rows.parquet")
    json.dump(out, open(f"{DATA}/points_report.json", "w"), indent=1, default=float)
    print(json.dumps(out, indent=1, default=float))
    print(summ.round(4).T.to_string())


if __name__ == "__main__":
    main()
