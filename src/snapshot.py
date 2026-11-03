"""Phase 2 snapshot: Pinnacle (sharp reference) vs Kalshi vs Polymarket vs our model.

Every run appends one row per (match, side, source) to data/snapshots/YYYY-MM-DD.csv with a
UTC timestamp, so the last snapshot before start = our closing line. PAPER ONLY.

Edge math (per side, buying 1 contract that pays $1):
  all-in cost   = ask + taker fee  (Kalshi 0.07*p*(1-p), Polymarket 0.05*p*(1-p))
  price edge    = Pinnacle no-vig prob - all-in cost       (is the price good?)
  model edge    = our model prob     - all-in cost         (is it our read too?)
  FLAG only when both clear MIN_EDGE (the "own read AND good price" rule). Sub-2c gaps are
  inside the noise of de-vigging Pinnacle and of quote timing, so they don't count.
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

from load import norm

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "data" / "snapshots"
_kf = ROOT / "secrets" / "odds_api_key"
KEY = os.environ.get("ODDS_API_KEY") or (_kf.read_text().strip() if _kf.exists() else "")
# Free tier = 500 credits/month, so Pinnacle is only pulled every 4h (UTC hours 0,4,8,...)
# unless forced; Kalshi/Polymarket are free and pulled every run.
USE_PINNACLE = os.environ.get("PINNACLE", "auto")
KALSHI = "https://api.elections.kalshi.com/trade-api/v2"
GAMMA = "https://gamma-api.polymarket.com"
FEE = {"kalshi": 0.07, "poly": 0.05}
MIN_EDGE = 0.02
COLUMNS = ["ts", "source", "tour", "level", "event", "tourney", "player", "opp", "key", "start",
           "bid", "ask", "ask_size", "volume", "liquidity", "price", "fair", "book_update",
           "fee", "cost", "pin_fair", "p_model", "p_elo", "surface", "surface_known", "model_err",
           "n_player", "n_opp", "price_edge", "model_edge", "flag"]
KALSHI_ML = {"KXATPMATCH": ("atp", "main"), "KXWTAMATCH": ("wta", "main"),
             "KXATPCHALLENGERMATCH": ("atp", "challenger"), "KXWTACHALLENGERMATCH": ("wta", "challenger")}
POLY_SERIES = {"10365": "atp", "10366": "wta"}

# Surfaces for events running now. Anything unknown defaults to Hard and is flagged.
SURFACE_HINTS = {"paris": "Hard", "finals": "Hard", "turin": "Hard", "riyadh": "Hard", "athens": "Hard",
                 "metz": "Hard", "belgrade": "Hard", "jiujiang": "Hard", "montevideo": "Clay",
                 "lima": "Clay", "guayaquil": "Clay", "buenos aires": "Clay", "santiago": "Clay",
                 "temuco": "Hard", "brasilia": "Hard", "sao paulo": "Clay", "florianopolis": "Clay",
                 "yokkaichi": "Hard", "kobe": "Hard", "champaign": "Hard", "knoxville": "Hard",
                 "charlottesville": "Hard", "drummondville": "Hard", "bergamo": "Hard", "helsinki": "Hard",
                 "ortisei": "Hard", "maia": "Clay", "puerto vallarta": "Hard", "merida": "Hard",
                 "andorra": "Hard", "tenerife": "Hard", "funchal": "Hard", "manila": "Hard",
                 "st. tropez": "Hard", "st tropez": "Hard", "bari": "Hard", "trnava": "Hard"}


def now():
    return datetime.now(timezone.utc)


def key_for(a, b):
    last = lambda n: norm(n).split()[-1] if norm(n) else ""
    return frozenset((last(a), last(b)))


def surface_for(text):
    t = (text or "").lower()
    for k, s in SURFACE_HINTS.items():
        if k in t:
            return s, True
    return "Hard", False


# ------------------------------------------------------------------ sources
def pinnacle():
    if not KEY or USE_PINNACLE == "0" or (USE_PINNACLE == "auto" and now().hour % 4 >= 2):
        return [], None
    sports = requests.get("https://api.the-odds-api.com/v4/sports", params={"apiKey": KEY}, timeout=30).json()
    keys = [s["key"] for s in sports if s["key"].startswith("tennis_") and s["active"]]
    rows, remaining = [], None
    for k in keys:
        r = requests.get(f"https://api.the-odds-api.com/v4/sports/{k}/odds", timeout=30,
                         params={"apiKey": KEY, "regions": "eu", "markets": "h2h",
                                 "bookmakers": "pinnacle", "oddsFormat": "decimal"})
        remaining = r.headers.get("x-requests-remaining")
        for e in r.json():
            for bm in e.get("bookmakers", []):
                o = bm["markets"][0]["outcomes"]
                if len(o) != 2:
                    continue
                inv = [1 / x["price"] for x in o]
                for i, x in enumerate(o):
                    rows.append({"source": "pinnacle", "tour": "atp" if "_atp_" in k else "wta",
                                 "event": k, "start": e["commence_time"], "player": x["name"],
                                 "opp": o[1 - i]["name"], "fair": inv[i] / sum(inv), "price": x["price"],
                                 "book_update": bm["last_update"]})
    return rows, remaining


def kalshi():
    rows = []
    for series, (tour, level) in KALSHI_ML.items():
        ms = requests.get(f"{KALSHI}/markets", params={"series_ticker": series, "status": "open", "limit": 1000},
                          timeout=30).json().get("markets", [])
        by_event = {}
        for m in ms:
            by_event.setdefault(m["event_ticker"], []).append(m)
        for ev, pair in by_event.items():
            if len(pair) != 2:
                continue
            for i, m in enumerate(pair):
                ask = float(m.get("yes_ask_dollars") or 0) or None
                bid = float(m.get("yes_bid_dollars") or 0) or None
                tourney = re.search(r"in the \d{4} (.+?) (Round|Qualif|Final|Semi|Quarter)", m.get("rules_primary", ""))
                rows.append({"source": "kalshi", "tour": tour, "level": level, "event": ev,
                             "tourney": tourney.group(1) if tourney else "",
                             "player": m.get("yes_sub_title"), "opp": pair[1 - i].get("yes_sub_title"),
                             "bid": bid, "ask": ask, "ask_size": float(m.get("yes_ask_size_fp") or 0),
                             "volume": float(m.get("volume_fp") or 0), "start": m.get("occurrence_datetime")})
    return rows


def polymarket():
    rows = []
    for sid, tour in POLY_SERIES.items():
        evs = requests.get(f"{GAMMA}/events", params={"series_id": sid, "closed": "false", "limit": 500},
                           timeout=30).json()
        for e in evs:
            ml = [m for m in e.get("markets", []) if m.get("sportsMarketType") == "moneyline"]
            if not ml or not ml[0].get("acceptingOrders"):
                continue
            m = ml[0]
            names = json.loads(m["outcomes"])
            bb, ba = m.get("bestBid"), m.get("bestAsk")
            if len(names) != 2 or bb is None or ba is None:
                continue
            start = (m.get("gameStartTime") or "").replace(" ", "T").replace("+00", "Z")
            tourney = e["title"].split(":")[0]
            # bestBid/bestAsk are for outcome 0; outcome 1's ask = 1 - outcome 0's bid
            for i, (bid, ask) in enumerate([(bb, ba), (1 - ba, 1 - bb)]):
                rows.append({"source": "poly", "tour": tour, "event": e["slug"], "tourney": tourney,
                             "player": names[i], "opp": names[1 - i], "bid": bid, "ask": ask,
                             "liquidity": float(e.get("liquidity") or 0), "start": start})
    return rows


# ------------------------------------------------------------------ assemble
def build(model=True):
    t0 = now()
    pin, remaining = pinnacle()
    df = pd.DataFrame(pin + kalshi() + polymarket())
    df["ts"] = t0.isoformat()
    df["key"] = [key_for(a, b) for a, b in zip(df.player, df.opp)]
    df["start"] = pd.to_datetime(df.start, utc=True, errors="coerce")
    # Pinnacle start times are the most reliable; copy them onto other sources' rows
    pin_start = df[df.source == "pinnacle"].groupby("key").start.first()
    if len(pin_start):
        df["start"] = df.key.map(pin_start.to_dict()).fillna(df.start)
    df = df[df.start.isna() | (df.start > t0)]  # pre-match only
    if "fair" not in df:
        df["fair"] = float("nan")
    fair = df[df.source == "pinnacle"].set_index(["key", "player"]).fair
    df["pin_fair"] = [fair.get((k, p)) for k, p in zip(df.key, df.player)]
    df["fee"] = [FEE.get(s, 0) * a * (1 - a) if a == a and a else 0 for s, a in zip(df.source, df.ask)]
    df["cost"] = df.ask + df.fee
    if model:
        import ratings
        R = ratings.load()
        probs = []
        for r in df.itertuples():
            surf, known = surface_for(f"{r.tourney if isinstance(r.tourney, str) else ''} {r.event}")
            p = R[r.tour].predict(r.player, r.opp, surf, 3)
            probs.append({"p_model": p.get("p_model"), "p_elo": p.get("p_elo"), "surface": surf,
                          "surface_known": known, "model_err": p.get("error"),
                          "n_player": p.get("n_a"), "n_opp": p.get("n_b")})
        df = pd.concat([df.reset_index(drop=True), pd.DataFrame(probs)], axis=1)
        df["model_edge"] = df.p_model - df.cost
    df["price_edge"] = df.pin_fair - df.cost
    df["flag"] = (df.price_edge >= MIN_EDGE) & (df.get("model_edge", 0) >= MIN_EDGE)
    df["key"] = df.key.map(lambda k: " v ".join(sorted(k)))
    SNAP.mkdir(parents=True, exist_ok=True)
    out = SNAP / f"{t0:%Y-%m-%d}.csv"
    df = df.reindex(columns=COLUMNS)  # fixed schema so appended runs line up
    df.to_csv(out, mode="a", header=not out.exists(), index=False)
    return df, remaining


if __name__ == "__main__":
    df, remaining = build(model="--no-model" not in sys.argv)
    print(f"odds-api credits left: {remaining}")
    cols = ["source", "tour", "player", "opp", "start", "ask", "cost", "pin_fair", "p_model",
            "price_edge", "model_edge", "flag", "surface"]
    show = df[df.source != "pinnacle"].sort_values(["start", "key"])
    print(show[[c for c in cols if c in show]].round(3).to_string(index=False))
