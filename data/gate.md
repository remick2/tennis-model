# Arb test status (Sun Nov 15 12:45PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (2/10 occasions, 1/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 2 | 10 |
| ...on different UTC days | 1 | 5 |
| ...found by the scanner / by the paper bot | 0 / 2 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 11 / 10 / 0 | - |
| Paper bot: simulated profit on traded fires | $+54.59 | > $0 |
| Paper bot: fires still fillable 1s later | 18% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 651 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 39,060 cycles; list vs book disagreed on 109 of 651 checks.

Bot coverage: 1,302 minutes watched. Cycles (2s each) where some pair cost under $1: **3,070**. Best a single fire would have netted: **$14.92**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **2414** · total **$-8779.42** · per fill $-3.64 ± 0.11. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      41 |   -89    |  -2.17 |
| kalshi  | True   |    2064 | -6901.66 |  -3.34 |
| polyus  | False  |       7 |   -20.49 |  -2.93 |
| polyus  | True   |     302 | -1768.27 |  -5.86 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          11 |           10 |          2395 |       54.59 |  -8786.7  |

