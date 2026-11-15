# Arb test status (Sat Nov 14 9:14PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (0/10 occasions, 0/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 0 | 10 |
| ...on different UTC days | 0 | 5 |
| ...found by the scanner / by the paper bot | 0 / 0 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 3 / 3 / 0 | - |
| Paper bot: simulated profit on traded fires | $+9.66 | > $0 |
| Paper bot: fires still fillable 1s later | 0% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 0s) | < 5% |

Coverage: 44 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 2 failed list refreshes in 11,250 cycles; list vs book disagreed on 13 of 44 checks.

Bot coverage: 375 minutes watched. Cycles (2s each) where some pair cost under $1: **345**. Best a single fire would have netted: **$5.94**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **283** · total **$-455.39** · per fill $-1.61 ± 0.30. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |   total |   mean |
|:--------|:-------|--------:|--------:|-------:|
| kalshi  | False  |      13 |  -29.27 |  -2.25 |
| kalshi  | True   |     254 | -330.41 |  -1.3  |
| polyus  | True   |      16 |  -95.71 |  -5.98 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |           3 |            3 |           264 |        9.66 |   -462.67 |

