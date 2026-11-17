# Arb test status (Mon Nov 16 5:25PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (6/10 occasions, 2/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 6 | 10 |
| ...on different UTC days | 2 | 5 |
| ...found by the scanner / by the paper bot | 0 / 6 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 33 / 31 / 7 | - |
| Paper bot: simulated profit on traded fires | $+60.22 | > $0 |
| Paper bot: fires still fillable 1s later | 18% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 881 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 112 failed list refreshes in 90,180 cycles; list vs book disagreed on 212 of 864 checks.

Bot coverage: 3,006 minutes watched. Cycles (2s each) where some pair cost under $1: **7,246**. Best a single fire would have netted: **$17.14**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **5404** · total **$-20487.60** · per fill $-3.79 ± 0.08. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |      95 |    248.54 |   2.62 |
| kalshi  | True   |    4456 | -15903.8  |  -3.57 |
| polyus  | False  |      14 |    -37.17 |  -2.66 |
| polyus  | True   |     839 |  -4795.15 |  -5.72 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |           0 |            0 |            23 |        0    |    -49.16 |

