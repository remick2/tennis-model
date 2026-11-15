# Arb test status (Sun Nov 15 1:15PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (2/10 occasions, 1/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 2 | 10 |
| ...on different UTC days | 1 | 5 |
| ...found by the scanner / by the paper bot | 0 / 2 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 13 / 12 / 0 | - |
| Paper bot: simulated profit on traded fires | $+57.91 | > $0 |
| Paper bot: fires still fillable 1s later | 15% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 675 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 39,960 cycles; list vs book disagreed on 116 of 675 checks.

Bot coverage: 1,332 minutes watched. Cycles (2s each) where some pair cost under $1: **3,124**. Best a single fire would have netted: **$14.92**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **2510** · total **$-8801.15** · per fill $-3.51 ± 0.11. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      41 |   -89    |  -2.17 |
| kalshi  | True   |    2154 | -6907.73 |  -3.21 |
| polyus  | False  |       7 |   -20.49 |  -2.93 |
| polyus  | True   |     308 | -1783.93 |  -5.79 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          13 |           12 |          2491 |       57.91 |  -8808.43 |

