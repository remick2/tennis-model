# Arb test status (Mon Nov 16 9:58AM MT)

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

Coverage: 831 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 110 failed list refreshes in 76,860 cycles; list vs book disagreed on 175 of 814 checks.

Bot coverage: 2,562 minutes watched. Cycles (2s each) where some pair cost under $1: **7,161**. Best a single fire would have netted: **$14.92**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **4303** · total **$-15155.08** · per fill $-3.52 ± 0.09. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |      94 |    249.58 |   2.66 |
| kalshi  | True   |    3603 | -11924.6  |  -3.31 |
| polyus  | False  |      14 |    -37.17 |  -2.66 |
| polyus  | True   |     592 |  -3442.92 |  -5.82 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |           3 |            3 |          1544 |       15.53 |  -6508.33 |

