"""Totals backtest: point model vs Kalshi's pre-match total-games prices (ATP/WTA main tour, Aug-Nov 2026).

For each settled "Over X.5 games" market:
  Kalshi P(over) = pre-match mid (last hourly candle >= 3h before settlement)
  model P(over)  = point model (pre-match serve/return skills -> Markov with form noise), two versions:
                   raw, and calibrated so its win prob equals the consensus closing moneyline
Outcome = how the market settled. Then: log loss, info beyond Kalshi, and ROI buying the side the
model likes at Kalshi's ask + taker fee.
"""
import json
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import statsmodels.api as sm

import backtest as b
import elo
import pointmodel as pm
from crosswalk import name_ok
from ratings import POINT_PARAMS

ROOT = Path(__file__).resolve().parents[1]
PRICES = ROOT / "data" / "kalshi_totals_prices.csv"
META = ROOT / "data" / "kalshi_totals_meta.json"
FEE = 0.07
RULE = re.compile(r".*in the (.+?) vs (.+?) professional tennis match in the (\d{4}) (.+?) (Round|Qualif|Final|Semi|Quarter)")
logit = lambda p: np.log(np.clip(p, 1e-6, 1 - 1e-6) / (1 - np.clip(p, 1e-6, 1 - 1e-6)))


def meta():
    """event -> (player1, player2, tournament) from the market rules text (cached)."""
    if META.exists():
        return json.loads(META.read_text())
    s, out = requests.Session(), {}
    for series in ("KXATPGTOTAL", "KXWTAGTOTAL"):
        cur = None
        while True:
            p = {"series_ticker": series, "status": "settled", "limit": 1000}
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
                    out[m["event_ticker"]] = [g.group(1), g.group(2), g.group(4)]
            cur = d.get("cursor")
            if not cur or not d.get("markets"):
                break
    META.write_text(json.dumps(out))
    return out


def link(px, info, tour, stream, odds):
    """Kalshi totals event -> stream row of the same match (names + date)."""
    o = stream[(stream.src == "odds")].reset_index()[["index", "date", "w_name", "l_name", "match_id"]]
    o = o.merge(odds[["match_id", "p_close", "best_of"]], on="match_id", how="left")
    ev = px[px.series.str.contains(tour.upper())].drop_duplicates("event")
    rows = []
    for e in ev.itertuples():
        if e.event not in info:
            continue
        a, c, tourney = info[e.event]
        d = pd.Timestamp(e.close_time).tz_localize(None).normalize()
        cand = o[(o.date >= d - pd.Timedelta(days=12)) & (o.date <= d + pd.Timedelta(days=1))]
        hit = cand[[(name_ok(a, w) and name_ok(c, l)) or (name_ok(c, w) and name_ok(a, l))
                    for w, l in zip(cand.w_name, cand.l_name)]]
        if len(hit) == 1:
            h = hit.iloc[0]
            rows.append({"event": e.event, "sidx": h["index"], "p_close": h.p_close,
                         "best_of": int(h.best_of) if h.best_of == h.best_of else 3, "tour": tour})
    return pd.DataFrame(rows)


def p_over_lines(pa, pb, bo, prm, lines, target=None):
    la, lb = pm.logit(pa), pm.logit(pb)
    c, d = (la + lb) / 2 + prm["delta"], prm["kappa"] * (la - lb) / 2
    A, B = pm.sig(c + d), pm.sig(c - d)
    if target is not None and target == target:  # calibrate win prob to the closing line
        la2, lb2 = pm.logit(A), pm.logit(B)
        lo, hi = -1.5, 1.5
        for _ in range(14):
            mid = (lo + hi) / 2
            p = pm.match_dist_mix(pm.sig(la2 + mid), pm.sig(lb2 - mid), bo, prm["sig_rel"])[0]
            lo, hi = (mid, hi) if p < target else (lo, mid)
        A, B = pm.sig(la2 + (lo + hi) / 2), pm.sig(lb2 - (lo + hi) / 2)
    _, tot, _ = pm.match_dist_mix(A, B, bo, prm["sig_rel"])
    return {L: sum(v for g, v in tot.items() if g > L) for L in lines}


def main():
    px = pd.read_csv(PRICES).dropna(subset=["bid", "ask"])
    px = px[(px.bid > 0) & (px.ask < 1) & (px.ask - px.bid <= 0.10)].copy()
    px["line"] = px.title.str.extract(r"Over ([\d.]+)").astype(float)
    px["y"] = (px.result == "yes").astype(int)
    px["p_kalshi"] = (px.bid + px.ask) / 2
    info = meta()
    out = []
    for tour in ("atp", "wta"):
        stream, odds = elo.build_stream(tour)
        sk = pm.run_skills(stream, lr=0.12, lr_surf=0.1)
        L = link(px, info, tour, stream, odds)
        print(f"{tour}: linked {len(L)} of {px[px.series.str.contains(tour.upper())].event.nunique()} events", flush=True)
        for r in L.itertuples():
            row = sk.loc[[r.sidx]]
            pa, pb = pm.point_probs(row)
            m = px[px.event == r.event]
            raw = p_over_lines(pa[0], pb[0], r.best_of, POINT_PARAMS[tour], m.line.tolist())
            cal = p_over_lines(pa[0], pb[0], r.best_of, POINT_PARAMS[tour], m.line.tolist(), r.p_close)
            for x in m.itertuples():
                out.append({"tour": tour, "event": r.event, "line": x.line, "y": x.y, "bid": x.bid, "ask": x.ask,
                            "p_kalshi": x.p_kalshi, "p_raw": raw[x.line], "p_cal": cal[x.line],
                            "close_time": x.close_time})
    d = pd.DataFrame(out)
    d.to_csv(ROOT / "data" / "totals_backtest_rows.csv", index=False)
    llb = lambda y, p: -np.mean(y * np.log(np.clip(p, 1e-6, 1)) + (1 - y) * np.log(np.clip(1 - p, 1e-6, 1)))
    print(f"\nlines scored: {len(d)} ({d.event.nunique()} matches)")
    print("\n== log loss on over/under outcomes (lower = better)")
    print(d.groupby("tour").apply(lambda g: pd.Series({
        "n": len(g), "kalshi": llb(g.y, g.p_kalshi), "model_raw": llb(g.y, g.p_raw), "model_cal": llb(g.y, g.p_cal)})).round(4).to_string())

    tr, te = d[d.close_time < "2026-10-01"], d[d.close_time >= "2026-10-01"]
    X = lambda g: np.column_stack([logit(g.p_kalshi), logit(g.p_cal)])
    fit = sm.Logit(tr.y, X(tr)).fit(disp=0)
    print(f"\n== info beyond Kalshi: coef_kalshi {fit.params.iloc[0]:.3f}, coef_model {fit.params.iloc[1]:.3f} "
          f"(se {fit.bse.iloc[1]:.3f}); Oct-Nov log loss blend {llb(te.y, fit.predict(X(te))):.4f} "
          f"vs Kalshi {llb(te.y, te.p_kalshi):.4f}")

    rows = []
    for name, col in (("raw", "p_raw"), ("calibrated", "p_cal")):
        over_cost = d.ask + FEE * d.ask * (1 - d.ask)
        under_px = 1 - d.bid
        under_cost = under_px + FEE * under_px * (1 - under_px)
        e_over, e_under = d[col] - over_cost, (1 - d[col]) - under_cost
        for e in (0.0, 0.03, 0.05, 0.10):
            bo, bu = e_over >= e, e_under >= e
            ret = np.concatenate([np.where(d.y[bo] == 1, 1 / over_cost[bo] - 1, -1.0),
                                  np.where(d.y[bu] == 0, 1 / under_cost[bu] - 1, -1.0)])
            rows.append({"model": name, "min_edge": e, "bets": len(ret), "overs": int(bo.sum()),
                         "unders": int(bu.sum()), "roi": ret.mean() if len(ret) else np.nan,
                         "se": ret.std() / np.sqrt(len(ret)) if len(ret) > 1 else np.nan})
    print("\n== flat $1 bets at Kalshi ask + fee when model edge >= x\n", pd.DataFrame(rows).round(4).to_string())


if __name__ == "__main__":
    main()
