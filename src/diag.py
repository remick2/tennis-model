"""Feed diagnostics (run by .github/workflows/diag.yml, ~2 min, prints only). Measures what the public feeds
allow from a GitHub runner: status codes, snapshot age, timing and rate limits. Use it whenever book reads look
thin or stale (data/gate.md shows the share of Polymarket US reads that failed)."""
import collections
import json
import time
from concurrent.futures import ThreadPoolExecutor

import requests

import arbscan as A
import bot as B

S = requests.Session()


def lists():
    out = []
    for lg in ("atp", "wta"):
        t = time.time()
        try:
            r = S.get(f"{A.POLYUS}/v2/leagues/{lg}/events", params={"limit": 500, "_": A.fresh()}, timeout=6)
            out.append((r.status_code, round(1000 * (time.time() - t)), r.headers.get("retry-after"), len(r.content)))
        except requests.RequestException as e:
            out.append((type(e).__name__, 0, None, 0))
    return out


def book(slug, bust=True):
    t = time.time()
    try:
        r = S.get(f"{A.POLYUS}/v1/markets/{slug}/book", params={"_": A.fresh()} if bust else None, timeout=6)
        return r.status_code, A._age(r.headers), round(1000 * (time.time() - t)), r.headers.get("retry-after")
    except requests.RequestException as e:
        return type(e).__name__, None, 0, None


d = S.get(f"{A.POLYUS}/v2/leagues/atp/events", params={"limit": 500, "_": A.fresh()}, timeout=20).json()
slugs = [m["slug"] for e in d.get("events", []) if not e.get("closed") and not e.get("ended")
         for m in e.get("markets", []) if m.get("sportsMarketType") == "tennis_match_winner" and not m.get("closed")][:12]
print(f"{len(slugs)} test markets")

print("A) both league lists every 1s x 25 (the cheap way to get every market's best bid/ask)")
c = collections.Counter()
for i in range(25):
    t0 = time.time()
    res = lists()
    for r in res:
        c[str(r[0])] += 1
    if i % 6 == 0 or any(r[0] != 200 for r in res):
        print("  ", i, res)
    time.sleep(max(0, 1 - (time.time() - t0)))
print("   list status totals:", dict(c))

print("B) one uncached book every 2s x 15")
c = collections.Counter()
for i in range(15):
    r = book(slugs[i % len(slugs)])
    c[str(r[0])] += 1
    if r[0] != 200:
        print("  ", i, r)
    time.sleep(2)
print("   book status totals:", dict(c))

time.sleep(12)
print("C) one uncached book every 1s x 20")
c = collections.Counter()
for i in range(20):
    r = book(slugs[i % len(slugs)])
    c[str(r[0])] += 1
    if r[0] != 200 and c[str(r[0])] <= 3:
        print("  ", i, r)
    time.sleep(1)
print("   book status totals:", dict(c))

time.sleep(12)
print("D) bursts of 3 uncached books, 4s apart x 6")
for i in range(6):
    print("  ", i, [book(s)[0] for s in slugs[:3]])
    time.sleep(4)

time.sleep(12)
print("E) CACHED book reads (no cache-buster) every 0.5s x 20: are they limited too?")
c = collections.Counter(); ages = []
for i in range(20):
    r = book(slugs[i % 4], bust=False)
    c[str(r[0])] += 1; ages.append(r[1])
    time.sleep(0.5)
print("   cached status totals:", dict(c), "ages", ages)
