# Arb test status (Sat Nov 14 7:13PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (0/10 occasions, 0/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 0 | 10 |
| ...on different UTC days | 0 | 5 |
| ...found by the scanner / by the paper bot | 0 / 0 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 1 / 1 / 0 | - |
| Paper bot: simulated profit on traded fires | $+2.09 | > $0 |
| Paper bot: fires still fillable 1s later | 0% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 0s) | < 5% |

Coverage: 21 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 1 failed list refreshes in 7,650 cycles; list vs book disagreed on 4 of 21 checks.

Bot coverage: 255 minutes watched. Cycles (2s each) where some pair cost under $1: **230**. Best a single fire would have netted: **$2.09**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **123** · total **$-34.97** · per fill $-0.28 ± 0.43. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |   total |   mean |
|:--------|:-------|--------:|--------:|-------:|
| kalshi  | False  |       7 |    2.85 |   0.41 |
| kalshi  | True   |     109 |    1.47 |   0.01 |
| polyus  | True   |       7 |  -39.29 |  -5.61 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |           1 |            1 |           104 |        2.09 |    -42.25 |

