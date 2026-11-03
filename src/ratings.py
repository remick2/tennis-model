"""Current ratings + name lookup, for pricing upcoming matches.

predict(tour, name_a, name_b, surface, best_of) -> dict with Elo, point-model and blend
probabilities for A, plus the total-games distribution (for totals markets).
"""
import pickle
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import backtest as b
import elo
import pointmodel as pm
from crosswalk import name_ok
from load import RAW, norm

CACHE = Path(__file__).resolve().parents[1] / "data" / "ratings.pkl"
POINT_PARAMS = {"atp": dict(kappa=1.0, sig_rel=0.2, delta=0.0), "wta": dict(kappa=1.4, sig_rel=0.2, delta=0.1)}
BLEND_W_POINT = {"atp": 0.4, "wta": 0.2}


class Ratings:
    def __init__(self, tour):
        self.tour = tour
        stream, _ = elo.build_stream(tour)
        preds, self.r, self.rs = elo.run(stream, mov=True, level_k=True, layoff=True)
        self.n = defaultdict(int)
        for w, l, st in zip(stream.w_id, stream.l_id, stream.status):
            if st == "done":
                self.n[w] += 1; self.n[l] += 1
        prm = b.tune(preds)
        self.w_blend, self.scale = prm["w_blend"], prm["scale"]
        self.base = pm.base_rates(stream)
        self.S, self.R, self.Ss, self.Rs = _final_skills(stream)
        self.last_date = stream.date.max()
        # injury/withdrawal signals: last match date and recent retirements/walkovers (as the loser)
        self.last_played = {}
        for w, l, d in zip(stream.w_id, stream.l_id, stream.date):
            self.last_played[w] = d; self.last_played[l] = d
        recent = stream[(stream.status.isin(["ret", "wo"])) & (stream.date >= self.last_date - pd.Timedelta(days=45))]
        self.recent_quit = {}
        for l, d, st, t in zip(recent.l_id, recent.date, recent.status, recent.tourney):
            self.recent_quit.setdefault(l, []).append(f"{'retired' if st == 'ret' else 'withdrew (W/O)'} {t} {d:%b %-d}")
        # names: Sackmann full names + odds-source short names -> id
        players = pd.read_csv(RAW / tour / f"{tour}_players.csv", dtype={"player_id": str}, low_memory=False)
        active = set(stream[stream.date >= "2024-01-01"].w_id) | set(stream[stream.date >= "2024-01-01"].l_id)
        players = players[players.player_id.isin(active)]
        self.full = {norm(f"{a} {c}"): pid for a, c, pid in
                     zip(players.name_first.fillna(""), players.name_last.fillna(""), players.player_id)}
        recent = stream[stream.date >= "2025-01-01"]
        self.short = dict(zip(recent.w_name, recent.w_id)) | dict(zip(recent.l_name, recent.l_id))

    def find(self, name):
        n = norm(name)
        if n in self.full:
            return self.full[n]
        hits = {pid for sn, pid in self.short.items() if name_ok(name, sn)}
        if len(hits) == 1:
            return hits.pop()
        hits = {pid for fn, pid in self.full.items() if sorted(fn.split()) == sorted(n.split())}
        return hits.pop() if len(hits) == 1 else None

    def predict(self, a, b_, surface="Hard", best_of=3):
        ia, ib = self.find(a), self.find(b_)
        if not ia or not ib:
            return {"error": f"unknown player: {a if not ia else b_}"}
        d_o = self.r.get(ia, 1500) - self.r.get(ib, 1500)
        d_s = self.rs.get((ia, surface), 1500) - self.rs.get((ib, surface), 1500)
        row = pd.DataFrame({"d_o": [d_o], "d_s": [d_s], "best_of": [best_of]})
        p_elo = float(elo.prob(row, self.w_blend, self.scale)[0])
        base = self.base.get(surface, self.base["_all"])
        la = base + self.S[ia] + self.Ss[(ia, surface)] - self.R[ib] - self.Rs[(ib, surface)]
        lb = base + self.S[ib] + self.Ss[(ib, surface)] - self.R[ia] - self.Rs[(ia, surface)]
        P = POINT_PARAMS[self.tour]
        c, d = (la + lb) / 2 + P["delta"], P["kappa"] * (la - lb) / 2
        p_pt, tot, marg = pm.match_dist_mix(pm.sig(c + d), pm.sig(c - d), best_of, P["sig_rel"])
        w = BLEND_W_POINT[self.tour]
        p_blend = float(pm.sig(w * pm.logit(p_pt) + (1 - w) * pm.logit(p_elo)))
        today = pd.Timestamp.now().normalize()
        days = lambda i: int((today - self.last_played[i]).days) if i in self.last_played else None
        return {"p_elo": p_elo, "p_point": float(p_pt), "p_model": p_blend,
                "days_off_a": days(ia), "days_off_b": days(ib),
                "quit_a": "; ".join(self.recent_quit.get(ia, [])), "quit_b": "; ".join(self.recent_quit.get(ib, [])),
                "n_a": self.n[ia], "n_b": self.n[ib], "totals": tot, "margin": marg,
                "pa": float(pm.sig(c + d)), "pb": float(pm.sig(c - d))}


def _final_skills(stream, lr=0.12, lr_surf=0.1):
    """Same update loop as pointmodel.run_skills, returning end-state skills."""
    base = pm.base_rates(stream)
    S = defaultdict(float); R = defaultdict(float); Ss = defaultdict(float); Rs = defaultdict(float)
    for w, l, surf, st, wsv, wsw, lsv, lsw in zip(stream.w_id, stream.l_id, stream.surface, stream.status,
                                                   stream.w_svpt, stream.w_spw, stream.l_svpt, stream.l_spw):
        if st != "done" or not np.all(np.isfinite([wsv, wsw, lsv, lsw])) or not (wsv > 0 and lsv > 0) \
                or wsw > wsv or lsw > lsv:
            continue
        bse = base.get(surf, base["_all"])
        for srv, ret, n_pts, won in ((w, l, wsv, wsw), (l, w, lsv, lsw)):
            ssrv, sret = (srv, surf), (ret, surf)
            g = (won / n_pts - pm.sig(bse + S[srv] + Ss[ssrv] - R[ret] - Rs[sret])) * n_pts / 80.0
            S[srv] += lr * g; R[ret] -= lr * g
            if surf in pm.SURFACES:
                Ss[ssrv] += lr_surf * g; Rs[sret] -= lr_surf * g
                Ss[ssrv] *= 0.999; Rs[sret] *= 0.999
    return S, R, Ss, Rs


def load(rebuild=False):
    if CACHE.exists() and not rebuild:
        return pickle.load(open(CACHE, "rb"))
    out = {t: Ratings(t) for t in ("atp", "wta")}
    pickle.dump(out, open(CACHE, "wb"))
    return out
