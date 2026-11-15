# Arb test status (Sun Nov 15 2:15PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (3/10 occasions, 1/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 3 | 10 |
| ...on different UTC days | 1 | 5 |
| ...found by the scanner / by the paper bot | 0 / 3 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 16 / 15 / 1 | - |
| Paper bot: simulated profit on traded fires | $+56.84 | > $0 |
| Paper bot: fires still fillable 1s later | 19% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 718 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 41,760 cycles; list vs book disagreed on 125 of 718 checks.

Bot coverage: 1,392 minutes watched. Cycles (2s each) where some pair cost under $1: **3,388**. Best a single fire would have netted: **$14.92**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **2625** · total **$-8756.96** · per fill $-3.34 ± 0.11. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      47 |   -90.78 |  -1.93 |
| kalshi  | True   |    2252 | -6827.19 |  -3.03 |
| polyus  | False  |       7 |   -20.49 |  -2.93 |
| polyus  | True   |     319 | -1818.5  |  -5.7  |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          16 |           15 |          2606 |       56.84 |  -8764.24 |

