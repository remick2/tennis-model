# Arb test status (Tue Nov 17 7:47PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (14/10 occasions, 4/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 14 | 10 |
| ...on different UTC days | 4 | 5 |
| ...found by the scanner / by the paper bot | 0 / 14 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 62 / 59 / 10 | - |
| Paper bot: simulated profit on traded fires | $+186.79 | > $0 |
| Paper bot: fires still fillable 1s later | 23% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 1151 candidate checks (list prices showed an arb), 29 got no Polymarket US book; 0 rate-limit hits; 116 failed list refreshes in 137,400 cycles; list vs book disagreed on 332 of 1122 checks.

Bot coverage: 4,580 minutes watched. Cycles (2s each) where some pair cost under $1: **11,558**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **8294** · total **$-31387.87** · per fill $-3.78 ± 0.06. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |     114 |    177.94 |   1.56 |
| kalshi  | True   |    6865 | -24148.8  |  -3.52 |
| polyus  | False  |      20 |   -107.9  |  -5.4  |
| polyus  | True   |    1295 |  -7309.13 |  -5.64 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          20 |           19 |          2654 |       82.47 | -10745.6  |
| 2026-11-18 |           9 |            9 |           259 |       44.1  |   -203.86 |

