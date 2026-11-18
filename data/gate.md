# Arb test status (Wed Nov 18 4:59PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (14/10 occasions, 4/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 14 | 10 |
| ...on different UTC days | 4 | 5 |
| ...found by the scanner / by the paper bot | 0 / 14 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 67 / 64 / 12 | - |
| Paper bot: simulated profit on traded fires | $+186.31 | > $0 |
| Paper bot: fires still fillable 1s later | 21% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 1244 candidate checks (list prices showed an arb), 29 got no Polymarket US book; 0 rate-limit hits; 117 failed list refreshes in 175,140 cycles; list vs book disagreed on 389 of 1215 checks.

Note: at candidate moments the Polymarket US list disagreed with its book 32% of the time. Every fire is re-checked on the real book, so this means missed detections, not false fires.

Bot coverage: 5,838 minutes watched. Cycles (2s each) where some pair cost under $1: **13,804**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **9536** · total **$-36681.11** · per fill $-3.85 ± 0.06. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |     137 |    188.88 |   1.38 |
| kalshi  | True   |    7807 | -27963.5  |  -3.58 |
| polyus  | False  |      21 |   -110.74 |  -5.27 |
| polyus  | True   |    1571 |  -8795.75 |  -5.6  |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          20 |           19 |          2654 |       82.47 | -10745.6  |
| 2026-11-18 |          14 |           14 |          1501 |       43.62 |  -5497.1  |

