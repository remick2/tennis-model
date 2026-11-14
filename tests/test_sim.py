"""Offline checks with synthetic order books. Run before pushing any change to bot/live/makersim/arbscan:
    python3 tests/test_sim.py
No network. Exits non-zero on the first failure."""
import base64
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import arbscan as A   # noqa: E402
import bot as B       # noqa: E402
import live as LIVE   # noqa: E402
import makersim as M  # noqa: E402

B.OUT = Path("/tmp/tennis_test"); B.OUT.mkdir(exist_ok=True); B.LEDGER = B.OUT / "ledger.json"
POOL = ThreadPoolExecutor(4)
KA, KB = "X-CHALLENGER-KA", "X-CHALLENGER-KB"


def kb(no_bids, yes_bids):
    return {"yes": {"ask": sorted((round(1 - p, 4), q) for p, q in no_bids), "bid": sorted(yes_bids, reverse=True)},
            "no": {"ask": sorted((round(1 - p, 4), q) for p, q in yes_bids), "bid": sorted(no_bids, reverse=True)}}


def pb(offers, bids):
    return {"0": {"ask": sorted(offers), "bid": sorted(bids, reverse=True)},
            "1": {"ask": sorted((round(1 - p, 4), q) for p, q in bids),
                  "bid": sorted(((round(1 - p, 4), q) for p, q in offers), reverse=True)}}


MATCH = {"live": True, "hot": True, "insts": {"a": [("kalshi", KA, "yes"), ("polyus", "S", "0")],
                                              "b": [("polyus", "S", "1"), ("kalshi", KA, "no")]}}
K_OK, K_GONE = kb([(0.54, 300), (0.53, 500)], [(0.44, 200)]), kb([(0.50, 300)], [(0.44, 200)])
P_OK, P_GONE = pb([(0.52, 400)], [(0.50, 1000)]), pb([(0.52, 400)], [(0.47, 1000)])


def run(seq):
    n = {"kalshi": 0, "polyus": 0}

    def rb(v, b):
        i = min(n[v], len(seq[v]) - 1); n[v] += 1
        return seq[v][i], 0.01
    B.read_book = rb
    L = {"started": "x", "cash": dict(B.START_CASH), "open": [], "settled_pnl": 0, "unwind_pnl": 0, "fires": 0, "settled": 0}
    B.time.sleep = lambda s: None   # skip the +1s/+3s waits
    f, best, _ = B.cycle({"a v b": MATCH}, L, B.Consumed(), POOL)
    return f[0], L


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    if not cond:
        sys.exit(1)


# --- paper bot: Polymarket US first, Kalshi for what filled
r, L = run({"kalshi": [K_OK], "polyus": [P_OK]})
check("clean arb fills both legs and locks the expected profit", r["filled_a"] == r["filled_b"] == r["shares"] and r["sim_profit"] == r["expected"] > 1)
r, L = run({"kalshi": [K_OK], "polyus": [P_OK, P_GONE]})
check("Polymarket US blank => nothing bought, no cash spent", r["filled_a"] == r["filled_b"] == 0 and L["cash"] == B.START_CASH)
check("...while both-at-once would have been stuck with the Kalshi leg", r["both_filled_a"] > 0 and r["both_filled_b"] == 0)
r, L = run({"kalshi": [K_OK, K_OK, K_GONE], "polyus": [P_OK]})
check("Kalshi gone after Polymarket US filled => unwind at a loss, nothing left open", r["unwound"] > 0 and r["unwind_pnl"] < 0 and r["naked"] == 0 and not L["open"])

# --- settlement pays the winning leg's venue
L = {"cash": {"kalshi": 0.0, "polyus": 0.0}, "settled_pnl": 0, "settled": 0,
     "open": [{"id": "x", "key": "a v b", "kalshi_ticker": KA, "kalshi_side": "yes", "shares": {"kalshi": 100, "polyus": 100}, "cost": 99.0, "expected": 1.0}]}
A.get = lambda url, params=None, tries=3: {"market": {"result": "no"}}
B.settle(L)
check("settlement: Kalshi YES lost => Polymarket US leg pays $100, P&L +$1", L["cash"] == {"kalshi": 0.0, "polyus": 100.0} and L["settled_pnl"] == 1.0)

# --- maker test
MM = {"live": False, "hot": True, "insts": {"a": [("kalshi", KA, "yes"), ("kalshi", KB, "no"), ("polyus", "S", "0")],
                                            "b": [("kalshi", KB, "yes"), ("kalshi", KA, "no"), ("polyus", "S", "1")]}}


def books(kbid, kask, pbid, pask):
    return {("kalshi", KA): kb([(round(1 - kask, 2), 500)], [(kbid, 500)]),
            ("kalshi", KB): kb([(kbid, 500)], [(round(1 - kask, 2), 500)]), ("polyus", "S"): pb([(pask, 500)], [(pbid, 500)])}


ms = M.MakerSim(); ms.step("a v b", MM, books(0.50, 0.51, 0.46, 0.54))
q = ms.quotes[("a v b", ("polyus", "S", "0"))]
check("maker quote locks >= MARGIN after the hedge and never crosses the ask", q["edge"] >= M.MARGIN and q["price"] < 0.54)
ms.step("a v b", MM, books(0.50, 0.51, 0.44, 0.46)); rows = ms.drain()
check("market trades through the bid, hedge venue unchanged => filled and hedged at a profit", len(rows) == 1 and rows[0]["action"] == "hedged" and rows[0]["pnl"] > 0)
ms = M.MakerSim(); ms.step("a v b", MM, books(0.50, 0.51, 0.46, 0.54)); ms.step("a v b", MM, books(0.40, 0.41, 0.40, 0.42))
check("both venues move against the quote => filled at a loss (adverse selection is counted)", ms.drain()[0]["pnl"] < 0)
ms = M.MakerSim(); ms.step("a v b", MM, books(0.50, 0.51, 0.46, 0.54)); ms.step("a v b", MM, books(0.50, 0.51, 0.46, 0.54))
check("no trade-through => no fill", not ms.drain())

# --- live order formats (no network: bodies only)
class P(LIVE.PolyUS):
    def __init__(self): pass
p = P()
b = p.body("s", "1", 10, 0.5412)
check("Polymarket US BUY_SHORT is priced as the YES price, rounded so we never pay more than our limit",
      b["intent"] == "ORDER_INTENT_BUY_SHORT" and b["price"]["value"] == "0.46" and b["tif"] == "TIME_IN_FORCE_IMMEDIATE_OR_CANCEL")
check("Polymarket US BUY_LONG rounds the limit down", p.body("s", "0", 10, 0.4687)["price"]["value"] == "0.46")
check("Polymarket US sell-back of a short position never sells below its floor", p.body("s", "1", 10, 0.4412, sell=True)["price"]["value"] == "0.55")
check("break-even limit: paid 0.52 all-in => other leg at most 0.46 with a 7% fee", LIVE.breakeven_limit(0.52, 0.07) == 0.46)

# --- freshness guard
class R:
    status_code = 200
    def __init__(self, age): self.headers = {"last-modified": "Sat, 14 Nov 2026 21:16:31 GMT", "date": f"Sat, 14 Nov 2026 21:16:{31 + age:02d} GMT"}
    def json(self): return {"marketData": {"bids": [], "offers": []}}
class S:
    def __init__(self, age): self.age = age
    def get(self, *a, **k): return R(self.age)
check("fresh Polymarket US book is accepted", A.polyus_book("s", session=S(1))[0] is not None)
check("Polymarket US book older than POLY_MAX_AGE is refused", A.polyus_book("s", session=S(9))[0] is None and A.POLY_STATS["stale"] >= 1)
print("all checks passed")
