# Arb test status (Mon Nov 16 7:19PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (7/10 occasions, 3/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 7 | 10 |
| ...on different UTC days | 3 | 5 |
| ...found by the scanner / by the paper bot | 0 / 7 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 38 / 36 / 7 | - |
| Paper bot: simulated profit on traded fires | $+72.98 | > $0 |
| Paper bot: fires still fillable 1s later | 18% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 944 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 112 failed list refreshes in 93,570 cycles; list vs book disagreed on 233 of 927 checks.

Bot coverage: 3,119 minutes watched. Cycles (2s each) where some pair cost under $1: **7,364**. Best a single fire would have netted: **$17.14**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **5603** · total **$-20803.52** · per fill $-3.71 ± 0.08. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |      95 |    248.54 |   2.62 |
| kalshi  | True   |    4639 | -16079.8  |  -3.47 |
| polyus  | False  |      15 |    -40.73 |  -2.72 |
| polyus  | True   |     854 |  -4931.57 |  -5.77 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |           5 |            5 |           222 |       12.76 |   -365.08 |

