"""Game-spread backtest: point model vs Kalshi's pre-match ATP game-spread prices (Aug-Nov 2026).

Kalshi market: "Will X win at least L more games than Y?" (L = 1.5, 3.5, 6.5 ...), YES if X's game
differential > L. Model P(yes) = sum of the point model's game-margin distribution above L, two versions:
raw (model's own win prob) and calibrated (win prob forced to the closing moneyline consensus).
Buying NO = taking Y +L (the underdog side of the spread when X is the favourite).

Run: python spread_backtest.py            (prices must already be in data/kalshi_spread_prices.csv;
     python kalshi_prices.py --spreads    downloads them)
"""
import json
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import statsmodels.api as sm

import elo
import pointmodel as pm
from crosswalk import name_ok
from ratings import POINT_PARAMS

ROOT = Path(__file__).resolve().parents[1]
PRICES = ROOT / "data" / "kalshi_spread_prices.csv"
META = ROOT / "data" / "kalshi_spread_meta.json"
FEE = 0.07
RULE = re.compile(r"in favor of (.+?) across the full match is above ([\d.]+) games in the (.+?) vs (.+?) "
                  r"professional tennis match in the (\d{4}) (.+?) (Round|Qualif|Final|Semi|Quarter)")
logit = lambda p: np.log(np.clip(p, 1e-6, 1 - 1e-6) / (1 - np.clip(p, 1e-6, 1 - 1e-6)))
llb = lambda y, p: -np.mean(y * np.log(np.clip(p, 1e-6, 1)) + (1 - y) * np.log(np.clip(1 - p, 1e-6, 1)))


def meta():
    """ticker -> [favoured player X, line, player1, player2, tournament] (cached)."""
    if META.exists():
        return json.loads(META.read_text())
    s, out, cur = requests.Session(), {}, None
    while True:
        p = {"series_ticker": "KXATPGSPREAD", "status": "settled", "limit": 1000}
        if cur: p["cursor"] = cur
        for _ in range(25):
            try:
                r = s.get("https://api.elections.kalshi.com/trade-api/v2/markets", params=p, timeout=30)
                if r.status_code == 200: break
            except requests.RequestException:
                pass
            time.sleep(1)
        d = r.json()
        for m in d.get("markets", []):
            g = RULE.search(m.get("rules_primary", ""))
            if g:
                out[m["ticker"]] = [g.group(1), float(g.group(2)), g.group(3), g.group(4), g.group(6)]
        cur = d.get("cursor")
        if not cur or not d.get("markets"):
            break
    META.write_text(json.dumps(out))
    return out


def main():
    px = pd.read_csv(PRICES).dropna(subset=["bid", "ask"])
    px = px[(px.bid > 0) & (px.ask < 1) & (px.ask - px.bid <= 0.10)].copy()
    info = meta()
    px = px[px.ticker.isin(info)].copy()
    px["x"] = px.ticker.map(lambda t: info[t][0])
    px["line"] = px.ticker.map(lambda t: info[t][1])
    px["y"] = (px.result == "yes").astype(int)
    px["p_kalshi"] = (px.bid + px.ask) / 2

    stream, odds = elo.build_stream("atp")
    sk = pm.run_skills(stream, lr=0.12, lr_surf=0.1)
    o = stream[stream.src == "odds"].reset_index()[["index", "date", "w_name", "l_name", "match_id"]]
    o = o.merge(odds[["match_id", "p_close", "best_of"]], on="match_id", how="left")
    prm = POINT_PARAMS["atp"]
    out, linked = [], 0
    for ev, m in px.groupby("event"):
        _, _, a, c, _ = info[m.ticker.iloc[0]]
        d = pd.Timestamp(m.close_time.iloc[0]).tz_localize(None).normalize()
        cand = o[(o.date >= d - pd.Timedelta(days=12)) & (o.date <= d + pd.Timedelta(days=1))]
        hit = cand[[(name_ok(a, w) and name_ok(c, l)) or (name_ok(c, w) and name_ok(a, l))
                    for w, l in zip(cand.w_name, cand.l_name)]]
        if len(hit) != 1:
            continue
        linked += 1
        h = hit.iloc[0]
        bo = int(h.best_of) if h.best_of == h.best_of else 3
        pa, pb = pm.point_probs(sk.loc[[h["index"]]])          # stream winner = A
        la, lb = pm.logit(pa[0]), pm.logit(pb[0])
        cc, dd = (la + lb) / 2 + prm["delta"], prm["kappa"] * (la - lb) / 2
        A, B = pm.sig(cc + dd), pm.sig(cc - dd)
        _, _, marg_raw = pm.match_dist_mix(A, B, bo, prm["sig_rel"])
        # calibrate win prob to the closing line (same bisection as the totals backtest)
        la2, lb2 = pm.logit(A), pm.logit(B); lo, hi = -1.5, 1.5
        for _ in range(14):
            mid = (lo + hi) / 2
            pw = pm.match_dist_mix(pm.sig(la2 + mid), pm.sig(lb2 - mid), bo, prm["sig_rel"])[0]
            lo, hi = (mid, hi) if pw < h.p_close else (lo, mid)
        _, _, marg_cal = pm.match_dist_mix(pm.sig(la2 + (lo + hi) / 2), pm.sig(lb2 - (lo + hi) / 2), bo, prm["sig_rel"])
        for x in m.itertuples():
            sign = 1 if name_ok(x.x, h.w_name) else -1           # margin is winner-minus-loser
            p_raw = sum(v for g, v in marg_raw.items() if sign * g > x.line)
            p_cal = sum(v for g, v in marg_cal.items() if sign * g > x.line)
            out.append({"event": ev, "x": x.x, "line": x.line, "y": x.y, "bid": x.bid, "ask": x.ask,
                        "p_kalshi": x.p_kalshi, "p_raw": p_raw, "p_cal": p_cal, "close_time": x.close_time,
                        "x_is_fav": (h.p_close >= 0.5) == (sign == 1)})
    d = pd.DataFrame(out)
    d.to_csv(ROOT / "data" / "spread_backtest_rows.csv", index=False)
    print(f"linked {linked} of {px.event.nunique()} matches; lines scored {len(d)}")
    print("\n== log loss (lower = better)")
    print(pd.Series({"kalshi": llb(d.y, d.p_kalshi), "model_raw": llb(d.y, d.p_raw),
                     "model_cal": llb(d.y, d.p_cal)}).round(4).to_string())
    tr, te = d[d.close_time < "2026-10-01"], d[d.close_time >= "2026-10-01"]
    X = lambda g: np.column_stack([logit(g.p_kalshi), logit(g.p_cal)])
    fit = sm.Logit(tr.y, X(tr)).fit(disp=0)
    print(f"\n== info beyond Kalshi: coef_kalshi {fit.params.iloc[0]:.3f}, coef_model {fit.params.iloc[1]:.3f} "
          f"(se {fit.bse.iloc[1]:.3f}); Oct-Nov log loss blend {llb(te.y, fit.predict(X(te))):.4f} "
          f"vs Kalshi {llb(te.y, te.p_kalshi):.4f}")

    yes_cost = d.ask + FEE * d.ask * (1 - d.ask)
    no_px = 1 - d.bid
    no_cost = no_px + FEE * no_px * (1 - no_px)
    rows = []
    for name, col in (("raw", "p_raw"), ("calibrated", "p_cal")):
        e_yes, e_no = d[col] - yes_cost, (1 - d[col]) - no_cost
        for e in (0.0, 0.03, 0.05, 0.10):
            by, bn = e_yes >= e, e_no >= e
            r_yes = np.where(d.y[by] == 1, 1 / yes_cost[by] - 1, -1.0)
            r_no = np.where(d.y[bn] == 0, 1 / no_cost[bn] - 1, -1.0)
            ret = np.concatenate([r_yes, r_no])
            # "dog + games" = buying NO on the favourite's spread
            dog = np.where(d.y[bn & d.x_is_fav] == 0, 1 / no_cost[bn & d.x_is_fav] - 1, -1.0)
            rows.append({"model": name, "min_edge": e, "bets": len(ret),
                         "roi": ret.mean() if len(ret) else np.nan,
                         "se": ret.std() / np.sqrt(len(ret)) if len(ret) > 1 else np.nan,
                         "dog_plus_bets": len(dog), "dog_plus_roi": dog.mean() if len(dog) else np.nan})
    print("\n== flat $1 bets at Kalshi ask + fee when model edge >= x\n", pd.DataFrame(rows).round(4).to_string())

    # the user's idea: underdog +games, all of them, no model (does Kalshi underprice the plus side?)
    fav = d[d.x_is_fav]
    r = np.where(fav.y == 0, 1 / no_cost[fav.index] - 1, -1.0)
    print(f"\n== baseline: every underdog +line at Kalshi (no model): n {len(fav)}, ROI {r.mean():+.4f} ± {r.std() / np.sqrt(len(fav)):.4f}")
    for L, g in fav.groupby("line"):
        rr = np.where(g.y == 0, 1 / no_cost[g.index] - 1, -1.0)
        if len(g) >= 30:
            print(f"   dog +{L}: n {len(g)}, Kalshi P(dog covers) {(1 - g.p_kalshi).mean():.3f}, actual {1 - g.y.mean():.3f}, ROI {rr.mean():+.3f}")


if __name__ == "__main__":
    main()
