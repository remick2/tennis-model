# Arb test status (Fri Nov 20 6:07PM MT)

Fresh data only, since Nov 14 21:20 UTC. **PASSED on fresh data.** Next step is Remick's: add his 4 API keys as GitHub secrets, then tell Claude to turn it on ($20 test budget, $5 per arb). Nobody else turns it on.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 22 | 10 |
| ...on different UTC days | 5 | 5 |
| ...found by the scanner / by the paper bot | 0 / 29 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 97 / 94 / 14 | - |
| Paper bot: simulated profit on traded fires | $+272.35 | > $0 |
| Paper bot: fires still fillable 1s later | 31% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 1479 candidate checks (list prices showed an arb), 36 got no Polymarket US book; 0 rate-limit hits; 315 failed list refreshes in 262,530 cycles; list vs book disagreed on 449 of 1443 checks.

Note: at candidate moments the Polymarket US list disagreed with its book 31% of the time. Every fire is re-checked on the real book, so this means missed detections, not false fires.

Bot coverage: 8,751 minutes watched. Cycles (2s each) where some pair cost under $1: **17,990**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **12238** · total **$-46530.25** · per fill $-3.80 ± 0.05. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |     143 |    187.39 |   1.31 |
| kalshi  | True   |    9996 | -34999    |  -3.5  |
| polyus  | False  |      27 |    -83.62 |  -3.1  |
| polyus  | True   |    2072 | -11635    |  -5.62 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          20 |           19 |          2654 |       82.47 | -10745.6  |
| 2026-11-18 |          14 |           14 |          1502 |       43.62 |  -5497.53 |
| 2026-11-19 |          29 |           29 |          1450 |       83.61 |  -5647.96 |
| 2026-11-20 |           1 |            1 |          1175 |        2.43 |  -4143.58 |
| 2026-11-21 |           0 |            0 |            76 |        0    |    -57.17 |

