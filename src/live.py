"""Live execution for bot.py: real limit IOC orders on Kalshi and Polymarket US.

Nothing here runs unless ALL of these hold:
  - Remick's API keys are in the GitHub secrets (KALSHI_KEY_ID, KALSHI_PRIVATE_KEY, POLY_KEY_ID, POLY_SECRET_KEY)
  - data/live/ENABLED exists; its contents are the max dollars per venue per arb (e.g. "25").
    Delete that file on GitHub to stop live trading instantly (the bot re-reads it every minute).
  - today's live losses haven't hit DAILY_LOSS_STOP and order errors haven't hit ERROR_STOP
    (either one turns live trading off for the rest of the run and opens a GitHub issue)

Order of operations for one arb (same as the dry run): Polymarket US IOC first; Kalshi IOC for exactly what
filled; if Kalshi comes up short, one more Kalshi IOC at break-even; whatever is still unhedged gets sold on
Polymarket US with an IOC that accepts at most UNWIND_MAX_LOSS per share; anything left rides to settlement.

Price conventions (from the official docs):
  Kalshi v2 (POST /portfolio/events/orders): side bid = buy YES, ask = sell YES = buy NO at 1 - price.
    Prices are YES prices. count is a fixed-point string.
  Polymarket US (POST /v1/orders): intent BUY_LONG / BUY_SHORT / SELL_LONG / SELL_SHORT; price is
    always the YES (long) price, so buying the short side at q is a limit of 1 - q.
"""
import base64
import json
import math
import os
import subprocess
import time
from pathlib import Path

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, padding

ROOT = Path(__file__).resolve().parents[1]
LIVE_DIR = ROOT / "data" / "live"
K_BASE, K_PREFIX = "https://api.elections.kalshi.com", "/trade-api/v2"
P_BASE = "https://api.polymarket.us"
DAILY_LOSS_STOP = 20.0     # dollars of realized one-leg losses in a UTC day -> live off
ERROR_STOP = 3             # order API errors in a run -> live off
UNWIND_MAX_LOSS = 0.06     # unwind sell accepts up to 6c/share below what we paid


def cents(px, up):
    """YES price rounded to the cent in the direction that never makes our order worse than its limit."""
    c = round(px * 100, 6)
    return (math.ceil(c) if up else math.floor(c)) / 100


def _num(x):
    """Numbers come back as numbers, strings, or {"value": "..."} objects."""
    if isinstance(x, dict):
        x = x.get("value")
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


class Kalshi:
    def __init__(self, key_id, pem):
        self.key_id = key_id
        self.key = serialization.load_pem_private_key(pem.encode(), password=None)
        self.s = requests.Session()

    def _headers(self, method, path):
        ts = str(int(time.time() * 1000))
        msg = (ts + method + path.split("?")[0]).encode()
        if isinstance(self.key, ed25519.Ed25519PrivateKey):
            sig = self.key.sign(msg)
        else:  # RSA-PSS, SHA-256, MGF1 SHA-256, salt = digest length
            sig = self.key.sign(msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                 salt_length=padding.PSS.DIGEST_LENGTH), hashes.SHA256())
        return {"KALSHI-ACCESS-KEY": self.key_id, "KALSHI-ACCESS-TIMESTAMP": ts,
                "KALSHI-ACCESS-SIGNATURE": base64.b64encode(sig).decode(), "Content-Type": "application/json"}

    def req(self, method, path, body=None):
        full = K_PREFIX + path
        r = self.s.request(method, K_BASE + full, headers=self._headers(method, full),
                           data=json.dumps(body) if body is not None else None, timeout=6)
        try:
            return r.status_code, r.json()
        except ValueError:
            return r.status_code, {"text": r.text[:300]}

    def balance(self):
        code, d = self.req("GET", "/portfolio/balance")
        return (d.get("balance", 0) / 100) if code == 200 else None

    def order(self, ticker, how, qty, limit, cid, sell=False):
        """how 'yes': this ticker's YES; 'no': its NO. limit = worst price for OUR side (max to buy, min to sell)."""
        if how == "yes":
            side, price = ("ask" if sell else "bid"), limit
        else:
            side, price = ("bid" if sell else "ask"), 1 - limit
        price = cents(price, up=(side == "ask"))   # bid: never above the limit; ask: never below
        body = {"ticker": ticker, "side": side, "count": f"{qty:.2f}", "price": f"{price:.4f}",
                "time_in_force": "immediate_or_cancel", "self_trade_prevention_type": "taker_at_cross",
                "client_order_id": cid}
        code, d = self.req("POST", "/portfolio/events/orders", body)
        ok = code in (200, 201)
        filled = _num(d.get("fill_count")) if ok else 0.0
        avg = _num(d.get("average_fill_price")) if filled else 0.0
        if how == "no" and filled:
            avg = 1 - avg  # back to the NO price we paid / received
        return {"ok": ok, "code": code, "filled": filled, "avg": avg,
                "fee": round(_num(d.get("average_fee_paid")) * filled, 4), "body": body, "resp": d}


class PolyUS:
    def __init__(self, key_id, secret):
        self.key_id = key_id
        self.key = ed25519.Ed25519PrivateKey.from_private_bytes(base64.b64decode(secret)[:32])
        self.s = requests.Session()

    def _headers(self, method, path):
        ts = str(int(time.time() * 1000))
        sig = self.key.sign(f"{ts}{method}{path}".encode())
        return {"X-PM-Access-Key": self.key_id, "X-PM-Timestamp": ts,
                "X-PM-Signature": base64.b64encode(sig).decode(), "Content-Type": "application/json"}

    def req(self, method, path, body=None):
        r = self.s.request(method, P_BASE + path, headers=self._headers(method, path.split("?")[0]),
                           data=json.dumps(body) if body is not None else None, timeout=6)
        try:
            return r.status_code, r.json()
        except ValueError:
            return r.status_code, {"text": r.text[:300]}

    def balance(self):
        code, d = self.req("GET", "/v1/account/balances")
        if code != 200:
            return None
        b = [x for x in d.get("balances", []) if x.get("currency", "USD") == "USD"]
        return _num(b[0].get("buyingPower")) if b else None

    def body(self, slug, idx, qty, limit, sell=False):
        intent = {("0", False): "ORDER_INTENT_BUY_LONG", ("1", False): "ORDER_INTENT_BUY_SHORT",
                  ("0", True): "ORDER_INTENT_SELL_LONG", ("1", True): "ORDER_INTENT_SELL_SHORT"}[(idx, sell)]
        px = limit if idx == "0" else 1 - limit   # always the YES price
        sells_yes = (idx == "0") == sell           # BUY_SHORT / SELL_LONG sell YES; the others buy YES
        px = cents(px, up=sells_yes)
        return {"marketSlug": slug, "intent": intent, "type": "ORDER_TYPE_LIMIT",
                "price": {"value": f"{px:.2f}", "currency": "USD"}, "quantity": qty,
                "tif": "TIME_IN_FORCE_IMMEDIATE_OR_CANCEL",
                "manualOrderIndicator": "MANUAL_ORDER_INDICATOR_AUTOMATIC",
                "synchronousExecution": True, "maxBlockTime": "2"}

    def order(self, slug, idx, qty, limit, cid, sell=False):
        body = self.body(slug, idx, qty, limit, sell)
        code, d = self.req("POST", "/v1/orders", body)
        ok = code in (200, 201)
        ex = d.get("executions") or []
        o = (ex[-1].get("order") or {}) if ex else {}
        filled = _num(o.get("cumQuantity")) if ok else 0.0
        avg = _num(o.get("avgPx")) if filled else 0.0
        if idx == "1" and filled:
            avg = 1 - avg  # back to the short-side price
        return {"ok": ok, "code": code, "filled": filled, "avg": avg,
                "fee": _num(o.get("commissionNotionalTotalCollected")), "body": body, "resp": d}

    def preview(self, slug, idx, qty, limit):
        return self.req("POST", "/v1/order/preview", {"request": self.body(slug, idx, qty, limit)})


# ------------------------------------------------------------------ live state
class Live:
    """Holds the venue clients, real balances and the kill switches."""

    def __init__(self, k, p):
        self.k, self.p = k, p
        self.bal = {"kalshi": None, "polyus": None}
        self.errors, self.off_reason, self.cap, self.last_check = 0, None, None, 0
        LIVE_DIR.mkdir(parents=True, exist_ok=True)
        self.ledger_path = LIVE_DIR / "ledger.json"
        self.L = (json.loads(self.ledger_path.read_text()) if self.ledger_path.exists() else
                  {"open": [], "realized": 0.0, "loss_by_day": {}, "trades": 0, "first_trade_alerted": False})

    @classmethod
    def from_env(cls):
        need = ["KALSHI_KEY_ID", "KALSHI_PRIVATE_KEY", "POLY_KEY_ID", "POLY_SECRET_KEY"]
        if not all(os.environ.get(n) for n in need):
            return None
        try:
            return cls(Kalshi(os.environ["KALSHI_KEY_ID"], os.environ["KALSHI_PRIVATE_KEY"]),
                       PolyUS(os.environ["POLY_KEY_ID"], os.environ["POLY_SECRET_KEY"]))
        except Exception as e:  # malformed key: stay dry, say why (never print the key)
            print("live keys present but unusable:", type(e).__name__)
            return None

    def refresh(self):
        """Every ~60s: re-read the ENABLED switch and both real balances."""
        if time.time() - self.last_check < 60:
            return
        self.last_check = time.time()
        # the switch is read from GitHub's copy, so deleting the file on github.com stops trading within a minute
        subprocess.run(["git", "fetch", "-q", "origin", "main"], cwd=ROOT, check=False, capture_output=True)
        r = subprocess.run(["git", "show", "origin/main:data/live/ENABLED"], cwd=ROOT, capture_output=True, text=True)
        try:
            self.cap = float(r.stdout.strip()) if r.returncode == 0 else None
        except ValueError:
            self.cap = None
        for venue, c in (("kalshi", self.k), ("polyus", self.p)):
            try:
                self.bal[venue] = c.balance()
            except requests.RequestException:
                self.bal[venue] = None

    def active(self, day):
        if self.off_reason or not self.cap or None in self.bal.values():
            return False
        return self.L["loss_by_day"].get(day, 0.0) < DAILY_LOSS_STOP

    def cash(self, venue):
        return min(self.bal[venue] or 0.0, self.cap or 0.0)

    def turn_off(self, reason):
        self.off_reason = reason
        issue("LIVE BOT STOPPED: " + reason, f"Live trading is off for the rest of this run: **{reason}**.\n\n"
              "The dry run keeps going. Live trading resumes on the next run unless `data/live/ENABLED` is deleted.")

    def save(self):
        self.ledger_path.write_text(json.dumps(self.L, indent=1))


def issue(title, body):
    if os.environ.get("GH_TOKEN"):
        subprocess.run(["gh", "issue", "create", "--title", title, "--body", body], cwd=ROOT, check=False)
    else:
        print(title, body)


def breakeven_limit(paid_per_share, fee_rate):
    """Highest price x for the missing leg with paid + x + fee(x) <= 1, rounded down to the cent."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if paid_per_share + mid + fee_rate * mid * (1 - mid) <= 1:
            lo = mid
        else:
            hi = mid
    return math.floor(lo * 100) / 100


def auth_check(live, universe):
    """First run with keys: confirm both logins work and that Polymarket US prices short orders in YES terms,
    WITHOUT trading. Writes data/live/auth_check.json for review before ENABLED is ever created."""
    out = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "kalshi_balance": live.k.balance(), "polyus_balance": live.p.balance(), "previews": []}
    slug = next((i[1] for m in universe.values() for s in m["insts"].values() for i in s if i[0] == "polyus"), None)
    if slug:
        for idx, lim in (("0", 0.02), ("1", 0.02)):   # 1 share at 2c: far from the market, can't fill
            code, d = live.p.preview(slug, idx, 1, lim)
            out["previews"].append({"slug": slug, "idx": idx, "limit_our_side": lim,
                                    "sent": live.p.body(slug, idx, 1, lim), "code": code, "resp": d})
    (LIVE_DIR / "auth_check.json").write_text(json.dumps(out, indent=1))
    print("auth check:", {k: v for k, v in out.items() if k != "previews"},
          [(p["idx"], p["code"]) for p in out["previews"]], flush=True)
    return out
