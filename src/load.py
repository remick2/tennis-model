"""Load + normalize match data into one chronological stream per tour.

Sources
- Sackmann archive (results, 2010 -> Roland Garros 2026): tour + Challenger/quals (ATP),
  tour + WTA125/ITF 50+ (WTA). Used for ratings.
- minmaxxxer odds dataset (main tour, Jan 2025 -> now, weekly): consensus closing odds.
  Used as the benchmark, and as the results feed after Sackmann's data ends.
"""
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
SACKMANN_END = 20260601  # Sackmann complete through RG 2026; odds source takes over after this

# Round order inside a tournament, so a player's earlier rounds update before later ones.
ROUND_ORDER = {r: i for i, r in enumerate(
    ["Q1", "Q2", "Q3", "Q4", "ER", "RR", "R128", "R64", "R32", "R16", "QF", "SF", "BR", "F"])}

# Levels used for ratings. ITF 15/25/35 skipped: tiny isolated pools that add noise, not signal.
WTA_KEEP = {"G", "PM", "P", "I", "F", "D", "C", "50", "60", "75", "80", "100"}
MAIN_LEVELS = {"G", "M", "A", "PM", "P", "I"}  # "main tour" for evaluation


def norm(s: str) -> str:
    """lowercase, strip accents/punctuation -> tokens separated by single spaces."""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z ]", " ", s.lower().replace("'", ""))
    return " ".join(s.split())


def _status(score: pd.Series) -> pd.Series:
    sc = score.fillna("").str.upper()
    return np.select([sc.str.contains("W/O|WALKOVER|DEF"), sc.str.contains("RET")],
                     ["wo", "ret"], "done")


def load_sackmann(tour: str) -> pd.DataFrame:
    files = sorted((RAW / tour).glob(f"{tour}_matches_20*.csv")) + \
            sorted((RAW / tour).glob(f"{tour}_matches_qual_*_20*.csv"))
    df = pd.concat([pd.read_csv(f, low_memory=False, dtype={"tourney_level": str}) for f in files])
    if tour == "wta":
        df = df[df.tourney_level.isin(WTA_KEEP)]
    df = df[df.tourney_date < SACKMANN_END]
    out = pd.DataFrame({
        "tour": tour,
        "date": pd.to_datetime(df.tourney_date.astype(int).astype(str)),
        "tourney": df.tourney_name, "level": df.tourney_level,
        "surface": df.surface.replace({"Carpet": "Hard"}),
        "best_of": df.best_of, "round": df["round"],
        "w_id": df.winner_id.astype(str), "l_id": df.loser_id.astype(str),
        "w_name": df.winner_name, "l_name": df.loser_name,
        "status": _status(df.score), "score": df.score, "src": "sack",
        "w_svpt": df.w_svpt, "w_spw": df.w_1stWon + df.w_2ndWon,
        "l_svpt": df.l_svpt, "l_spw": df.l_1stWon + df.l_2ndWon,
    })
    out["order"] = out["round"].map(ROUND_ORDER).fillna(6)
    return out


def load_odds(tour: str) -> pd.DataFrame:
    df = pd.concat([pd.read_csv(f) for f in sorted((RAW / "odds").glob(f"{tour}_matches_20*.csv"))])
    return pd.DataFrame({
        "tour": tour,
        "date": pd.to_datetime(df.tourney_date.astype(str)),
        "start": pd.to_datetime(df.start_time_utc, utc=True, errors="coerce"),
        "tourney": df.tourney_name, "level": df.tourney_level, "surface": df.surface,
        "best_of": df.best_of, "round": df["round"],
        "o_w_id": df.winner_id.astype(str), "o_l_id": df.loser_id.astype(str),
        "w_name": df.winner_name, "l_name": df.loser_name,
        "status": _status(df.score), "score": df.score, "match_id": df.match_id,
        "w_svpt": df.w_svpt, "w_spw": df.w_1stWon + df.w_2ndWon,
        "l_svpt": df.l_svpt, "l_spw": df.l_1stWon + df.l_2ndWon,
        "p_close": df.winner_close_prob, "p_open": df.winner_open_prob,
        "w_fair": df.winner_close_fair_odds, "l_fair": df.loser_close_fair_odds,
        "w_best": df.winner_best_close_odds, "l_best": df.loser_best_close_odds,
        "books": df.bookmakers, "margin": df.margin_pct,
    }).reset_index(drop=True)


def games(score):
    """'6-4 3-6 7-6(5)' -> (16, 16) winner/loser games; None if unparseable."""
    gw = gl = 0
    for a, b in re.findall(r"(\d+)-(\d+)", re.sub(r"\(\d+\)|\[\d+\]", "", str(score))):
        gw += int(a); gl += int(b)
    return (gw, gl) if gw + gl > 0 else None
