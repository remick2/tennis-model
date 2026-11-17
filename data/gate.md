# Arb test status (Mon Nov 16 6:10PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (6/10 occasions, 2/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 6 | 10 |
| ...on different UTC days | 2 | 5 |
| ...found by the scanner / by the paper bot | 0 / 6 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 35 / 33 / 7 | - |
| Paper bot: simulated profit on traded fires | $+67.22 | > $0 |
| Paper bot: fires still fillable 1s later | 17% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 897 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 112 failed list refreshes in 91,530 cycles; list vs book disagreed on 218 of 880 checks.

Bot coverage: 3,051 minutes watched. Cycles (2s each) where some pair cost under $1: **7,280**. Best a single fire would have netted: **$17.14**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **5482** · total **$-20746.31** · per fill $-3.78 ± 0.08. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |      95 |    248.54 |   2.62 |
| kalshi  | True   |    4524 | -16071.6  |  -3.55 |
| polyus  | False  |      15 |    -40.73 |  -2.72 |
| polyus  | True   |     848 |  -4882.55 |  -5.76 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |           2 |            2 |           101 |        7    |   -307.87 |

