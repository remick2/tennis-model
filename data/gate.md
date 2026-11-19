# Arb test status (Thu Nov 19 5:36AM MT)

Fresh data only, since Nov 14 21:20 UTC. **PASSED on fresh data.** Next step is Remick's: confirm he wants live trading at $25 per venue per arb. Nobody else turns it on.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 22 | 10 |
| ...on different UTC days | 5 | 5 |
| ...found by the scanner / by the paper bot | 0 / 29 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 95 / 92 / 14 | - |
| Paper bot: simulated profit on traded fires | $+268.86 | > $0 |
| Paper bot: fires still fillable 1s later | 32% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 1342 candidate checks (list prices showed an arb), 30 got no Polymarket US book; 0 rate-limit hits; 178 failed list refreshes in 197,640 cycles; list vs book disagreed on 398 of 1312 checks.

Note: at candidate moments the Polymarket US list disagreed with its book 30% of the time. Every fire is re-checked on the real book, so this means missed detections, not false fires.

Bot coverage: 6,588 minutes watched. Cycles (2s each) where some pair cost under $1: **17,552**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **10061** · total **$-38048.50** · per fill $-3.78 ± 0.06. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |     140 |    193.22 |   1.38 |
| kalshi  | True   |    8228 | -28688.5  |  -3.49 |
| polyus  | False  |      27 |    -83.62 |  -3.1  |
| polyus  | True   |    1666 |  -9469.62 |  -5.68 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          20 |           19 |          2654 |       82.47 | -10745.6  |
| 2026-11-18 |          14 |           14 |          1502 |       43.62 |  -5497.53 |
| 2026-11-19 |          28 |           28 |           524 |       82.55 |  -1366.96 |

