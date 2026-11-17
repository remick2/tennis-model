# Arb test status (Tue Nov 17 12:51PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (8/10 occasions, 3/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 8 | 10 |
| ...on different UTC days | 3 | 5 |
| ...found by the scanner / by the paper bot | 0 / 8 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 44 / 41 / 7 | - |
| Paper bot: simulated profit on traded fires | $+132.85 | > $0 |
| Paper bot: fires still fillable 1s later | 18% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 1043 candidate checks (list prices showed an arb), 29 got no Polymarket US book; 0 rate-limit hits; 116 failed list refreshes in 125,010 cycles; list vs book disagreed on 295 of 1014 checks.

Bot coverage: 4,167 minutes watched. Cycles (2s each) where some pair cost under $1: **11,314**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **7406** · total **$-28703.87** · per fill $-3.88 ± 0.06. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |     114 |    177.94 |   1.56 |
| kalshi  | True   |    6102 | -22142.9  |  -3.63 |
| polyus  | False  |      20 |   -107.9  |  -5.4  |
| polyus  | True   |    1170 |  -6631.03 |  -5.67 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          11 |           10 |          2025 |       72.63 |  -8265.43 |

