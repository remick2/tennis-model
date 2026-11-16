# Arb test status (Sun Nov 15 5:11PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (4/10 occasions, 1/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 4 | 10 |
| ...on different UTC days | 1 | 5 |
| ...found by the scanner / by the paper bot | 0 / 4 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 21 / 20 / 1 | - |
| Paper bot: simulated profit on traded fires | $+79.75 | > $0 |
| Paper bot: fires still fillable 1s later | 19% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 740 candidate checks (list prices showed an arb), 2 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 46,980 cycles; list vs book disagreed on 130 of 738 checks.

Bot coverage: 1,566 minutes watched. Cycles (2s each) where some pair cost under $1: **5,911**. Best a single fire would have netted: **$14.92**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **2768** · total **$-8672.42** · per fill $-3.13 ± 0.11. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      74 |   256.63 |   3.47 |
| kalshi  | True   |    2352 | -6969.7  |  -2.96 |
| polyus  | False  |       7 |   -20.49 |  -2.93 |
| polyus  | True   |     335 | -1938.86 |  -5.79 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |           0 |            0 |             9 |        0    |    -25.67 |

