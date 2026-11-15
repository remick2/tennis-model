# Arb test status (Sun Nov 15 10:30AM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (0/10 occasions, 0/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 0 | 10 |
| ...on different UTC days | 0 | 5 |
| ...found by the scanner / by the paper bot | 0 / 0 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 4 / 4 / 0 | - |
| Paper bot: simulated profit on traded fires | $+13.79 | > $0 |
| Paper bot: fires still fillable 1s later | 0% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 574 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 35,010 cycles; list vs book disagreed on 91 of 574 checks.

Bot coverage: 1,167 minutes watched. Cycles (2s each) where some pair cost under $1: **2,851**. Best a single fire would have netted: **$5.94**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **2042** · total **$-8114.08** · per fill $-3.97 ± 0.12. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      40 |   -76.33 |  -1.91 |
| kalshi  | True   |    1716 | -6392.83 |  -3.73 |
| polyus  | False  |       7 |   -20.49 |  -2.93 |
| polyus  | True   |     279 | -1624.43 |  -5.82 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |           4 |            4 |          2023 |       13.79 |  -8121.36 |

