# Arb test status (Tue Nov 17 6:55AM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (8/10 occasions, 3/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 8 | 10 |
| ...on different UTC days | 3 | 5 |
| ...found by the scanner / by the paper bot | 0 / 8 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 43 / 40 / 7 | - |
| Paper bot: simulated profit on traded fires | $+127.41 | > $0 |
| Paper bot: fires still fillable 1s later | 19% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 1002 candidate checks (list prices showed an arb), 18 got no Polymarket US book; 0 rate-limit hits; 112 failed list refreshes in 114,390 cycles; list vs book disagreed on 268 of 984 checks.

Bot coverage: 3,813 minutes watched. Cycles (2s each) where some pair cost under $1: **11,251**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **6620** · total **$-25458.87** · per fill $-3.85 ± 0.07. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |     110 |    211.1  |   1.92 |
| kalshi  | True   |    5433 | -19503.4  |  -3.59 |
| polyus  | False  |      19 |    -90.64 |  -4.77 |
| polyus  | True   |    1058 |  -6075.9  |  -5.74 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          10 |            9 |          1239 |       67.19 |  -5020.43 |

