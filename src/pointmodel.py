"""Point-level model: serve/return skill -> point probs -> exact game/set/match distributions.

1) Skills (opponent-adjusted, like Elo but for points). For each player keep
   serve skill s and return skill r, overall and per surface, in logit space:
       P(A wins a point on A's serve) = sigmoid(base[tour,surface] + s_A - r_B)
   After each match, nudge s_A / r_B toward what actually happened on A's serve points
   (and vice versa). Learning rate = how fast form counts vs. history; starting everyone
   at 0 (= tour average) is the regression to the mean.
2) Markov chain: point prob -> hold prob -> exact set-score distribution -> match.
   Gives win prob, total-games distribution and game-margin distribution in one pass.
"""
from collections import defaultdict
from functools import lru_cache

import numpy as np

SURFACES = ("Hard", "Clay", "Grass")


def sig(x):
    return 1 / (1 + np.exp(-x))


def logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


# ======================================================================= skills
def base_rates(stream):
    """Tour/surface average serve-point win % (logit), from 2010-2021 only (no peeking at test years)."""
    d = stream[(stream.date < "2022-01-01") & (stream.w_svpt > 0) & (stream.l_svpt > 0)]
    out = {}
    for (surf), g in d.groupby("surface"):
        out[surf] = float(logit((g.w_spw.sum() + g.l_spw.sum()) / (g.w_svpt.sum() + g.l_svpt.sum())))
    out["_all"] = float(logit((d.w_spw.sum() + d.l_spw.sum()) / (d.w_svpt.sum() + d.l_svpt.sum())))
    return out


def run_skills(stream, lr=0.08, lr_surf=0.12):
    """Walk forward; record PRE-match skills for every row."""
    base = base_rates(stream)
    S = defaultdict(float); R = defaultdict(float)          # overall
    Ss = defaultdict(float); Rs = defaultdict(float)        # per (player, surface)
    N = defaultdict(int)
    n = len(stream)
    rec = {c: np.full(n, np.nan) for c in
           ("base", "s_w", "r_w", "s_l", "r_l", "ss_w", "rs_w", "ss_l", "rs_l", "npt_w", "npt_l")}
    cols = zip(stream.w_id, stream.l_id, stream.surface, stream.status,
               stream.w_svpt, stream.w_spw, stream.l_svpt, stream.l_spw)
    for i, (w, l, surf, st, wsv, wsw, lsv, lsw) in enumerate(cols):
        b = base.get(surf, base["_all"])
        sw, sl = (w, surf), (l, surf)
        rec["base"][i] = b
        rec["s_w"][i], rec["r_w"][i], rec["s_l"][i], rec["r_l"][i] = S[w], R[w], S[l], R[l]
        rec["ss_w"][i], rec["rs_w"][i], rec["ss_l"][i], rec["rs_l"][i] = Ss[sw], Rs[sw], Ss[sl], Rs[sl]
        rec["npt_w"][i], rec["npt_l"][i] = N[w], N[l]
        if st != "done" or not np.all(np.isfinite([wsv, wsw, lsv, lsw])) \
                or not (wsv > 0 and lsv > 0) or wsw > wsv or lsw > lsv:
            continue
        # winner serving: observed vs expected, in logit units (weighted by points played)
        for (srv, ret, n_pts, won) in ((w, l, wsv, wsw), (l, w, lsv, lsw)):
            ssrv, sret = (srv, surf), (ret, surf)
            exp = sig(b + S[srv] + Ss[ssrv] - R[ret] - Rs[sret])
            obs = won / n_pts
            # gradient of binomial log-lik in logit space, scaled per ~80 points
            g = (obs - exp) * n_pts / 80.0
            S[srv] += lr * g; R[ret] -= lr * g
            if surf in SURFACES:
                Ss[ssrv] += lr_surf * g; Rs[sret] -= lr_surf * g
                Ss[ssrv] *= 0.999; Rs[sret] *= 0.999   # surface deviations shrink slowly to 0
        N[w] += wsv + lsv; N[l] += wsv + lsv
    out = stream.copy()
    for c, v in rec.items():
        out[c] = v
    return out


def point_probs(df, surf_w=1.0):
    """P(winner wins a point on own serve), P(loser wins a point on own serve)."""
    pw = sig(df.base + df.s_w + surf_w * df.ss_w - df.r_l - surf_w * df.rs_l)
    pl = sig(df.base + df.s_l + surf_w * df.ss_l - df.r_w - surf_w * df.rs_w)
    return np.asarray(pw, float), np.asarray(pl, float)


# ======================================================================= Markov chain
def p_hold(p):
    q = 1 - p
    return p ** 4 * (1 + 4 * q + 10 * q ** 2) + 20 * p ** 3 * q ** 3 * p ** 2 / (1 - 2 * p * q)


def p_tiebreak(pa, pb):
    """A serves first point; then B 2, A 2, ... First to 7, win by 2."""
    @lru_cache(None)
    def f(a, b):
        if a >= 7 and a - b >= 2: return 1.0
        if b >= 7 and b - a >= 2: return 0.0
        if a == b and a >= 6:  # from deuce: one serve each per pair
            x, y = pa * (1 - pb), (1 - pa) * pb
            return x / (x + y)
        k = a + b
        a_serving = (k % 4 == 0) or (k % 4 == 3)
        p = pa if a_serving else 1 - pb
        return p * f(a + 1, b) + (1 - p) * f(a, b + 1)
    return f(0, 0)


def set_dist(pa, pb, a_serves_first):
    """Exact distribution over final set scores {(ga, gb): prob}. pa/pb = serve-point probs."""
    ha, hb = p_hold(pa), p_hold(pb)
    tb = p_tiebreak(pa, pb) if a_serves_first else 1 - p_tiebreak(pb, pa)
    dist = defaultdict(float)
    states = {(0, 0): 1.0}
    while states:
        nxt = defaultdict(float)
        for (a, b), pr in states.items():
            if (a == 6 and b <= 4) or (a == 7): dist[(a, b)] += pr; continue
            if (b == 6 and a <= 4) or (b == 7): dist[(a, b)] += pr; continue
            if a == 6 and b == 6:
                dist[(7, 6)] += pr * tb; dist[(6, 7)] += pr * (1 - tb); continue
            a_serving = ((a + b) % 2 == 0) == a_serves_first
            pwin = ha if a_serving else 1 - hb
            nxt[(a + 1, b)] += pr * pwin
            nxt[(a, b + 1)] += pr * (1 - pwin)
        states = nxt
    return dist


def match_dist(pa, pb, best_of=3):
    """Returns (P(A wins), {total_games: p}, {A_games - B_games: p}). Averages over who serves first."""
    need = 2 if best_of == 3 else 3
    sd = {True: set_dist(pa, pb, True), False: set_dist(pa, pb, False)}
    p_win = 0.0
    tot = defaultdict(float); marg = defaultdict(float)
    for first in (True, False):
        # state: (sets_a, sets_b, a_serves_first_in_this_set, games_a, games_b) -> prob
        states = {(0, 0, first, 0, 0): 0.5}
        while states:
            nxt = defaultdict(float)
            for (sa, sb, af, ga, gb), pr in states.items():
                if sa == need or sb == need:
                    if sa == need: p_win += pr
                    tot[ga + gb] += pr; marg[ga - gb] += pr
                    continue
                for (a, b), q in sd[af].items():
                    n_games = a + b
                    next_af = af if n_games % 2 == 0 else (not af)
                    key = (sa + (a > b), sb + (b > a), next_af, ga + a, gb + b)
                    nxt[key] += pr * q
            states = nxt
    return p_win, dict(tot), dict(marg)


@lru_cache(maxsize=200_000)
def _cached(pa, pb, best_of):
    return match_dist(pa, pb, best_of)


def match_dist_fast(pa, pb, best_of=3):
    """Round probs to 0.001 so repeated pairs hit the cache."""
    return _cached(round(float(pa), 3), round(float(pb), 3), int(best_of))


# ======================================================================= day-to-day form
_GH_X, _GH_W = np.polynomial.hermite_e.hermegauss(5)   # nodes/weights for N(0,1)
_GH_W = _GH_W / _GH_W.sum()


def match_dist_mix(pa, pb, best_of=3, sig_rel=0.0, sig_com=0.0):
    """Average the Markov result over match-level noise in logit space:
       rel: one player has a better day than the other (A up, B down) -> more lopsided matches
       com: both serve better/worse than usual (conditions, balls, altitude) -> totals move
    Constant-probability models ignore this and predict matches that are too close / too long."""
    la, lb = logit(pa), logit(pb)
    pw = 0.0; tot = defaultdict(float); marg = defaultdict(float)
    rel = [(0.0, 1.0)] if sig_rel == 0 else list(zip(_GH_X, _GH_W))
    com = [(0.0, 1.0)] if sig_com == 0 else list(zip(_GH_X, _GH_W))
    for zr, wr in rel:
        for zc, wc in com:
            p, t, m = match_dist_fast(sig(la + sig_rel * zr + sig_com * zc),
                                      sig(lb - sig_rel * zr + sig_com * zc), best_of)
            wt = wr * wc
            pw += wt * p
            for k, v in t.items(): tot[k] += wt * v
            for k, v in m.items(): marg[k] += wt * v
    return pw, dict(tot), dict(marg)
