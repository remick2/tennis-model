"""Compare Elo variants. Select on 2022-24 tuning log loss (no odds); report 2025-26 gap to the close."""
import itertools, pickle, warnings
import numpy as np, pandas as pd
import elo, backtest as b
warnings.filterwarnings("ignore")

streams = {t: elo.build_stream(t) for t in ("atp", "wta")}
rows = []
for mov, lk, lay in itertools.product([False, True], [False, True], [False, True]):
    res = {"mov": mov, "level_k": lk, "layoff": lay}
    tests = []
    for t, (stream, odds) in streams.items():
        preds, _, _ = elo.run(stream, mov=mov, level_k=lk, layoff=lay)
        prm = b.tune(preds)
        res[f"{t}_tune_ll"] = prm["tune_logloss"]
        tests.append(b.test_set(b.attach(preds, odds, prm)))
    t_ = pd.concat(tests)
    for t in ("atp", "wta"):
        d = t_[t_.tour == t]
        res[f"{t}_test_gap"] = b.ll(d.p_model).mean() - b.ll(d.p_close).mean()
    res["n_test"] = len(t_)
    rows.append(res); print(res, flush=True)
out = pd.DataFrame(rows)
out.to_csv("../data/elo_variants.csv", index=False)
print(out.round(4).to_string())
