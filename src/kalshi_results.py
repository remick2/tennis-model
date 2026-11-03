"""Challenger results after Sackmann's data ends (June 2026), from Kalshi's settled match markets.

Each Kalshi match = an event with 2 markets ("X wins"); the one that settled 'yes' is the winner.
Rules say a player wins "after a ball has been played", so retirements count as wins (we can't
tell them apart: small noise); walkovers settle at a fair price -> no 'yes' -> skipped.
Writes data/results_kalshi.csv (committed, updated incrementally by the scheduled job).
"""
import re
import time
from pathlib import Path

import pandas as pd
import requests

from load import RAW, norm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "results_kalshi.csv"
API = "https://api.elections.kalshi.com/trade-api/v2/markets"
SERIES = {"KXATPCHALLENGERMATCH": "atp", "KXWTACHALLENGERMATCH": "wta"}
RULE = re.compile(r"wins the (.+?) professional tennis match in the (\d{4}) (.+?) "
                  r"(Round Of \d+|Qualification.*?|Quarterfinals?|Semifinals?|Finals?|Final)\b", re.I)


def _get(params):
    for a in range(6):
        r = requests.get(API, params=params, timeout=60)
        if r.status_code == 200:
            return r.json()
        time.sleep(2 ** a)
    r.raise_for_status()


def fetch(min_close_ts=None):
    rows = []
    for series, tour in SERIES.items():
        cur, ms = None, []
        while True:
            p = {"series_ticker": series, "status": "settled", "limit": 1000}
            if cur: p["cursor"] = cur
            if min_close_ts: p["min_close_ts"] = int(min_close_ts)
            d = _get(p)
            ms += d.get("markets", [])
            cur = d.get("cursor")
            if not cur or not d.get("markets"):
                break
            time.sleep(0.3)
        by_ev = {}
        for m in ms:
            by_ev.setdefault(m["event_ticker"], []).append(m)
        for ev, pair in by_ev.items():
            win = [m for m in pair if m.get("result") == "yes"]
            if len(pair) != 2 or len(win) != 1:
                continue
            w = win[0]; l = [m for m in pair if m is not w][0]
            g = RULE.search(w.get("rules_primary", ""))
            rows.append({"event": ev, "tour": tour, "date": w.get("occurrence_datetime", "")[:10],
                         "tourney": g.group(3) if g else "", "round": g.group(4) if g else "",
                         "w_name": w.get("yes_sub_title"), "l_name": l.get("yes_sub_title")})
    return pd.DataFrame(rows)


def update():
    """Refetch the last ~10 days and merge, or everything if no file yet."""
    old = pd.read_csv(OUT) if OUT.exists() else pd.DataFrame()
    since = (pd.Timestamp(old.date.max()) - pd.Timedelta(days=10)).timestamp() if len(old) else None
    new = fetch(since)
    df = pd.concat([old, new]).drop_duplicates("event", keep="last").sort_values(["date", "event"])
    df.to_csv(OUT, index=False)
    return df


# --------------------------------------------------------------- surfaces + ids
def surface_map(tour):
    """City -> most recent surface, from Sackmann's Challenger/WTA125 history (2022+)."""
    files = sorted((RAW / tour).glob(f"{tour}_matches_qual_*_202*.csv"))
    d = pd.concat([pd.read_csv(f, usecols=["tourney_name", "surface", "tourney_date"], low_memory=False) for f in files])
    d = d.sort_values("tourney_date")
    d["city"] = d.tourney_name.map(_city)
    m = d.dropna(subset=["surface"]).groupby("city").surface.last().to_dict()
    # cities new since 2022 (checked by hand); anything else unknown defaults to Hard
    m.update({"plovdiv": "Clay", "catania": "Clay", "palermo": "Clay", "fort": "Hard", "ningbo": "Hard",
              "roehampton": "Grass", "kingston": "Grass"})
    return m


def _city(name):
    s = norm(re.sub(r"\b(ATP|WTA|Challenger|CH|125k?|Open|II|III|IV|\d{1,4})\b", " ", str(name), flags=re.I))
    return s.split()[0] if s else ""


def to_stream(df, tour, find_id):
    """Rows in the Elo stream's format. find_id(name) -> player id or None."""
    smap = surface_map(tour)
    d = df[df.tour == tour].copy()
    d["surface"] = d.tourney.map(lambda t: smap.get(_city(t), "Hard"))
    d["surface_known"] = d.tourney.map(lambda t: _city(t) in smap)
    d["w_id"] = [find_id(n) or f"k:{norm(n)}" for n in d.w_name]
    d["l_id"] = [find_id(n) or f"k:{norm(n)}" for n in d.l_name]
    out = pd.DataFrame({
        "tour": tour, "date": pd.to_datetime(d.date), "tourney": d.tourney, "level": "C",
        "surface": d.surface, "best_of": 3, "round": d["round"], "w_id": d.w_id, "l_id": d.l_id,
        "w_name": d.w_name, "l_name": d.l_name, "status": "done", "score": None, "src": "kalshi",
        "order": 6.0})
    return out, d.surface_known.mean()


if __name__ == "__main__":
    df = update()
    print(df.groupby(["tour", df.date.str[:7]]).size())
