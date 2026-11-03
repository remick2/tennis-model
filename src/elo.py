"""Overall + surface Elo, run walk-forward over the full match stream.

For every match we record the PRE-match rating gaps, then update. Storing the gaps (not a
final probability) lets us tune the overall/surface blend and calibration afterwards
without re-running the loop.

Choices (standard tennis Elo, Sackmann / FiveThirtyEight style):
- K = 250 / (n + 5)^0.4: new players move fast, established players move slowly.
- Separate rating per surface with its own match count; overall rating updates on every match.
- Walkovers and retirements don't update ratings (they say more about injury than ability).
"""
from collections import defaultdict

import numpy as np
import pandas as pd

from load import SACKMANN_END, games, load_odds, load_sackmann
import crosswalk

SURFACES = ("Hard", "Clay", "Grass")


def k(n):
    return 250.0 / (n + 5) ** 0.4


def exp_p(ra, rb):
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))


def build_stream(tour):
    sack = load_sackmann(tour)
    odds = load_odds(tour)
    idmap = crosswalk.build(sack, odds, tour)
    odds["w_id"] = odds.o_w_id.map(idmap)
    odds["l_id"] = odds.o_l_id.map(idmap)
    post = odds[odds.date >= pd.Timestamp(str(SACKMANN_END))].copy()
    post["src"] = "odds"
    post["order"] = post.start.rank(method="first")  # real start times after the switch
    stream = pd.concat([sack, post[sack.columns.intersection(post.columns).tolist() + ["start", "match_id"]]],
                       ignore_index=True)
    stream = stream.sort_values(["date", "tourney", "order"], kind="stable").reset_index(drop=True)
    return stream, odds


LEVEL_K = {"G": 1.1, "C": 0.9, "50": 0.85, "60": 0.85, "75": 0.85, "80": 0.85, "100": 0.9}


def run(stream, mov=False, level_k=False, layoff=False):
    """mov:     scale each update by the winner's share of games (normalised to ~1 on average),
                so a 6-1 6-1 moves ratings more than 7-6 7-6 (WElo, Angelini et al. 2022).
       level_k: bigger K at slams, smaller at Challenger/ITF.
       layoff:  first matches back after 90+ days get a larger K (rating is stale)."""
    r = defaultdict(lambda: 1500.0); n = defaultdict(int)
    rs = defaultdict(lambda: 1500.0); ns = defaultdict(int)
    last = {}
    rec = {c: np.full(len(stream), np.nan) for c in ("d_o", "d_s", "n_w", "n_l", "ns_w", "ns_l")}
    cols = zip(stream.w_id, stream.l_id, stream.surface, stream.status, stream.score,
               stream.level, stream.date.values)
    for i, (w, l, surf, st, sc, lev, dt) in enumerate(cols):
        has_s = surf in SURFACES
        # --- record pre-match state
        rec["d_o"][i] = r[w] - r[l]
        rec["n_w"][i], rec["n_l"][i] = n[w], n[l]
        if has_s:
            rec["d_s"][i] = rs[(w, surf)] - rs[(l, surf)]
            rec["ns_w"][i], rec["ns_l"][i] = ns[(w, surf)], ns[(l, surf)]
        if st != "done":
            continue
        # --- multipliers
        m = 1.0
        if mov:
            g = games(sc)
            if g:
                m *= (g[0] / (g[0] + g[1])) / 0.6
        if level_k:
            m *= LEVEL_K.get(str(lev), 1.0)
        mw = ml = m
        if layoff:
            gap = lambda p: (dt - last[p]) / np.timedelta64(1, "D") if p in last else 0
            mw *= 1.5 if gap(w) > 90 else 1.0
            ml *= 1.5 if gap(l) > 90 else 1.0
        last[w] = last[l] = dt
        # --- update
        e = exp_p(r[w], r[l])
        r[w] += k(n[w]) * mw * (1 - e); r[l] -= k(n[l]) * ml * (1 - e)
        n[w] += 1; n[l] += 1
        if has_s:
            sw, sl = (w, surf), (l, surf)
            e = exp_p(rs[sw], rs[sl])
            rs[sw] += k(ns[sw]) * mw * (1 - e); rs[sl] -= k(ns[sl]) * ml * (1 - e)
            ns[sw] += 1; ns[sl] += 1
    out = stream.copy()
    for c, v in rec.items():
        out[c] = v
    return out, dict(r), dict(rs)


# ---------- turning rating gaps into a probability ----------
def bo5_from_bo3(p3):
    """Bo3 match prob -> per-set prob q (solve q^2(3-2q)=p3) -> Bo5 match prob.
    Best-of-5 gives the better player more room, so favourites get stronger."""
    p3 = np.clip(p3, 1e-6, 1 - 1e-6)
    lo, hi = np.zeros_like(p3), np.ones_like(p3)
    for _ in range(50):  # bisection, vectorised
        q = (lo + hi) / 2
        too_low = q * q * (3 - 2 * q) < p3
        lo, hi = np.where(too_low, q, lo), np.where(too_low, hi, q)
    q = (lo + hi) / 2
    return q ** 3 * (1 + 3 * (1 - q) + 6 * (1 - q) ** 2)


def prob(df, w_blend, scale, use_bo5=True):
    d_s = df.d_s.fillna(df.d_o)  # no surface (e.g. some Davis Cup rows) -> overall only
    d = w_blend * df.d_o + (1 - w_blend) * d_s
    p = 1 / (1 + 10 ** (-scale * d / 400))
    if use_bo5:
        p = np.where(df.best_of == 5, bo5_from_bo3(np.asarray(p, float)), p)
    return np.asarray(p, float)
