# Arb test status (Mon Nov 16 2:54PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (5/10 occasions, 2/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 5 | 10 |
| ...on different UTC days | 2 | 5 |
| ...found by the scanner / by the paper bot | 0 / 5 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 29 / 27 / 4 | - |
| Paper bot: simulated profit on traded fires | $+73.32 | > $0 |
| Paper bot: fires still fillable 1s later | 17% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 863 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 112 failed list refreshes in 85,680 cycles; list vs book disagreed on 200 of 846 checks.

Bot coverage: 2,856 minutes watched. Cycles (2s each) where some pair cost under $1: **7,214**. Best a single fire would have netted: **$17.14**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **5097** · total **$-19164.48** · per fill $-3.76 ± 0.08. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |      94 |    249.58 |   2.66 |
| kalshi  | True   |    4223 | -14972.2  |  -3.55 |
| polyus  | False  |      14 |    -37.17 |  -2.66 |
| polyus  | True   |     766 |  -4404.68 |  -5.75 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |           8 |            7 |          2338 |       -6.43 | -10517.7  |

