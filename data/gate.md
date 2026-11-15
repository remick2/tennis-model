# Arb test status (Sun Nov 15 7:35AM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (0/10 occasions, 0/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 0 | 10 |
| ...on different UTC days | 0 | 5 |
| ...found by the scanner / by the paper bot | 0 / 0 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 4 / 4 / 0 | - |
| Paper bot: simulated profit on traded fires | $+13.79 | > $0 |
| Paper bot: fires still fillable 1s later | 0% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 0s) | < 5% |

Coverage: 531 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 29,790 cycles; list vs book disagreed on 66 of 531 checks.

Bot coverage: 993 minutes watched. Cycles (2s each) where some pair cost under $1: **2,737**. Best a single fire would have netted: **$5.94**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **1520** · total **$-5964.86** · per fill $-3.92 ± 0.14. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      35 |   -81.12 |  -2.32 |
| kalshi  | True   |    1312 | -4841.13 |  -3.69 |
| polyus  | False  |       6 |   -19.84 |  -3.31 |
| polyus  | True   |     167 | -1022.77 |  -6.12 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |           4 |            4 |          1501 |       13.79 |  -5972.14 |

