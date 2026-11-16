# Arb test status (Mon Nov 16 1:53AM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (5/10 occasions, 2/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 5 | 10 |
| ...on different UTC days | 2 | 5 |
| ...found by the scanner / by the paper bot | 0 / 5 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 24 / 23 / 1 | - |
| Paper bot: simulated profit on traded fires | $+95.28 | > $0 |
| Paper bot: fires still fillable 1s later | 21% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 814 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 109 failed list refreshes in 62,400 cycles; list vs book disagreed on 163 of 797 checks.

Bot coverage: 2,080 minutes watched. Cycles (2s each) where some pair cost under $1: **6,056**. Best a single fire would have netted: **$14.92**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **3583** · total **$-12063.61** · per fill $-3.37 ± 0.10. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      85 |   265.76 |   3.13 |
| kalshi  | True   |    3005 | -9451.99 |  -3.15 |
| polyus  | False  |       9 |   -24.66 |  -2.74 |
| polyus  | True   |     484 | -2852.72 |  -5.89 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |           3 |            3 |           824 |       15.53 |  -3416.86 |

