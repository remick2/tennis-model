# Arb test status (Sun Nov 15 6:11PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (4/10 occasions, 1/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 4 | 10 |
| ...on different UTC days | 1 | 5 |
| ...found by the scanner / by the paper bot | 0 / 4 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 22 / 21 / 1 | - |
| Paper bot: simulated profit on traded fires | $+86.56 | > $0 |
| Paper bot: fires still fillable 1s later | 18% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 750 candidate checks (list prices showed an arb), 5 got no Polymarket US book; 0 rate-limit hits; 6 failed list refreshes in 48,780 cycles; list vs book disagreed on 133 of 745 checks.

Bot coverage: 1,626 minutes watched. Cycles (2s each) where some pair cost under $1: **5,926**. Best a single fire would have netted: **$14.92**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **2862** · total **$-8912.43** · per fill $-3.11 ± 0.11. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      74 |   256.63 |   3.47 |
| kalshi  | True   |    2434 | -7139.49 |  -2.93 |
| polyus  | False  |       7 |   -20.49 |  -2.93 |
| polyus  | True   |     347 | -2009.08 |  -5.79 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |           1 |            1 |           103 |        6.81 |   -265.68 |

