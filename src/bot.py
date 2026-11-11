"""DRY-RUN arbitrage bot: Kalshi + Polymarket US. Places NO real orders and holds no keys.

What it does, every ~2s, for the matches most likely to arb (every live match on both venues,
plus pre-match ones within 2c of an arb):
  1. reads all order books at once (Kalshi: both players' tickers; Polymarket US: the match book)
  2. for every cross-venue way to hold both players (Kalshi YES on A / NO on B's ticker, Polymarket US
     long / short), walks both ladders together, buying pairs while each extra pair costs < $1 after fees,
     capped by the paper cash sitting on each venue
  3. if the whole order would net >= $1: "fires" two limit IOC orders (logged exactly as they'd be sent),
     then re-reads both books to see what would actually have filled at those limits (one API round trip
     later, about when real orders would land)
  4. if one leg fills short: first tries to buy the missing shares on that venue at break-even or better,
     then sells any leftover shares on the other leg at the bid (the "unwind"), and books the loss
  5. holds hedged pairs to settlement and pays each venue its winning leg (Kalshi result; Polymarket US
     settles the same way: walkover = last fair price, retirement = official winner)

The paper ledger (data/bot/ledger.json) starts with $345 on each venue and carries across runs, so it
shows real-world limits too: cash locked in open matches, and winnings piling up on one venue.
Liquidity the bot "took" is subtracted from later book reads for 2 minutes so it can't fill twice.

Run: python bot.py --minutes 340 [--interval 2] [--no-git]
"""
import argparse
import json
import math
import os
import subprocess
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests

import arbscan as A

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bot"
LEDGER = OUT / "ledger.json"
START_CASH = {"kalshi": 345.0, "polyus": 345.0}   # Remick's ~$690, split evenly
FEE = A.FEE
MIN_PROFIT = 1.00        # fire only if the whole order nets >= $1 after fees (same bar as the gate)
MIN_EDGE = 0.001         # every marginal pair must clear $1 by at least 0.1c
MAX_MATCHES = 10         # ~20 Kalshi + 10 Polymarket US book reads per cycle: inside both rate limits
REFRESH = 60             # seconds between full market-list refreshes
CONSUME_SECS = 120       # how long liquidity we "took" stays out of later book reads
RUN = os.environ.get("GITHUB_RUN_ID", "local")
_tl = threading.local()


def sess():
    if not hasattr(_tl, "s"):
        _tl.s = requests.Session()
    return _tl.s


def fast_get(url):
    """One quick try (the hot loop can't wait on retries). Returns (json or None, seconds)."""
    t = time.time()
    try:
        r = sess().get(url, timeout=4)
        return (r.json() if r.status_code == 200 else None), time.time() - t
    except (requests.RequestException, ValueError):
        return None, time.time() - t


def ceil_cent(x):
    return math.ceil(round(x * 100, 6)) / 100


# ------------------------------------------------------------------ books
# An instrument is (venue, book_id, how): Kalshi ("kalshi", ticker, "yes"|"no"), Polymarket US
# ("polyus", slug, "0"|"1"). Each book gives an ASK ladder (what buying costs) and a BID ladder (what
# selling pays), ascending / descending by price, as [(price, qty)].
def read_book(venue, book_id):
    if venue == "kalshi":
        d, secs = fast_get(f"{A.KALSHI}/markets/{book_id}/orderbook")
        ob = (d or {}).get("orderbook_fp")
        if ob is None:
            return None, secs
        yb = [(float(p), float(q)) for p, q in ob.get("yes_dollars") or []]
        nb = [(float(p), float(q)) for p, q in ob.get("no_dollars") or []]
        return {"yes": {"ask": sorted((round(1 - p, 4), q) for p, q in nb), "bid": sorted(yb, reverse=True)},
                "no": {"ask": sorted((round(1 - p, 4), q) for p, q in yb), "bid": sorted(nb, reverse=True)}}, secs
    d, secs = fast_get(f"{A.POLYUS}/v1/markets/{book_id}/book")
    b = (d or {}).get("marketData")
    if b is None:
        return None, secs
    off = [(float(x["px"]["value"]), float(x["qty"])) for x in (b.get("offers") or b.get("asks") or [])]
    bid = [(float(x["px"]["value"]), float(x["qty"])) for x in (b.get("bids") or [])]
    return {"0": {"ask": sorted(off), "bid": sorted(bid, reverse=True)},
            "1": {"ask": sorted((round(1 - p, 4), q) for p, q in bid),
                  "bid": sorted(((round(1 - p, 4), q) for p, q in off), reverse=True)}}, secs


def read_books(ids, pool):
    """All books at once. Returns ({(venue, id): book}, slowest read in seconds)."""
    res = list(pool.map(lambda vi: read_book(*vi), ids))
    return {vi: b for vi, (b, _) in zip(ids, res) if b is not None}, max((s for _, s in res), default=0)


# ------------------------------------------------------------------ order sizing
class Consumed:
    """Liquidity the paper bot already took, so later reads don't fill it twice."""
    def __init__(self):
        self.d = {}

    def add(self, inst, fills):
        exp = time.time() + CONSUME_SECS
        for p, q in fills:
            k = (inst, round(p, 4))
            self.d[k] = (self.d.get(k, (0, 0))[0] + q, exp)

    def adjust(self, inst, ladder):
        now = time.time()
        self.d = {k: v for k, v in self.d.items() if v[1] > now}
        return [(p, q - self.d.get((inst, round(p, 4)), (0, 0))[0]) for p, q in ladder
                if q - self.d.get((inst, round(p, 4)), (0, 0))[0] > 1e-9]


def unit_cost(p, f):
    return p + f * p * (1 - p)


def walk(la, lb, fa, fb, cash_a, cash_b):
    """Buy pairs level by level while each extra pair costs < 1 - MIN_EDGE all-in and both venues have
    cash. Returns shares, the fills on each leg [(price, qty)], and the worst price used on each leg."""
    la, lb = [list(x) for x in la], [list(x) for x in lb]
    i = j = 0
    shares, fills_a, fills_b, spent_a, spent_b = 0, [], [], 0.0, 0.0
    while i < len(la) and j < len(lb):
        pa, pb = la[i][0], lb[j][0]
        ua, ub = unit_cost(pa, fa), unit_cost(pb, fb)
        if ua + ub > 1 - MIN_EDGE:
            break
        n = math.floor(min(la[i][1], lb[j][1], (cash_a - spent_a) / ua, (cash_b - spent_b) / ub))
        if n <= 0:
            break
        shares += n
        fills_a.append((pa, n)); fills_b.append((pb, n))
        spent_a += n * ua; spent_b += n * ub
        la[i][1] -= n; lb[j][1] -= n
        if la[i][1] < 1: i += 1
        if lb[j][1] < 1: j += 1
    return shares, fills_a, fills_b


def leg_cost(fills, f):
    """Price paid plus the taker fee, rounded up to the cent per order (both venues round fees up)."""
    px = sum(p * q for p, q in fills)
    return px, ceil_cent(sum(f * p * (1 - p) * q for p, q in fills))


def take(ladder, limit, qty, better=lambda p, lim: p <= lim + 1e-9):
    """What an IOC order for qty at limit fills against this ladder: [(price, qty)]."""
    out, left = [], qty
    for p, q in ladder:
        if left <= 0 or not better(p, limit):
            break
        n = min(q, left)
        out.append((p, n)); left -= n
    return out


def payload(inst, qty, limit, cid):
    """The order exactly as the live bot would send it (dry run: logged, never sent)."""
    venue, bid, how = inst
    if venue == "kalshi":   # POST /trade-api/v2/portfolio/orders
        return {"ticker": bid, "side": how, "action": "buy", "count": int(qty), "type": "limit",
                f"{how}_price_dollars": f"{limit:.4f}", "time_in_force": "immediate_or_cancel",
                "client_order_id": cid}
    # Polymarket US (api.polymarket.us, Ed25519-signed). Field names per its order API; the live bot will
    # be checked against the official docs before any real order.
    return {"marketSlug": bid, "intent": "ORDER_INTENT_BUY_LONG" if how == "0" else "ORDER_INTENT_BUY_SHORT",
            "quantity": int(qty), "priceC": int(round(limit * 100)),
            "timeInForce": "TIME_IN_FORCE_IMMEDIATE_OR_CANCEL", "clientOrderId": cid}


# ------------------------------------------------------------------ ledger
def load_ledger():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    return {"started": A.now().isoformat(timespec="seconds"), "cash": dict(START_CASH), "open": [],
            "settled_pnl": 0.0, "unwind_pnl": 0.0, "fires": 0, "settled": 0}


def save_ledger(L):
    LEDGER.write_text(json.dumps(L, indent=1))


def settle(L):
    """Pay out finished matches from Kalshi's result for the Kalshi leg's ticker."""
    still = []
    for pos in L["open"]:
        d = A.get(f"{A.KALSHI}/markets/{pos['kalshi_ticker']}", tries=2) or {}
        m = d.get("market") or {}
        v = None
        if m.get("result") in ("yes", "no"):
            v = 1.0 if m["result"] == "yes" else 0.0
        elif m.get("result") == "scalar" and m.get("settlement_value_dollars"):
            v = float(m["settlement_value_dollars"])
        if v is None:
            still.append(pos); continue
        k_pay = v if pos["kalshi_side"] == "yes" else 1 - v   # per share, Kalshi leg
        pays = {"kalshi": k_pay * pos["shares"]["kalshi"], "polyus": (1 - k_pay) * pos["shares"]["polyus"]}
        for venue, amt in pays.items():
            L["cash"][venue] = round(L["cash"][venue] + amt, 2)
        pnl = round(sum(pays.values()) - pos["cost"], 2)
        L["settled_pnl"] = round(L["settled_pnl"] + pnl, 2)
        L["settled"] += 1
        A.log(OUT / f"{A.now():%Y-%m-%d}_{RUN}_settlements.csv",
              [{"ts": A.now().isoformat(timespec="seconds"), "id": pos["id"], "key": pos["key"],
                "kalshi_payout": round(pays["kalshi"], 2), "polyus_payout": round(pays["polyus"], 2),
                "cost": pos["cost"], "pnl": pnl, "expected": pos["expected"]}])
    L["open"] = still


def summary(L):
    locked = sum(p["cost"] for p in L["open"])
    files = sorted(OUT.glob("*_fires.csv"))
    f = pd.concat([pd.read_csv(x) for x in files], ignore_index=True) if files else pd.DataFrame()
    lines = [f"# Dry-run bot ({pd.Timestamp.now(tz='America/Denver'):%a %b %-d %-I:%M%p} MT)", "",
             "Paper only: no keys, no real orders. Started " + L["started"][:10] +
             f" with ${sum(START_CASH.values()):.0f} (${START_CASH['kalshi']:.0f} per venue).", "",
             f"- Cash: Kalshi **${L['cash']['kalshi']:.2f}**, Polymarket US **${L['cash']['polyus']:.2f}**; "
             f"locked in {len(L['open'])} open matches: ${locked:.2f}",
             f"- Bankroll now (cash + open at cost): **${L['cash']['kalshi'] + L['cash']['polyus'] + locked:.2f}**",
             f"- Fires: {L['fires']} · settled: {L['settled']} · settled P&L **${L['settled_pnl']:+.2f}** "
             f"(includes unwinds: ${L['unwind_pnl']:+.2f})"]
    if len(f):
        both = (f.filled_a >= f.shares) & (f.filled_b >= f.shares)
        lines += [f"- Both legs fully filled: {both.mean():.0%} of fires · one leg short: {(f.filled_a != f.filled_b).sum()}"
                  f" · expected ${f.expected.sum():.2f} vs simulated ${pd.to_numeric(f.sim_profit, errors='coerce').sum():.2f}",
                  f"- Median book-read time {1000 * f.read_secs.median():.0f} ms, fill check {1000 * f.fill_secs.median():.0f} ms",
                  "", "## Last 15 fires", "",
                  f[["ts", "key", "live", "shares", "total", "expected", "filled_a", "filled_b", "unwind_pnl",
                     "sim_profit"]].tail(15).to_markdown(index=False)]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n")


# ------------------------------------------------------------------ universe
def universe():
    """Matches to watch: every live one on both venues, plus pre-match ones within 2c of an arb.
    Returns {key: {"live": bool, "insts": {side: [inst, ...]}, "kalshi_tickers": {side: ticker}}}."""
    _, df, c = A.scan()
    if not len(c):
        return {}
    best = c.groupby("key").agg(total=("total", "min"), live=("live", "max"))
    keep = best[(best.live) | (best.total < 1.02)].sort_values(["live", "total"], ascending=[False, True])
    out = {}
    for key in keep.index[:MAX_MATCHES]:
        g = df[df.key == key]
        sides = sorted(g.side.unique())
        if len(sides) != 2:
            continue
        other = {sides[0]: sides[1], sides[1]: sides[0]}
        insts, kt = {s: [] for s in sides}, {}
        for r in g.itertuples():
            if r.source == "kalshi":
                kt[r.side] = r.ref
                insts[r.side].append(("kalshi", r.ref, "yes"))
                insts[other[r.side]].append(("kalshi", r.ref, "no"))
            else:
                slug, idx = r.ref.rsplit("#", 1)
                insts[r.side].append(("polyus", slug, idx))
        names = {r.side: r.player for r in g[g.source == "kalshi"].itertuples()}
        out[key] = {"live": bool(keep.loc[key, "live"]), "insts": {s: list(dict.fromkeys(v)) for s, v in insts.items()},
                    "names": names}
    return out


# ------------------------------------------------------------------ one cycle
def cycle(U, L, consumed, pool):
    ids = sorted({(i[0], i[1]) for m in U.values() for s in m["insts"].values() for i in s})
    books, read_secs = read_books(ids, pool)
    fires, best_total = [], None
    for key, m in U.items():
        (s1, l1), (s2, l2) = m["insts"].items()
        cands = []
        for ia in l1:
            for ib in l2:
                if ia[0] == ib[0]:
                    continue
                ba, bb = books.get(ia[:2]), books.get(ib[:2])
                if not ba or not bb:
                    continue
                la, lb = consumed.adjust(ia, ba[ia[2]]["ask"]), consumed.adjust(ib, bb[ib[2]]["ask"])
                if la and lb:
                    t = unit_cost(la[0][0], FEE[ia[0]]) + unit_cost(lb[0][0], FEE[ib[0]])
                    best_total = t if best_total is None else min(best_total, t)
                sh, fa, fb = walk(la, lb, FEE[ia[0]], FEE[ib[0]], L["cash"][ia[0]], L["cash"][ib[0]])
                if not sh:
                    continue
                (pxa, fea), (pxb, feb) = leg_cost(fa, FEE[ia[0]]), leg_cost(fb, FEE[ib[0]])
                exp = sh - pxa - fea - pxb - feb
                cands.append((exp, ia, ib, sh, fa, fb, s1, s2))
        if not cands:
            continue
        exp, ia, ib, sh, fa, fb, sa, sb = max(cands, key=lambda c: c[0])
        if exp < MIN_PROFIT:
            continue
        fires.append(fire(key, m, L, consumed, pool, exp, ia, ib, sh, fa, fb, sa, sb, read_secs))
    return fires, best_total, read_secs


def fire(key, m, L, consumed, pool, exp, ia, ib, sh, fa, fb, sa, sb, read_secs):
    ts = A.now().isoformat(timespec="seconds")
    lim_a, lim_b = ceil_cent(max(p for p, _ in fa)), ceil_cent(max(p for p, _ in fb))
    cid = uuid.uuid4().hex[:12]
    pay_a, pay_b = payload(ia, sh, lim_a, f"{cid}a"), payload(ib, sh, lim_b, f"{cid}b")
    # both orders "land" now: re-read both books and fill each IOC at its limit
    t = time.time()
    (nb_a, _), (nb_b, _) = pool.map(lambda inst: read_book(inst[0], inst[1]), [ia, ib])
    fill_secs = time.time() - t
    ask_a = consumed.adjust(ia, nb_a[ia[2]]["ask"]) if nb_a else []
    ask_b = consumed.adjust(ib, nb_b[ib[2]]["ask"]) if nb_b else []
    got_a, got_b = take(ask_a, lim_a, sh), take(ask_b, lim_b, sh)
    qa, qb = sum(q for _, q in got_a), sum(q for _, q in got_b)
    consumed.add(ia, got_a); consumed.add(ib, got_b)
    (pxa, fea), (pxb, feb) = leg_cost(got_a, FEE[ia[0]]), leg_cost(got_b, FEE[ib[0]])
    spent = {ia[0]: pxa + fea, ib[0]: pxb + feb}
    chase = unwind_q = 0
    unwind_pnl = 0.0
    naked = chase_order = None
    if qa != qb:
        # one leg came up short. Long leg = the one with extra shares.
        long_i, short_i = (ia, ib) if qa > qb else (ib, ia)
        long_got, short_book = (got_a, nb_b) if qa > qb else (got_b, nb_a)
        long_book = nb_a if qa > qb else nb_b
        extra = abs(qa - qb)
        avg_long = (spent[long_i[0]]) / max(qa, qb)
        # 1) chase: buy the missing shares on the short venue if the pair still costs <= $1
        if short_book:
            ladder = consumed.adjust(short_i, short_book[short_i[2]]["ask"])
            ok = [(p, q) for p, q in ladder if avg_long + unit_cost(p, FEE[short_i[0]]) <= 1.0]
            ch = take(ok, 1.0, extra)
            chase = sum(q for _, q in ch)
            if chase:
                consumed.add(short_i, ch)
                cp, cf = leg_cost(ch, FEE[short_i[0]])
                spent[short_i[0]] += cp + cf
                chase_order = payload(short_i, chase, ceil_cent(max(p for p, _ in ch)), f"{cid}c")
        # 2) unwind: sell what's still unhedged on the long venue at the bid
        left = extra - chase
        if left > 0:
            bids = long_book[long_i[2]]["bid"] if long_book else []
            sold = take(bids, 0.0, left, better=lambda p, lim: p > lim)
            unwind_q = sum(q for _, q in sold)
            proceeds = sum(p * q for p, q in sold) - ceil_cent(sum(FEE[long_i[0]] * p * (1 - p) * q for p, q in sold))
            unwind_pnl = round(proceeds - avg_long * unwind_q, 2)
            spent[long_i[0]] -= proceeds
            if left - unwind_q > 0:
                naked = (long_i, left - unwind_q)   # couldn't sell: rides to settlement unhedged
    hedged = min(qa, qb) + chase
    k_inst = ia if ia[0] == "kalshi" else ib
    k_q = qa if ia[0] == "kalshi" else qb
    p_q = qb if ia[0] == "kalshi" else qa
    # shares held per venue after chase/unwind
    held = {"kalshi": k_q, "polyus": p_q}
    if qa != qb:
        held[short_i[0]] += chase
        held[long_i[0]] -= unwind_q
    cost = round(sum(spent.values()), 2)
    for venue, amt in spent.items():
        L["cash"][venue] = round(L["cash"][venue] - amt, 2)
    L["fires"] += 1
    L["unwind_pnl"] = round(L["unwind_pnl"] + unwind_pnl, 2)
    sim = None if naked else round(hedged - cost, 2)   # cost is already net of any unwind sale
    if held["kalshi"] or held["polyus"]:
        # which Kalshi ticker/side decides the payout of the Kalshi leg
        L["open"].append({"id": cid, "key": key, "opened": ts, "kalshi_ticker": k_inst[1], "kalshi_side": k_inst[2],
                          "shares": held, "cost": cost, "expected": round(exp, 2)})
    rec = {"ts": ts, "key": key, "live": m["live"], "shares": sh,
           "leg_a": f"{ia[0]}:{ia[1]}:{ia[2]}", "limit_a": lim_a, "leg_b": f"{ib[0]}:{ib[1]}:{ib[2]}", "limit_b": lim_b,
           "total": round((sum(p * q for p, q in fa) + sum(p * q for p, q in fb)) / sh +
                          (leg_cost(fa, FEE[ia[0]])[1] + leg_cost(fb, FEE[ib[0]])[1]) / sh, 4),
           "expected": round(exp, 2), "filled_a": qa, "filled_b": qb, "chase": chase, "unwound": unwind_q,
           "unwind_pnl": unwind_pnl, "naked": naked[1] if naked else 0, "cost": cost,
           "sim_profit": sim if sim is not None else "",  # locked profit if fully hedged; blank if a naked leg rides
           "read_secs": round(read_secs, 3), "fill_secs": round(fill_secs, 3),
           "order_a": json.dumps(pay_a), "order_b": json.dumps(pay_b),
           "chase_order": json.dumps(chase_order) if chase_order else ""}
    print(f"FIRE {key}: {sh} pairs, expect ${exp:.2f}; filled {qa}/{qb}, chase {chase}, unwound {unwind_q} "
          f"({unwind_pnl:+.2f}), naked {rec['naked']}", flush=True)
    return rec


# ------------------------------------------------------------------ main loop
def commit(msg):
    cmd = ("git add data/bot && (git diff --cached --quiet || git commit -qm \"%s\"); "
           "for i in 1 2 3 4 5; do "
           "  if git pull --rebase -q origin main && git push -q origin HEAD:main; then echo pushed; break; fi; "
           "  git rebase --abort 2>/dev/null; echo \"push attempt $i failed\"; sleep $((i*20)); "
           "done") % msg
    subprocess.run(["bash", "-c", cmd], cwd=ROOT, check=False)


def dispatch_next():
    for i in range(8):
        if subprocess.run(["gh", "workflow", "run", "bot.yml", "--ref", "main"], cwd=ROOT).returncode == 0:
            print("next bot run requested"); return True
        time.sleep(30 * (i + 1))
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=340)
    ap.add_argument("--interval", type=float, default=2.0)
    ap.add_argument("--no-git", action="store_true")
    a = ap.parse_args()
    if not a.no_git:
        subprocess.run(["bash", "-c", "git fetch -q origin main && git checkout -q -B main origin/main"],
                       cwd=ROOT, check=False)
    OUT.mkdir(parents=True, exist_ok=True)
    L, consumed = load_ledger(), Consumed()
    pool = ThreadPoolExecutor(16)
    start = last_commit = last_settle = time.time()
    U, last_u, handed_off, stats = {}, 0, False, []
    while True:
        t0 = time.time()
        if t0 - last_u > REFRESH:
            try:
                U = universe()
            except Exception as e:  # a bad market list shouldn't kill the loop
                print("universe refresh failed:", e)
            last_u = t0
        try:
            fires, best, rs = cycle(U, L, consumed, pool)
        except Exception as e:
            print("cycle failed:", repr(e)); fires, best, rs = [], None, 0
        day = A.now().strftime("%Y-%m-%d")
        if fires:
            A.log(OUT / f"{day}_{RUN}_fires.csv", fires)
            save_ledger(L)
        stats.append((time.time() - t0, best, rs))
        if len(stats) >= max(1, int(60 / a.interval)):   # one summary row per minute
            A.log(OUT / f"{day}_{RUN}_cycles.csv", [{
                "ts": A.now().isoformat(timespec="seconds"), "matches": len(U),
                "live": sum(m["live"] for m in U.values()), "cycles": len(stats),
                "avg_cycle_ms": round(1000 * sum(s[0] for s in stats) / len(stats)),
                "max_read_ms": round(1000 * max(s[2] for s in stats)),
                "best_total": round(min((s[1] for s in stats if s[1] is not None), default=float("nan")), 4)}])
            stats = []
        if time.time() - last_settle > 300:
            settle(L); save_ledger(L); last_settle = time.time()
        elapsed = (time.time() - start) / 60
        if time.time() - last_commit > 15 * 60:
            save_ledger(L); summary(L)
            if not a.no_git:
                commit(f"bot {A.now().isoformat(timespec='minutes')[:16]}Z")
            last_commit = time.time()
        if not a.no_git and not handed_off and elapsed > a.minutes - 60:
            handed_off = dispatch_next()
        if elapsed > a.minutes:
            break
        time.sleep(max(0, a.interval - (time.time() - t0)))
    settle(L); save_ledger(L); summary(L)
    if not a.no_git:
        if not handed_off:
            dispatch_next()
        commit(f"bot {A.now().isoformat(timespec='minutes')[:16]}Z")


if __name__ == "__main__":
    main()
