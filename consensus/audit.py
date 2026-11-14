"""One-off, read-only audit collector for the consensus tracker (manual workflow: consensus-audit).

Pulls every trade since the evening of Nov 3 2026 for the traders who were top-50 on the monthly sports
leaderboard THAT day (so they were picked before the test window), plus traders added to the roster
later, and aggregates them per trader / market / side, split into pre-game and all trades. Prints the
result as gzip+base64 lines prefixed AUDITDATA: so the analysis can be done offline. Changes nothing.
"""
import base64
import gzip
import json
import re
import sys
import time
from datetime import datetime, timezone

import requests

DATA = "https://data-api.polymarket.com"
GAMMA = "https://gamma-api.polymarket.com"
UA = {"User-Agent": "consensus-paper-tracker/1.0"}
T0 = int(datetime(2026, 11, 4, 0, 30, tzinfo=timezone.utc).timestamp())   # leaderboard was pulled ~00:20Z
MAX_PAGES = 60
DATED = re.compile(r"\d{4}-\d{2}-\d{2}$")

# rank on the Nov 3 monthly sports leaderboard, name, wallet, monthly PnL then, monthly volume then
NOV3 = """1|BreakTheBank|0xf0318c32136c2db7fec88b84869aee6a1106c80c|5922965|89455633
2|joseph00677|0xcdcccd0f2d86e450d973da415ad2430e5cc7935a|5685941|46990663
3|UpTheBlues|0x2a69660046d7acc4ab204d7cc5ba78b0776cd2f7|1960772|161053676
4|HomeRunHazard|0x5268527977f700f9bf9b6d5cd843859e4e70135d|1644610|101451855
5|monkeymashingkeyboard|0x684baa57c338c2549aec0aa3f034f695d72a8409|1529198|17670392
6|googleplay|0xe9b710551dd82a44e79203c2394a2b10163ace7b|1208725|46588760
7|jakepaulthegoat2008|0x6ac5bb06a9eb05641fd5e82640268b92f3ab4b6e|1156145|15287423
8|takeormake|0xa38a455bbdd4b68486548b7e19da99903f4f821d|1019621|32398101
9|Multicoloured-Serf|0x958bdb8aa30b8e5bd1fe4ee071f309c84e97f826|843812|25443250
10|Flaznorp|0x821dab0565ebf5b327f51db06223fdcfe01acf16|821497|240947771
11|Diabolical-Prize|0x7c37b52eb226bcb9411375ec48b0169663fb6aeb|737386|1593689
12|keeptheblueflagflyinghigh|0x0d6a1ada6d7ff785ab4b7263d9ce8e2baa85aa98|731349|27203522
13|0xb4F978BE|0xb4f978be63cdf75554b0b46a4262a6db597cc9a7|729656|13094275
14|Jsram|0x83720820a8aa6c3f20ad71850e7a1a17d16c5223|721893|3423914
15|RN1|0x2005d16a84ceefa912d4e380cd32e7ff827875ea|659707|125998471
16|Woaifacai|0x9b89ef1f344d3e17b37ccdff3bccf62d04f04244|649058|17927372
17|juice-fruit|0x5fdd66ffd0325d4e8d1d86fbec50caa31770a747|595263|5628451
18|ArielFilipino|0xe18ecc345e00ee7c4f2d1f676f3dd2acb112f826|586840|4357083
19|0xd4aa6f8e|0x709e8dcb133555794decc598e07f2c923b8366f5|438885|3015607
20|ndb1|0xfea31bc088000ff909be1dfd8d0e3f2c7ef2d227|414028|6833667
21|0xb0e74DF9|0xb0e74df9430a089aa102e2207af5fde1967439d2|413571|6881
22|chongchong37|0x2879ded7fe05df00eddbb2fba412a0d30964411a|386386|4331084
23|justwins|0xa2cced8bfae7d645f7f437fb76becf2fcbb70cbc|383254|4537400
24|primm|0xd38b71f3e8ed1af71983e5c309eac3dfa9b35029|375009|7043854
25|Eugycom|0x64ceab3becc143e1b97a8e16dc270c2297566015|358369|2714560
26|Elaran1993|0xb7271c112cbd83eb4c1ef1b554ff963604ae2a9d|349993|2461395
27|yabanci|0x285faa3e3d1465cf3ff1bff1e1d14891f5b8495f|345851|6385451
28|Herdonia|0xd106952ebf30a3125affd8a23b6c1f30c35fc79c|342203|10411961
29|drainedandpoor|0x5e6e2c3f06686f2607b86c90e35f536e81a1be00|340898|2658502
30|pikachu2508|0x38891af2ad2f103ab8dc896c0243d2646deffe34|339048|704990
31|robustmst|0xebfdb8164f0e0748818d6c7a9ac85a323267fd63|329792|13199244
32|GoalLineGhost|0x0346afae2603313d2bbee96b628536c8cbe352a5|311211|84538561
33|darkumbreon88|0x0235dc24b38772bf3339a9e5ec5db3d3a05fcee5|291417|3531411
34|theowalcott|0x7ad71d79a3bb90d0a87a06500fa0fe11663842aa|281220|8946071
35|6512395314597884|0x796fc6fda8f8e03c03e2a2d012155989960300f6|281148|38128326
36|1l2ihj34li12u34|0xb52e8b3afd9f0f0d502a5a76494b42816d67285c|269823|13600093
37|01258787xy48487484545122|0x5bfe9469c7c4035325024c846bc530c9d29e3258|264928|11653860
38|3edmond.dantes|0x983eedfbd75803602e4a6e6ea9aab6dc6b9c6748|264642|4934585
39|ic4cream|0x27f738fe203827445690339104aae35b20bc44b0|262869|3129487
40|lfg100k|0xd3911bd5e070c9ad9a9519c966347802d8f3b109|260751|1694882
41|ch27er|0x61a3f1ef9c9618f532eb49f0cb260486c168e508|257265|3585103
42|BillyGating|0x2dfa4e79eca44b7c774f40a45535adbc368a6f60|253029|501366
43|scootergene|0xf3a6ac44c5c90ff2b4afa4459f71acc2e57971bd|251141|1669936
44|UnRektCapital|0xdb7513a3c54d579d64ee64c948c85d2f27620252|250000|0
45|0x20D64368|0x20d6436849f930584892730c7f96ebb2ac763856|245683|1834811
46|fatfatcat|0x6d98d93b9fa0684f21fa1a2ab475c8ca8b97efe9|242920|1699107
47|RichieRicher|0x361b16e3ddfe1d415d41008daac2631d94ab74fe|240798|3592858
48|0x9f15613e|0x9f15613ebf1f36d4bc679e1211d1fc567cf9bdb3|232268|6706346
49|ethanaz|0xf28e42d20e4826f2b10a24bc952001697947cab2|230579|15822542
50|olegio|0x12ec6d71325afac2b4d25b3de94185e2c48d41ae|214998|1464711"""
# added to the roster later (picked from Nov 7 / Nov 10 screens): rank 0 = not in the Nov 3 top 50
LATER = """0|purplegatto|0x032eb1bc893940263ad0b01889f262fc232f2a9e|0|0
0|999585|0x88a6c8e00c4752a8c70d24025fa781fa046a7e77|0|0
0|JoeyAroyyOO|0xc3744a19f42266ce6fa2736f52eae6e178b20f3e|0|0
0|Kyn008|0xd29312e2446a746bbd94408e1c475f1ec6d7d683|0|0
0|ianf2026|0x81d972dbea298a5064d4ba51031e0386182fe9c9|0|0
0|fantasy7788|0x0259b2054f046fe0ee8f3e075fdb85fc3ba9769e|0|0
0|bands1|0xa080dadd87036ad01dbf5e9c254b0c3dbdba234f|0|0
0|AppleTiiime|0x951634357346bb291df117f9ac410100feea2104|0|0"""

S = requests.Session()


def get(url, params):
    for i in range(6):
        try:
            r = S.get(url, params=params, headers=UA, timeout=40)
            if r.status_code == 429:
                time.sleep(5 * (i + 1))
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if i == 5:
                print(f"GET failed {url} {type(e).__name__}", file=sys.stderr)
                return None
            time.sleep(2 * (i + 1))
    return None


def activity(wallet):
    out, cursor, pages = [], None, 0
    while pages < MAX_PAGES:
        p = {"user": wallet, "limit": 500}
        if cursor:
            p["cursor"] = cursor
        j = get(f"{DATA}/v2/activity", p)
        if j is None:
            return out, "error"
        d = j.get("data") or []
        out += d
        pages += 1
        cursor = (j.get("pagination") or {}).get("next_cursor")
        if not cursor or not d or d[-1]["timestamp"] < T0:
            return out, ""
    return out, "truncated"


def parse_ts(s):
    if not s:
        return None
    s = s.strip().replace(" ", "T")
    s = re.sub(r"\+00$", "+00:00", s).replace("Z", "+00:00")
    try:
        return int(datetime.fromisoformat(s).timestamp())
    except ValueError:
        return None


def markets(cids):
    out = {}
    cids = list(cids)
    for i in range(0, len(cids), 20):
        chunk = cids[i:i + 20]
        for closed in ("true", "false"):
            j = get(f"{GAMMA}/markets", [("limit", 100), ("closed", closed)] + [("condition_ids", c) for c in chunk])
            for m in j or []:
                ev = (m.get("events") or [{}])[0]
                st = parse_ts(m.get("gameStartTime")) or parse_ts(ev.get("startTime"))
                try:
                    prices = [float(x) for x in json.loads(m.get("outcomePrices") or "[]")]
                except ValueError:
                    prices = []
                res = prices if m.get("closed") and prices and max(prices) >= 0.98 and min(prices) <= 0.02 else None
                try:
                    toks = json.loads(m.get("clobTokenIds") or "[]")
                except ValueError:
                    toks = []
                out[m["conditionId"]] = [ev.get("slug") or "", m.get("question") or "", st, res,
                                         (m.get("feeSchedule") or {}).get("rate"), toks]
    return out


def main():
    people = [l.split("|") for l in (NOV3 + "\n" + LATER).splitlines()]
    wallets, raw = [], {}
    for rank, name, w, pnl, vol in people:
        acts, flag = activity(w)
        win = [a for a in acts if a.get("timestamp", 0) >= T0]
        types = {}
        for a in win:
            types[a.get("type")] = types.get(a.get("type"), 0) + 1
        tr = [a for a in win if a.get("type") == "TRADE" and DATED.search(a.get("event_slug") or "")
              and a.get("condition_id")]
        mk = {}
        for a in tr:
            if a.get("side") == "BUY":
                mk.setdefault(a["condition_id"], set()).add(a.get("outcome_index"))
        both = sum(len(v) > 1 for v in mk.values())
        days = max(1.0, (time.time() - T0) / 86400)
        info = {"rank": int(rank), "name": name, "wallet": w, "pnl_nov3": int(pnl), "vol_nov3": int(vol),
                "flag": flag, "n_window": len(win), "n_trades": len(tr), "types": types, "n_markets": len(mk),
                "both_pct": round(100 * both / len(mk)) if mk else 0,
                "oldest": min((a["timestamp"] for a in acts), default=0)}
        info["mm"] = bool(flag or info["both_pct"] > 30 or len(mk) / days > 60)
        wallets.append(info)
        raw[w] = tr
        print(f"{rank:>2} {name[:24]:24} window {len(win):6} trades {len(tr):6} markets {len(mk):5} "
              f"both {info['both_pct']:3}% {flag} {'MM' if info['mm'] else ''}", file=sys.stderr)

    cids = {a["condition_id"] for i in wallets if not i["mm"] for a in raw[i["wallet"]]}
    print(f"looking up {len(cids)} markets", file=sys.stderr)
    mk = markets(cids)
    cid_list = sorted(mk)
    cid_idx = {c: i for i, c in enumerate(cid_list)}

    rows = []
    for wi, info in enumerate(wallets):
        if info["mm"]:
            continue
        agg = {}
        for a in sorted(raw[info["wallet"]], key=lambda x: x["timestamp"]):
            cid = a["condition_id"]
            if cid not in mk:
                continue
            st = mk[cid][2]
            oi = a.get("outcome_index")
            usd, sh, px, ts = float(a.get("usdc_size") or 0), float(a.get("size") or 0), float(a.get("price") or 0), a["timestamp"]
            r = agg.setdefault((cid, oi), [0.0] * 8 + [None, None, None, None, a.get("token_id") or ""])
            # 0 pre_buy_usd 1 pre_buy_sh 2 pre_sell_usd 3 pre_sell_sh 4 all_buy_usd 5 all_buy_sh 6 all_sell_usd
            # 7 all_sell_sh 8 t_first 9 p_first 10 t_cross 11 p_cross 12 token
            pre = st is not None and ts < st
            if a.get("side") == "BUY":
                r[4] += usd
                r[5] += sh
                if pre:
                    r[0] += usd
                    r[1] += sh
                    if r[8] is None:
                        r[8], r[9] = ts, px
                    if r[10] is None and r[0] - r[2] >= 1000:
                        r[10], r[11] = ts, px
            else:
                r[6] += usd
                r[7] += sh
                if pre:
                    r[2] += usd
                    r[3] += sh
        for (cid, oi), r in agg.items():
            rows.append([wi, cid_idx[cid], oi] + [round(x, 2) for x in r[:8]] + r[8:])

    blob = {"T0": T0, "now": int(time.time()), "wallets": wallets, "cids": cid_list,
            "markets": [mk[c] for c in cid_list], "rows": rows}
    b = base64.b64encode(gzip.compress(json.dumps(blob, separators=(",", ":")).encode())).decode()
    print(f"rows {len(rows)} markets {len(cid_list)} b64 {len(b)}", file=sys.stderr)
    for i in range(0, len(b), 4000):
        print("AUDITDATA:" + b[i:i + 4000])
    print("AUDITEND")


if __name__ == "__main__":
    main()
