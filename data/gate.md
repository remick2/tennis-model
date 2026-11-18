# Arb test status (Wed Nov 18 12:13AM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (14/10 occasions, 4/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 14 | 10 |
| ...on different UTC days | 4 | 5 |
| ...found by the scanner / by the paper bot | 0 / 14 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 65 / 62 / 10 | - |
| Paper bot: simulated profit on traded fires | $+193.26 | > $0 |
| Paper bot: fires still fillable 1s later | 22% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 1195 candidate checks (list prices showed an arb), 29 got no Polymarket US book; 0 rate-limit hits; 116 failed list refreshes in 145,350 cycles; list vs book disagreed on 357 of 1166 checks.

**DATA WARNING: Polymarket US list prices disagree with its order book too often; candidates from the list can't be trusted. Investigate before believing any result.**

Bot coverage: 4,845 minutes watched. Cycles (2s each) where some pair cost under $1: **11,638**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **8621** · total **$-32767.42** · per fill $-3.80 ± 0.06. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |     117 |    173.55 |   1.48 |
| kalshi  | True   |    7133 | -25189.6  |  -3.53 |
| polyus  | False  |      20 |   -107.9  |  -5.4  |
| polyus  | True   |    1351 |  -7643.46 |  -5.66 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          20 |           19 |          2654 |       82.47 | -10745.6  |
| 2026-11-18 |          12 |           12 |           586 |       50.57 |  -1583.41 |

