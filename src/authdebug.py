"""One-off: print the SHAPE of Kalshi's balance response and Polymarket US's order-preview response (no orders,
ids redacted) so live.py parses them right."""
import json
import bot
import live

def shape(x, depth=0):
    if isinstance(x, dict):
        return {k: ("<id>" if "id" in k.lower() or "account" in k.lower() or "user" in k.lower() else shape(v, depth + 1))
                for k, v in x.items()}
    if isinstance(x, list):
        return [shape(v, depth + 1) for v in x[:2]]
    return x

LV = live.Live.from_env()
code, d = LV.k.req("GET", "/portfolio/balance")
print("KALSHI BALANCE", code, json.dumps(shape(d)))
U = bot.universe()
slug = next(i[1] for m in U.values() for s in m["insts"].values() for i in s if i[0] == "polyus")
b = bot.read_book("polyus", slug)[0]
print("BOOK top idx0 ask/bid", b and b["0"]["ask"][:1], b and b["0"]["bid"][:1])
for idx, lim in (("1", 0.02), ("1", 0.98), ("0", 0.98)):
    code, d = LV.p.preview(slug, idx, 1, lim)
    print("PREVIEW idx", idx, "our-side limit", lim, "sent", LV.p.body(slug, idx, 1, lim)["price"]["value"], code, json.dumps(shape(d))[:1500])
