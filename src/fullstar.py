"""Fullstar (no API): parse the page text of its TENNIS ATP/WTA - MATCHUPS view, captured
through Remick's Chrome, and compare against the sharp reference + Kalshi/Polymarket + model.

Reference ("fair") = Pinnacle no-vig if the Odds API has the match, else the mid of
Kalshi/Polymarket (they track the sharp line closely, as the first snapshots showed).
Fullstar EV per $1 = ref_prob * decimal_odds - 1. Totals use the point model calibrated to
the reference moneyline (the setup that scored best in the backtest).
"""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from load import norm

ROOT = Path(__file__).resolve().parents[1]
PRICE = re.compile(r"^([+-]\d{3,}|EV)$")
SPREAD = re.compile(r"^([+-](\d+)?½?|PK)( EV)?$")  # "+2½ EV" = spread with its price inline
TOTAL = re.compile(r"^([ou])(\d+)(½)?( EV)?$")
TIME = re.compile(r"^\d{1,2}:\d{2} [AP]M$")


def dec(american):
    if american == "EV":
        return 2.0
    a = int(american)
    return 1 + (a / 100 if a > 0 else 100 / -a)


def parse(text, tour):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    rows, i, event = [], 0, None
    while i < len(lines):
        l = lines[i]
        if re.match(r"^(ATP|WTA|CHALLENGER|ITF)\b.* - ", l) or l.startswith(("ATP -", "WTA -")):
            event = l; i += 1; continue
        if l.isupper() and not TIME.match(l) and not l.startswith("TENNIS") and not re.match(r"^[A-Z]{3} \d{2}$", l) \
                and not PRICE.match(l) and not TOTAL.match(l) and not SPREAD.match(l):
            p = {"player": l.title(), "event": event, "tour": tour}
            i += 1
            while i < len(lines) and not (lines[i].isupper() and not TOTAL.match(lines[i]) and not PRICE.match(lines[i])
                                          and not SPREAD.match(lines[i])) \
                    and not TIME.match(lines[i]):
                t = lines[i]
                if TOTAL.match(t):
                    m = TOTAL.match(t)
                    p["total_side"], p["total_line"] = m.group(1), int(m.group(2)) + (0.5 if m.group(3) else 0)
                    if m.group(4):
                        p["total_price"] = "EV"
                    else:
                        i += 1; p["total_price"] = lines[i]
                elif SPREAD.match(t) and not PRICE.match(t):
                    m = SPREAD.match(t)
                    v = m.group(1).replace("½", ".5").replace("PK", "0")
                    p["spread"] = float(v if v not in ("+.5", "-.5") else v.replace(".5", "0.5"))
                    if m.group(3):
                        p["spread_price"] = "EV"
                    else:
                        i += 1; p["spread_price"] = lines[i]
                elif PRICE.match(t):
                    p["ml"] = t
                i += 1
            rows.append(p)
            continue
        i += 1
    # pair consecutive players into matches
    out = []
    for a, b in zip(rows[::2], rows[1::2]):
        a["opp"], b["opp"] = b["player"], a["player"]
        out += [a, b]
    df = pd.DataFrame(out)
    for c in ("ml", "total_price", "spread_price"):
        if c in df:
            df[c + "_dec"] = df[c].map(lambda x: dec(x) if isinstance(x, str) else None)
    return df


def fs_stake(p, d, bankroll=700.0):
    """Quarter Kelly off the reference prob, capped at 2%. Fullstar minimum: risk $10, or enough to
    win $10 on minus odds, whichever is larger. Below the minimum = no bet (not 'bet the minimum')."""
    f = 0.25 * (p * d - 1) / (d - 1)
    risk = max(0.0, min(f, 0.02)) * bankroll
    min_risk = max(10.0, 10.0 / (d - 1))
    return round(risk, 2) if risk >= min_risk else 0.0


KALSHI = "https://api.elections.kalshi.com/trade-api/v2/markets"
K_TOT = re.compile(r".*in the (.+?) vs (.+?) professional tennis match")
K_SPR = re.compile(r"in favor of (.+?) across the full match is above ([\d.]+) games in the (.+?) vs (.+?) professional")


def kalshi_lines():
    """Open Kalshi total-games and game-spread markets -> list of dicts with names, line, mid."""
    import requests
    out = []
    for series, kind in (("KXATPGTOTAL", "total"), ("KXWTAGTOTAL", "total"), ("KXATPGSPREAD", "spread")):
        try:
            ms = requests.get(KALSHI, params={"series_ticker": series, "status": "open", "limit": 1000},
                              timeout=30).json().get("markets", [])
        except Exception:
            continue
        for m in ms:
            b, a = float(m.get("yes_bid_dollars") or 0), float(m.get("yes_ask_dollars") or 0)
            if not (0 < b and a < 1 and a - b <= 0.10):
                continue
            r = m.get("rules_primary", "")
            if kind == "total":
                g, L = K_TOT.search(r), re.search(r"Over ([\d.]+)", m.get("title", ""))
                if g and L:
                    out.append({"kind": kind, "a": g.group(1), "b": g.group(2), "x": None,
                                "line": float(L.group(1)), "mid": (a + b) / 2})
            else:
                g = K_SPR.search(r)
                if g:
                    out.append({"kind": kind, "a": g.group(3), "b": g.group(4), "x": g.group(1),
                                "line": float(g.group(2)), "mid": (a + b) / 2})
    return out


def kalshi_checks(r, kl, same):
    """EV of Fullstar's total and spread on this row vs Kalshi's mid at the SAME line (no interpolation)."""
    res = {}
    mine = [k for k in kl if (same(k["a"], r.player) and same(k["b"], r.opp)) or (same(k["a"], r.opp) and same(k["b"], r.player))]
    if getattr(r, "total_side", None) in ("o", "u") and isinstance(getattr(r, "total_price", None), str):
        t = [k for k in mine if k["kind"] == "total" and k["line"] == r.total_line]
        if t:
            p = t[0]["mid"] if r.total_side == "o" else 1 - t[0]["mid"]
            res.update(k_total_p=p, k_total_ev=p * dec(r.total_price) - 1)
    sp = getattr(r, "spread", None)
    if sp == sp and sp is not None and isinstance(getattr(r, "spread_price", None), str) and sp != 0:
        if sp < 0:   # player must win by more than |sp|
            t = [k for k in mine if k["kind"] == "spread" and same(k["x"], r.player) and k["line"] == -sp]
            p = t[0]["mid"] if t else None
        else:        # player covers +sp unless opp wins by more than sp
            t = [k for k in mine if k["kind"] == "spread" and same(k["x"], r.opp) and k["line"] == sp]
            p = 1 - t[0]["mid"] if t else None
        if p is not None:
            res.update(k_spread_p=p, k_spread_ev=p * dec(r.spread_price) - 1)
    return res


def compare(fs, snap):
    """fs: parsed Fullstar rows. snap: latest snapshot DataFrame (pinnacle/kalshi/poly rows + model)."""
    import ratings
    import pointmodel as pm
    from snapshot import _toks
    R = ratings.load()
    kl = kalshi_lines()
    same = lambda x, y: bool(_toks(x)) and bool(_toks(y)) and (_toks(x) <= _toks(y) or _toks(y) <= _toks(x))
    last = lambda n: norm(n).split()[-1]
    snap = snap.copy()
    snap["k"] = [(last(a), last(b)) for a, b in zip(snap.player, snap.opp)]
    out = []
    for r in fs.itertuples():
        k = (last(r.player), last(r.opp))
        s = snap[snap.k == k]
        pin = s[s.source == "pinnacle"].fair
        mids = s[s.source.isin(["kalshi", "poly"])].eval("(bid + ask) / 2").dropna()
        ref, ref_src = (float(pin.iloc[0]), "pinnacle") if len(pin) else \
            ((float(mids.mean()), "kalshi/poly mid") if len(mids) else (None, None))
        row = {"tour": r.tour, "player": r.player, "opp": r.opp, "event": r.event,
               "fs_ml": r.ml if isinstance(r.ml, str) else None, "ref": ref, "ref_src": ref_src}
        if row["fs_ml"]:
            d = dec(r.ml)
            row["fs_implied"] = 1 / d
            row["ml_ev_vs_ref"] = ref * d - 1 if ref else None
        pred = R[r.tour].predict(r.player, r.opp, "Hard", 3)
        row["p_model"] = pred.get("p_model")
        row["ml_ev_vs_model"] = (pred["p_model"] * dec(r.ml) - 1) if "p_model" in pred and row["fs_ml"] else None
        # size when the price beats the reference by 2%+ (price only, decision 2026-11-03; model = info)
        ok = row.get("ml_ev_vs_ref") is not None and row["ml_ev_vs_ref"] >= 0.02
        row["paper_risk"] = fs_stake(ref, dec(r.ml)) if ok else 0.0
        # totals: shift the point model so P(win) = reference, then P(over line)
        if getattr(r, "total_side", None) in ("o", "u") and ref and "pa" in pred:
            pa, pb = pred["pa"], pred["pb"]
            la, lb = pm.logit(pa), pm.logit(pb)
            lo, hi = -1.5, 1.5
            for _ in range(14):
                mid = (lo + hi) / 2
                p = pm.match_dist_mix(pm.sig(la + mid), pm.sig(lb - mid), 3, ratings.POINT_PARAMS[r.tour]["sig_rel"])[0]
                lo, hi = (mid, hi) if p < ref else (lo, mid)
            _, tot, _ = pm.match_dist_mix(pm.sig(la + (lo + hi) / 2), pm.sig(lb - (lo + hi) / 2), 3,
                                          ratings.POINT_PARAMS[r.tour]["sig_rel"])
            p_over = sum(v for g, v in tot.items() if g > r.total_line)
            p_side = p_over if r.total_side == "o" else 1 - p_over
            row.update(total=f"{r.total_side}{r.total_line}", total_price=r.total_price,
                       p_total_side=p_side, total_ev=p_side * dec(r.total_price) - 1)
        row.update(spread=getattr(r, "spread", None), spread_price=getattr(r, "spread_price", None))
        row.update(kalshi_checks(r, kl, same))
        for c in ("k_total_ev", "k_spread_ev"):  # paper-size totals/spreads that beat Kalshi's price by 2%+
            if (row.get(c) or -1) >= 0.02:
                pr = row["k_total_p"] if c == "k_total_ev" else row["k_spread_p"]
                px = r.total_price if c == "k_total_ev" else r.spread_price
                row[c.replace("_ev", "_risk")] = fs_stake(pr, dec(px))
        out.append(row)
    return pd.DataFrame(out)


if __name__ == "__main__":
    ts = datetime.now(timezone.utc).isoformat()
    frames = []
    for f in sys.argv[1:]:
        tour = "wta" if "wta" in f.lower() else "atp"
        frames.append(parse(Path(f).read_text(), tour))
    fs = pd.concat(frames, ignore_index=True)
    snaps = sorted((ROOT / "data" / "snapshots").glob("20*.csv"))
    snap = pd.concat([pd.read_csv(f, low_memory=False) for f in snaps[-2:]])
    snap["t"] = pd.to_datetime(snap.ts, utc=True, format="ISO8601")
    mk = snap[(snap.t == snap.t.max()) & (snap.source != "pinnacle")]
    pin = snap[(snap.source == "pinnacle") & (snap.t >= snap.t.max() - pd.Timedelta(hours=6))]
    pin = pin[pin.t == pin.t.max()] if len(pin) else pin       # Pinnacle is pulled every 2-4h, not every cycle
    snap = pd.concat([mk, pin]).drop(columns="t")
    res = compare(fs, snap)
    res.insert(0, "ts", ts)
    out = ROOT / "data" / "fullstar_log.csv"
    old = pd.read_csv(out) if out.exists() else pd.DataFrame()
    pd.concat([old, res], ignore_index=True).to_csv(out, index=False)  # union of columns, never misaligned
    pd.set_option("display.width", 250)
    print(res.drop(columns=["ts", "event"]).round(3).to_string(index=False))
