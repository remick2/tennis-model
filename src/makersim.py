"""Paper test of a second strategy: REST a buy order on one venue (maker), hedge on the other only if it fills.

Why test it: buying both sides as a taker costs ~3.5c of fees per $1 pair at 50/50, and on fresh data the
venues almost never disagree by that much. A resting order pays far less:
  Polymarket US maker: $0 (no fee; rebates only start at $10M/month volume)
  Kalshi maker: $0 on Challengers (fee_type "quadratic"), 0.0175*p*(1-p) on ATP/WTA main tour
    ("quadratic_with_maker_fees"; Kalshi's fee schedule lists KXATPMATCH and KXWTAMATCH with maker
    multiplier 1 on the 0.0175 formula, checked Nov 14 2026)
so the hurdle is about half. The catch is adverse selection: a resting bid gets filled exactly when the
price moves against it, and the hedge has moved too. This simulator measures which effect wins.

How a quote is simulated (per match, per side, per maker venue; $QUOTE_USD each):
  - hedge cost h = cheapest fresh ask for the OTHER player on the OTHER venue, plus its taker fee
  - highest bid that still locks MARGIN after fees: q_max + maker_fee + h <= 1 - MARGIN
  - post at min(q_max, best bid + 1c) if that is within DEEP of the best bid and doesn't cross the ask
  - FILL RULE (conservative): the quote counts as filled only when, at a later read, the maker venue's best
    ask is at or below our bid: the market traded through our price, so our bid must have been hit. Fills
    from ordinary sells that don't move the ask are missed (understates fills); queue position can't
    overstate fills because a through-move consumes every bid at that price.
  - on a fill: hedge at the other venue's fresh ask from that same read (up to one poll interval late, so
    pessimistic vs a real bot on a websocket), or sell the filled leg back at the bid, whichever loses less.
The quote is then recomputed from the fresh books. No cash limits: this measures edge per quote, not bankroll.
Logs each fill to data/bot/<day>_<run>_maker.csv. Nothing here places an order.
"""
import math
import time

import arbscan as A

QUOTE_USD = 50.0
MARGIN = 0.005        # lock at least 0.5c per pair after fees at the moment of posting
DEEP = 0.03           # only keep quotes within 3c of the best bid
TAKER = A.FEE
TICK = 0.01


def maker_fee(inst):
    if inst[0] == "polyus":
        return 0.0
    return 0.0 if "CHALLENGER" in inst[1] else 0.0175


def unit(p, f):
    return p + f * p * (1 - p)


def fill_from(ladder, qty):
    out, left = [], qty
    for p, q in ladder:
        if left <= 0:
            break
        n = min(q, left)
        out.append((p, n)); left -= n
    return out, qty - left


class MakerSim:
    def __init__(self):
        self.quotes = {}      # (key, maker_inst) -> dict(price, n, ts, side, at_touch, edge)
        self.posted = 0       # quote-reads with an active quote (exposure measure)
        self.fills = []       # rows waiting to be logged

    def step(self, key, m, books):
        """One fresh read of every book for this match."""
        (s1, l1), (s2, l2) = m["insts"].items()
        other = {s1: l2, s2: l1}
        now = time.time()
        for side, insts in ((s1, l1), (s2, l2)):
            for mk in insts:
                if mk[0] == "kalshi" and mk[2] != "yes":
                    continue   # one maker instrument per venue per side (Kalshi: the player's own YES)
                mb = books.get(mk[:2])
                hedges = [(h, books.get(h[:2])) for h in other[side] if h[0] != mk[0]]
                hedges = [(h, b) for h, b in hedges if b]
                k = (key, mk)
                if not mb or not hedges:
                    self.quotes.pop(k, None)   # can't see a book: a real bot would pull the quote
                    continue
                ask, bid = mb[mk[2]]["ask"], mb[mk[2]]["bid"]
                q = self.quotes.pop(k, None)
                if q and ask and ask[0][0] <= q["price"] + 1e-9:
                    self.fills.append(self._fill(key, m, mk, q, bid, hedges, now))
                # (re)quote from the fresh books
                h_cost = min((unit(b[h[2]]["ask"][0][0], TAKER[h[0]]) for h, b in hedges
                              if b[h[2]]["ask"] and b[h[2]]["ask"][0][1] >= 100), default=None)
                if h_cost is None or not bid or not ask:
                    continue
                mf = maker_fee(mk)
                lo, hi = 0.0, 1.0
                for _ in range(30):
                    mid = (lo + hi) / 2
                    lo, hi = (mid, hi) if unit(mid, mf) + h_cost <= 1 - MARGIN else (lo, mid)
                q_max = math.floor(lo / TICK + 1e-9) * TICK
                bb, ba = bid[0][0], ask[0][0]
                px = round(min(q_max, bb + TICK), 4)
                if px >= ba - 1e-9 or px < bb - DEEP or not (0.03 <= px <= 0.97):
                    continue
                self.quotes[k] = {"price": px, "n": math.floor(QUOTE_USD / px), "ts": now, "side": side,
                                  "at_touch": px >= bb - 1e-9, "edge": round(1 - unit(px, mf) - h_cost, 4)}
                self.posted += 1

    def _fill(self, key, m, mk, q, bid, hedges, now):
        n, px, mf = q["n"], q["price"], maker_fee(mk)
        paid = px * n + mf * px * (1 - px) * n
        best = None
        for h, b in hedges:   # hedge: buy the other player on the other venue at whatever the ask is now
            got, qty = fill_from(b[h[2]]["ask"], n)
            if qty >= n:
                cost = sum(p * x for p, x in got) + sum(TAKER[h[0]] * p * (1 - p) * x for p, x in got)
                if best is None or cost < best[0]:
                    best = (cost, h, got[-1][0])
        hedge_pnl = (n - paid - best[0]) if best else None
        sold, qty = fill_from(bid, n)   # or give up: sell the filled leg back at the bid (taker)
        unwind_pnl = (sum(p * x for p, x in sold) - sum(TAKER[mk[0]] * p * (1 - p) * x for p, x in sold) - paid
                      ) if qty >= n else None
        opts = [(v, a) for v, a in ((hedge_pnl, "hedged"), (unwind_pnl, "unwound")) if v is not None]
        pnl, action = max(opts) if opts else (None, "stuck")
        return {"ts": A.now().isoformat(timespec="seconds"), "key": key, "live": m["live"],
                "maker": f"{mk[0]}:{mk[1]}:{mk[2]}", "price": px, "shares": n, "at_touch": q["at_touch"],
                "edge_when_posted": q["edge"], "rested_secs": round(now - q["ts"], 1), "action": action,
                "hedge": f"{best[1][0]}:{best[1][1]}:{best[1][2]}" if best else "", "hedge_worst_px": best[2] if best else "",
                "hedge_pnl": "" if hedge_pnl is None else round(hedge_pnl, 2),
                "unwind_pnl": "" if unwind_pnl is None else round(unwind_pnl, 2),
                "pnl": "" if pnl is None else round(pnl, 2), "fresh": True}

    def drain(self):
        rows, self.fills = self.fills, []
        return rows
