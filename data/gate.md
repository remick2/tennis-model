# Arb test status (Wed Nov 18 9:55PM MT)

Fresh data only, since Nov 14 21:20 UTC. **PASSED on fresh data.** Next step is Remick's: confirm he wants live trading at $25 per venue per arb. Nobody else turns it on.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 21 | 10 |
| ...on different UTC days | 5 | 5 |
| ...found by the scanner / by the paper bot | 0 / 26 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 91 / 88 / 14 | - |
| Paper bot: simulated profit on traded fires | $+262.46 | > $0 |
| Paper bot: fires still fillable 1s later | 30% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 1335 candidate checks (list prices showed an arb), 29 got no Polymarket US book; 0 rate-limit hits; 118 failed list refreshes in 183,960 cycles; list vs book disagreed on 397 of 1306 checks.

Note: at candidate moments the Polymarket US list disagreed with its book 30% of the time. Every fire is re-checked on the real book, so this means missed detections, not false fires.

Bot coverage: 6,132 minutes watched. Cycles (2s each) where some pair cost under $1: **14,065**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **9962** · total **$-37612.91** · per fill $-3.78 ± 0.06. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |     138 |    190.54 |   1.38 |
| kalshi  | True   |    8182 | -28457.3  |  -3.48 |
| polyus  | False  |      21 |   -110.74 |  -5.27 |
| polyus  | True   |    1621 |  -9235.36 |  -5.7  |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          20 |           19 |          2654 |       82.47 | -10745.6  |
| 2026-11-18 |          14 |           14 |          1502 |       43.62 |  -5497.53 |
| 2026-11-19 |          24 |           24 |           425 |       76.15 |   -931.37 |

