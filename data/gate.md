# Arb test status (Sun Nov 15 8:05AM MT)

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
| Polymarket US reads refused as stale | 0.0% (oldest 0s) | < 5% |

Coverage: 545 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 30,690 cycles; list vs book disagreed on 69 of 545 checks.

Bot coverage: 1,023 minutes watched. Cycles (2s each) where some pair cost under $1: **2,773**. Best a single fire would have netted: **$5.94**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **1571** · total **$-6150.13** · per fill $-3.91 ± 0.14. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      36 |   -70.9  |  -1.97 |
| kalshi  | True   |    1359 | -5023.99 |  -3.7  |
| polyus  | False  |       6 |   -19.84 |  -3.31 |
| polyus  | True   |     170 | -1035.4  |  -6.09 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |           4 |            4 |          1552 |       13.79 |  -6157.41 |

