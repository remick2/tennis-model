"""Map odds-source player ids ("Sinner J.") to Sackmann ids ("Jannik Sinner").

Why match on *matches* not names: "Cerundolo F." vs "Cerundolo J. M." or two "Zhang Z."s
are ambiguous by name, but (date, both players, result) pins down a match uniquely.
Players only seen after Sackmann ends fall back to a name rule, else get a fresh id.
"""
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

from load import RAW, SACKMANN_END, norm


def parse_odds_name(name: str):
    """'Cerundolo J. M.' -> ('cerundolo', 'j');  'Van De Zandschulp B.' -> ('van de zandschulp', 'b')"""
    toks = str(name).split()
    sur = [t for t in toks if not t.endswith(".")]
    ini = [t for t in toks if t.endswith(".")]
    return norm(" ".join(sur)), (norm(ini[0])[:1] if ini else "")


def name_ok(sack_full: str, odds_name: str) -> bool:
    """Surname + first initial, in either name order ('Bu Yunchaokete' vs 'Bu Y.')."""
    sur, ini = parse_odds_name(odds_name)
    s = norm(sack_full)
    if not sur:
        return False
    if s == sur or sorted(s.split()) == sorted(sur.split()):
        return True
    western = s.endswith(" " + sur) and s.startswith(ini)
    eastern = s.startswith(sur + " ") and s[len(sur) + 1:].startswith(ini)
    return western or eastern


def build(sack: pd.DataFrame, odds: pd.DataFrame, tour: str) -> dict:
    # --- 1) match-based: overlap window where both sources have the same matches
    s = sack[(sack.date >= "2024-12-15")].sort_values("date").reset_index(drop=True)
    s_dates = s.date.values
    s_rows = list(s.itertuples())

    votes = defaultdict(Counter)
    o = odds[odds.date < pd.Timestamp(str(SACKMANN_END))]
    win = pd.Timedelta(days=8)
    for r in o.itertuples():
        lo = s_dates.searchsorted(np.datetime64(r.date - win))
        hi = s_dates.searchsorted(np.datetime64(r.date + win), side="right")
        cands = [c for c in s_rows[lo:hi]
                 if name_ok(c.w_name, r.w_name) and name_ok(c.l_name, r.l_name)]
        if len(cands) >= 1 and len({(c.w_id, c.l_id) for c in cands}) == 1:
            votes[r.o_w_id][cands[0].w_id] += 1
            votes[r.o_l_id][cands[0].l_id] += 1
    mapping = {oid: c.most_common(1)[0][0] for oid, c in votes.items()}

    # --- 2) name fallback for players not seen in the overlap (e.g. debuted after June 2026)
    players = pd.read_csv(RAW / tour / f"{tour}_players.csv", dtype={"player_id": str}, low_memory=False)
    recent_ids = set(sack[sack.date >= "2022-01-01"].w_id) | set(sack[sack.date >= "2022-01-01"].l_id)
    players = players[players.player_id.isin(recent_ids)]
    full = (players.name_first.fillna("") + " " + players.name_last.fillna("")).tolist()
    pid = players.player_id.tolist()
    names = dict(zip(odds.o_w_id, odds.w_name)) | dict(zip(odds.o_l_id, odds.l_name))
    n_fallback = n_new = 0
    for oid, nm in names.items():
        if oid in mapping:
            continue
        hits = [p for p, f in zip(pid, full) if name_ok(f, nm)]
        if len(hits) == 1 and hits[0] not in mapping.values():
            mapping[oid] = hits[0]; n_fallback += 1
        else:
            mapping[oid] = "new:" + oid; n_new += 1
    print(f"[{tour}] crosswalk: {len(votes)} by match, {n_fallback} by name, {n_new} new ids")
    return mapping
