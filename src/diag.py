"""Feed diagnostics (run by .github/workflows/diag.yml, ~1 min, prints only). Reads order books the way the bot
does (same burst size, cache-busted) and reports status codes, snapshot age and timing per venue, plus what the
bot's own reader returns. Use it whenever book reads look thin or stale."""
import collections
import time
from concurrent.futures import ThreadPoolExecutor

import requests

import arbscan as A
import bot as B

U = B.universe()
keys = list(U)[:6]
ids = sorted({(i[0], i[1]) for k in keys for s in U[k]["insts"].values() for i in s})
print(f"{len(U)} matched matches; testing {len(keys)} of them = {len(ids)} books "
      f"({sum(v == 'kalshi' for v, _ in ids)} Kalshi, {sum(v == 'polyus' for v, _ in ids)} Polymarket US)")
pool = ThreadPoolExecutor(16)


def raw(vi):
    v, i = vi
    url = (f"{A.KALSHI}/markets/{i}/orderbook" if v == "kalshi" else f"{A.POLYUS}/v1/markets/{i}/book?_={A.fresh()}")
    t = time.time()
    try:
        r = B.sess().get(url, timeout=4)
        return v, r.status_code, A._age(r.headers), time.time() - t, r.headers.get("cache-control"), r.headers.get("retry-after")
    except requests.RequestException as e:
        return v, type(e).__name__, None, time.time() - t, None, None


for rnd in range(8):
    res = list(pool.map(raw, ids))
    for v in ("kalshi", "polyus"):
        rs = [r for r in res if r[0] == v]
        print(f"round {rnd} {v:7s} status {dict(collections.Counter(str(r[1]) for r in rs))} "
              f"ages {sorted({r[2] for r in rs}, key=str)} max {1000 * max(r[3] for r in rs):.0f}ms "
              f"cache-control {sorted({str(r[4]) for r in rs})} retry-after {sorted({str(r[5]) for r in rs})}")
    time.sleep(2)

A.POLY_STATS.update(reads=0, stale=0, unknown=0, max_age=0.0)
for rnd in range(5):
    books, secs = B.read_books(ids, pool)
    got = collections.Counter(v for v, _ in books)
    print(f"bot reader round {rnd}: got {got.get('kalshi', 0)}/{sum(v == 'kalshi' for v, _ in ids)} Kalshi, "
          f"{got.get('polyus', 0)}/{sum(v == 'polyus' for v, _ in ids)} Polymarket US in {1000 * secs:.0f}ms; POLY_STATS {A.POLY_STATS}")
    time.sleep(2)
