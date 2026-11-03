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
SPREAD = re.compile(r"^([+-](\d+)?½?|PK)$")
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
                and not PRICE.match(l) and not TOTAL.match(l):
            p = {"player": l.title(), "event": event, "tour": tour}
            i += 1
            while i < len(lines) and not (lines[i].isupper() and not TOTAL.match(lines[i]) and not PRICE.match(lines[i])) \
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
                    v = t.replace("½", ".5").replace("PK", "0")
                    p["spread"] = float(v if v not in ("+.5", "-.5") else v.replace(".5", "0.5"))
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


def compare(fs, snap):
    """fs: parsed Fullstar rows. snap: latest snapshot DataFrame (pinnacle/kalshi/poly rows + model)."""
    import ratings
    import pointmodel as pm
    R = ratings.load()
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
    snap = pd.read_csv(snaps[-1]); snap = snap[snap.ts == snap.ts.max()]
    res = compare(fs, snap)
    res.insert(0, "ts", ts)
    out = ROOT / "data" / "fullstar_log.csv"
    res.to_csv(out, mode="a", header=not out.exists(), index=False)
    pd.set_option("display.width", 250)
    print(res.drop(columns=["ts", "event"]).round(3).to_string(index=False))
