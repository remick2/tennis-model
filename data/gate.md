# Arb test status (Sun Nov 15 9:45AM MT)

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

Coverage: 561 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 33,660 cycles; list vs book disagreed on 82 of 561 checks.

Bot coverage: 1,122 minutes watched. Cycles (2s each) where some pair cost under $1: **2,831**. Best a single fire would have netted: **$5.94**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **1882** · total **$-7324.96** · per fill $-3.89 ± 0.12. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      39 |   -75.68 |  -1.94 |
| kalshi  | True   |    1610 | -5943.37 |  -3.69 |
| polyus  | False  |       6 |   -19.84 |  -3.31 |
| polyus  | True   |     227 | -1286.07 |  -5.67 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |           4 |            4 |          1863 |       13.79 |  -7332.24 |

