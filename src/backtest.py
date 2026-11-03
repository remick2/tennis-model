"""Tune on 2022-24 (results only), then test 2025-26 against consensus closing odds.

Run: python backtest.py   (after: python -c "import elo; ..." builds data/preds_*.parquet — see run_all.py)
"""
import json

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

import elo
from load import MAIN_LEVELS, SACKMANN_END

DATA = elo.__file__.rsplit("/src/", 1)[0] + "/data"
EPS = 1e-9
SWITCH = pd.Timestamp(str(SACKMANN_END))


def ll(p):  # p = prob assigned to the actual winner
    return -np.log(np.clip(p, EPS, 1 - EPS))


def brier(p):
    return (1 - p) ** 2


# ---------------------------------------------------------------- tuning (no odds used)
def tune(preds):
    v = preds[(preds.date >= "2022-01-01") & (preds.date < "2025-01-01") & (preds.status == "done")
              & preds.level.isin(MAIN_LEVELS) & (preds.n_w >= 10) & (preds.n_l >= 10)]
    best = None
    for w in np.round(np.arange(0, 1.01, 0.1), 2):
        res = minimize_scalar(lambda s: ll(elo.prob(v, w, s)).mean(), bounds=(0.3, 2.0), method="bounded")
        if best is None or res.fun < best[2]:
            best = (w, res.x, res.fun)
    w, s, _ = best
    no_bo5 = ll(elo.prob(v, w, s, use_bo5=False))[v.best_of == 5].mean()
    yes_bo5 = ll(elo.prob(v, w, s, use_bo5=True))[v.best_of == 5].mean()
    return {"w_blend": float(w), "scale": float(s), "n_tune": len(v),
            "tune_logloss": float(best[2]), "slam_ll_bo5_on": float(yes_bo5), "slam_ll_bo5_off": float(no_bo5)}


# ---------------------------------------------------------------- attach model probs to odds rows
def attach(preds, odds, prm):
    preds = preds.copy()
    preds["p_model"] = elo.prob(preds, prm["w_blend"], prm["scale"])
    # after the switch, odds rows ARE the stream rows -> join on match_id
    post = odds[odds.date >= SWITCH].merge(
        preds[preds.src == "odds"][["match_id", "p_model", "n_w", "n_l"]], on="match_id", how="left")
    # before the switch, find the same match in Sackmann's stream: same ids, within 8 days
    pre = odds[odds.date < SWITCH].copy()
    sk = preds[preds.src == "sack"][["w_id", "l_id", "date", "p_model", "n_w", "n_l"]]
    m = pre.reset_index().merge(sk, on=["w_id", "l_id"], suffixes=("", "_s"))
    m = m[(m.date - m.date_s).abs() <= pd.Timedelta(days=8)]
    m = m.sort_values("index").drop_duplicates("index")  # first hit only
    pre = pre.join(m.set_index("index")[["p_model", "n_w", "n_l"]])
    return pd.concat([pre, post], ignore_index=True)


# ---------------------------------------------------------------- evaluation
def test_set(df):
    keep = (df.status == "done") & df.level.isin(["G", "M", "A"]) & (df.books >= 10) \
        & df.p_close.notna() & df.p_model.notna()
    return df[keep].copy()


def summarize(t, by):
    g = t.groupby(by, dropna=False)
    out = pd.DataFrame({
        "n": g.size(),
        "ll_model": g.apply(lambda d: ll(d.p_model).mean()),
        "ll_market": g.apply(lambda d: ll(d.p_close).mean()),
        "brier_model": g.apply(lambda d: brier(d.p_model).mean()),
        "brier_market": g.apply(lambda d: brier(d.p_close).mean()),
    })
    out["ll_gap"] = out.ll_model - out.ll_market  # >0 = model worse than market
    return out.round(4)


def oriented(t, seed=0):
    """Random side orientation so 'y' isn't always 1 (needed for regression/betting)."""
    rng = np.random.default_rng(seed)
    flip = rng.random(len(t)) < 0.5
    o = pd.DataFrame(index=t.index)
    o["y"] = np.where(flip, 0, 1)
    for a, b, c in [("pm", "p_model", None), ("pc", "p_close", None), ("po", "p_open", None)]:
        o[a] = np.where(flip, 1 - t[b], t[b])
    o["fair"] = np.where(flip, t.l_fair, t.w_fair)
    o["best"] = np.where(flip, t.l_best, t.w_best)
    o["margin"] = t.margin.values / 100
    o["date"] = t.date.values
    o["tour"] = t.tour.values
    return o


def logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def info_beyond_market(o):
    """Fit y ~ a*logit(market) + b*logit(model) on 2025, score on 2026.
    If the model has info the closing line lacks, b > 0 and the blend beats the market out of sample."""
    import statsmodels.api as sm
    tr, te = o[o.date < "2026-01-01"], o[o.date >= "2026-01-01"]
    X = lambda d: np.column_stack([logit(d.pc), logit(d.pm)])
    fit = sm.Logit(tr.y, X(tr)).fit(disp=0)
    p_blend = fit.predict(X(te))
    ll_b = -np.mean(te.y * np.log(p_blend) + (1 - te.y) * np.log(1 - p_blend))
    ll_m = -np.mean(te.y * np.log(te.pc) + (1 - te.y) * np.log(1 - te.pc))
    return {"coef_market": fit.params.iloc[0], "coef_model": fit.params.iloc[1],
            "se_model": fit.bse.iloc[1], "oos_ll_blend_2026": ll_b, "oos_ll_market_2026": ll_m}


def line_move(o):
    """Does the model predict where the line goes? corr(model - open, close - open)."""
    d = o.dropna(subset=["po"])
    return {"corr_model_minus_open_vs_move": float(np.corrcoef(d.pm - d.po, d.pc - d.po)[0, 1]),
            "n": len(d)}


def bet_sim(o, edges=(0.0, 0.03, 0.05, 0.10)):
    """Flat 1u bets when model EV > edge. Two prices:
    'typical book' = fair odds with the median bookmaker margin taken out (roughly a normal book),
    'best' = best closing price across ~21 books (upper bound; you won't get it consistently)."""
    rows = []
    typical = o.fair / (1 + o.margin)
    for name, price in [("typical_book", typical), ("best_of_21", o.best)]:
        ev = o.pm * price - 1
        for e in edges:
            b = ev > e
            ret = np.where(o.y[b] == 1, price[b] - 1, -1.0)
            rows.append({"price": name, "min_edge": e, "bets": int(b.sum()),
                         "roi": float(ret.mean()) if b.sum() else np.nan,
                         "roi_se": float(ret.std() / np.sqrt(b.sum())) if b.sum() > 1 else np.nan})
    return pd.DataFrame(rows).round(4)


def main():
    report = {}
    tests = []
    for tour in ("atp", "wta"):
        preds = pd.read_parquet(f"{DATA}/preds_{tour}.parquet")
        odds = pd.read_parquet(f"{DATA}/odds_{tour}.parquet")
        prm = tune(preds)
        report[tour] = {"params": prm}
        df = attach(preds, odds, prm)
        report[tour]["coverage"] = {
            "odds_rows": len(odds), "with_model_prob": int(df.p_model.notna().sum())}
        tests.append(test_set(df))
    t = pd.concat(tests, ignore_index=True)
    t["year"] = t.date.dt.year
    t["exp"] = np.where(np.minimum(t.n_w, t.n_l) >= 50, "both 50+ matches", "a player <50 matches")
    t.to_parquet(f"{DATA}/test_rows.parquet")

    report["overall"] = summarize(t, ["tour"]).reset_index().to_dict("records")
    tables = {
        "by_tour_level": summarize(t, ["tour", "level"]),
        "by_tour_surface": summarize(t, ["tour", "surface"]),
        "by_tour_year": summarize(t, ["tour", "year"]),
        "by_tour_experience": summarize(t, ["tour", "exp"]),
    }
    o = oriented(t)
    report["info_beyond_market"] = {k: float(v) for k, v in info_beyond_market(o).items()}
    report["line_move"] = line_move(o)
    sims = bet_sim(o)
    json.dump(report, open(f"{DATA}/report.json", "w"), indent=1, default=float)
    print(json.dumps(report, indent=1, default=float))
    for k_, v in tables.items():
        print(f"\n== {k_}\n{v.to_string()}")
    print(f"\n== bet sim (flat 1u, at the CLOSE)\n{sims.to_string()}")
    return report, tables, sims


if __name__ == "__main__":
    main()
