# Arb test status (Sun Nov 15 2:30PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (3/10 occasions, 1/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 3 | 10 |
| ...on different UTC days | 1 | 5 |
| ...found by the scanner / by the paper bot | 0 / 3 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 17 / 16 / 1 | - |
| Paper bot: simulated profit on traded fires | $+60.08 | > $0 |
| Paper bot: fires still fillable 1s later | 18% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 719 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 42,210 cycles; list vs book disagreed on 125 of 719 checks.

Bot coverage: 1,407 minutes watched. Cycles (2s each) where some pair cost under $1: **3,399**. Best a single fire would have netted: **$14.92**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **2647** · total **$-8806.66** · per fill $-3.33 ± 0.11. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      47 |   -90.78 |  -1.93 |
| kalshi  | True   |    2271 | -6863.95 |  -3.02 |
| polyus  | False  |       7 |   -20.49 |  -2.93 |
| polyus  | True   |     322 | -1831.44 |  -5.69 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          17 |           16 |          2628 |       60.08 |  -8813.94 |

