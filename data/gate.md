# Arb test status (Sat Nov 14 5:43PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (0/10 occasions, 0/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 0 | 10 |
| ...on different UTC days | 0 | 5 |
| ...found by the scanner / by the paper bot | 0 / 0 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 0 / 0 / 0 | - |
| Paper bot: simulated profit on traded fires | $+0.00 | > $0 |
| Paper bot: fires still fillable 1s later | n/a | - |
| Polymarket US reads refused as stale | 0.0% (oldest 0s) | < 5% |

Coverage: 5 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 0 failed list refreshes in 4,950 cycles; list vs book disagreed on 1 of 5 checks.

Bot coverage: 165 minutes watched. Cycles (2s each) where some pair cost under $1: **190**. Best a single fire would have netted: **$0.75**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **55** · total **$-49.05** · per fill $-0.89 ± 0.69. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |   total |   mean |
|:--------|:-------|--------:|--------:|-------:|
| kalshi  | False  |       7 |    2.85 |   0.41 |
| kalshi  | True   |      42 |  -14.04 |  -0.33 |
| polyus  | True   |       6 |  -37.86 |  -6.31 |

## By UTC day

| day        |   maker fills |   maker $ |
|:-----------|--------------:|----------:|
| 2026-11-14 |            19 |      7.28 |
| 2026-11-15 |            36 |    -56.33 |

