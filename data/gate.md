# Arb test status (Tue Nov 17 6:02PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (9/10 occasions, 4/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 9 | 10 |
| ...on different UTC days | 4 | 5 |
| ...found by the scanner / by the paper bot | 0 / 9 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 55 / 52 / 10 | - |
| Paper bot: simulated profit on traded fires | $+150.85 | > $0 |
| Paper bot: fires still fillable 1s later | 16% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 1123 candidate checks (list prices showed an arb), 29 got no Polymarket US book; 0 rate-limit hits; 116 failed list refreshes in 134,280 cycles; list vs book disagreed on 330 of 1094 checks.

**DATA WARNING: Polymarket US list prices disagree with its order book too often; candidates from the list can't be trusted. Investigate before believing any result.**

Bot coverage: 4,476 minutes watched. Cycles (2s each) where some pair cost under $1: **11,460**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **8116** · total **$-31310.06** · per fill $-3.86 ± 0.06. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |     114 |    177.94 |   1.56 |
| kalshi  | True   |    6696 | -24099.4  |  -3.6  |
| polyus  | False  |      20 |   -107.9  |  -5.4  |
| polyus  | True   |    1286 |  -7280.73 |  -5.66 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          20 |           19 |          2654 |       82.47 | -10745.6  |
| 2026-11-18 |           2 |            2 |            81 |        8.16 |   -126.05 |

