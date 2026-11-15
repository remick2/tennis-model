# Arb test status (Sun Nov 15 4:25PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (4/10 occasions, 1/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 4 | 10 |
| ...on different UTC days | 1 | 5 |
| ...found by the scanner / by the paper bot | 0 / 4 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 21 / 20 / 1 | - |
| Paper bot: simulated profit on traded fires | $+79.75 | > $0 |
| Paper bot: fires still fillable 1s later | 19% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 738 candidate checks (list prices showed an arb), 1 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 45,630 cycles; list vs book disagreed on 130 of 737 checks.

Bot coverage: 1,521 minutes watched. Cycles (2s each) where some pair cost under $1: **5,194**. Best a single fire would have netted: **$14.92**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **2735** · total **$-8560.72** · per fill $-3.13 ± 0.11. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      73 |   259.93 |   3.56 |
| kalshi  | True   |    2327 | -6904.33 |  -2.97 |
| polyus  | False  |       7 |   -20.49 |  -2.93 |
| polyus  | True   |     328 | -1895.83 |  -5.78 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2716 |       79.75 |  -8568    |

