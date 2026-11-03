"""Challenger / WTA125 backtest: model vs Kalshi's pre-match price (late Aug -> now).

Question: is the model competitive in the lower tiers, where we suspected the edge would be?
- log loss: model vs Kalshi pre-match mid (winner's probability)
- does the model add information beyond Kalshi? (logistic blend fit on Aug-Sep, scored Oct-Nov)
- flat-stake ROI buying at Kalshi's ask + taker fee when model edge >= threshold
Ratings are walk-forward: each match is predicted before its own result enters the ratings.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

import backtest as b
import elo
from kalshi_prices import OUT as PRICES

FEE = 0.07
logit = lambda p: np.log(np.clip(p, 1e-6, 1 - 1e-6) / (1 - np.clip(p, 1e-6, 1 - 1e-6)))


def model_probs():
    out = []
    for tour in ("atp", "wta"):
        s, _ = elo.build_stream(tour)
        p, _, _ = elo.run(s, mov=True, level_k=True, layoff=True)
        prm = b.tune(p)
        p["p_model"] = elo.prob(p, prm["w_blend"], prm["scale"])
        k = p[p.src == "kalshi"][["match_id", "tour", "date", "tourney", "w_name", "l_name", "p_model", "n_w", "n_l"]]
        out.append(k)
    return pd.concat(out)


def main():
    px = pd.read_csv(PRICES).dropna(subset=["bid", "ask"])
    px = px[(px.bid > 0) & (px.ask < 1) & (px.ask - px.bid <= 0.10)]
    px["p_mkt"] = (px.bid + px.ask) / 2
    m = model_probs().merge(px.rename(columns={"event": "match_id"}), on="match_id")
    m["exp"] = np.where(np.minimum(m.n_w, m.n_l) >= 50, "both 50+ matches", "a player <50")
    print(f"matches with model + Kalshi pre-match price: {len(m)}")

    g = m.groupby(["tour"])
    summ = pd.DataFrame({"n": g.size(), "ll_model": g.apply(lambda d: b.ll(d.p_model).mean()),
                         "ll_kalshi": g.apply(lambda d: b.ll(d.p_mkt).mean())})
    summ["gap"] = summ.ll_model - summ.ll_kalshi
    g2 = m.groupby(["tour", "exp"])
    summ2 = pd.DataFrame({"n": g2.size(), "gap": g2.apply(lambda d: b.ll(d.p_model).mean() - b.ll(d.p_mkt).mean())})
    print("\n== log loss (lower = better; gap > 0 = model worse than Kalshi)\n", summ.round(4).to_string())
    print("\n== by experience\n", summ2.round(4).to_string())

    # orient randomly so y isn't always 1
    rng = np.random.default_rng(0)
    flip = rng.random(len(m)) < 0.5
    o = pd.DataFrame({"y": np.where(flip, 0, 1), "date": m.date.values,
                      "pm": np.where(flip, 1 - m.p_model, m.p_model),
                      "pk": np.where(flip, 1 - m.p_mkt, m.p_mkt),
                      # buy price for the oriented side: winner side = its ask; loser side = 1 - winner bid
                      "ask": np.where(flip, 1 - m.bid, m.ask)})
    tr, te = o[o.date < "2026-10-01"], o[o.date >= "2026-10-01"]
    X = lambda d: np.column_stack([logit(d.pk), logit(d.pm)])
    fit = sm.Logit(tr.y, X(tr)).fit(disp=0)
    pb = fit.predict(X(te))
    llf = lambda y, p: -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    print(f"\n== info beyond Kalshi: coef_kalshi {fit.params[0]:.3f}, coef_model {fit.params[1]:.3f} "
          f"(se {fit.bse[1]:.3f}); Oct-Nov log loss blend {llf(te.y, pb):.4f} vs Kalshi {llf(te.y, te.pk):.4f}")

    rows = []
    cost = o.ask + FEE * o.ask * (1 - o.ask)
    for e in (0.0, 0.02, 0.05, 0.10):
        sel = (o.pm - cost) >= e
        r = np.where(o.y[sel] == 1, 1 / cost[sel] - 1, -1.0)  # $1 risked at all-in cost
        rows.append({"min_model_edge": e, "bets": int(sel.sum()), "roi": r.mean() if sel.sum() else np.nan,
                     "se": r.std() / np.sqrt(sel.sum()) if sel.sum() > 1 else np.nan})
    print("\n== flat $1 bets at Kalshi ask + fee when model edge >= x\n", pd.DataFrame(rows).round(4).to_string())
    m.to_csv(PRICES.parent / "challenger_backtest_rows.csv", index=False)


if __name__ == "__main__":
    main()
