# Arb test status (Mon Nov 16 10:28AM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (5/10 occasions, 2/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 5 | 10 |
| ...on different UTC days | 2 | 5 |
| ...found by the scanner / by the paper bot | 0 / 5 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 24 / 23 / 1 | - |
| Paper bot: simulated profit on traded fires | $+95.28 | > $0 |
| Paper bot: fires still fillable 1s later | 21% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 834 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 110 failed list refreshes in 77,760 cycles; list vs book disagreed on 178 of 817 checks.

Bot coverage: 2,592 minutes watched. Cycles (2s each) where some pair cost under $1: **7,166**. Best a single fire would have netted: **$14.92**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **4447** · total **$-16057.34** · per fill $-3.61 ± 0.09. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |      94 |    249.58 |   2.66 |
| kalshi  | True   |    3699 | -12541.7  |  -3.39 |
| polyus  | False  |      14 |    -37.17 |  -2.66 |
| polyus  | True   |     640 |  -3728.04 |  -5.83 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |           3 |            3 |          1688 |       15.53 |  -7410.59 |

