# Arb test status (Mon Nov 16 9:19PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (7/10 occasions, 3/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 7 | 10 |
| ...on different UTC days | 3 | 5 |
| ...found by the scanner / by the paper bot | 0 / 7 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 41 / 38 / 7 | - |
| Paper bot: simulated profit on traded fires | $+123.88 | > $0 |
| Paper bot: fires still fillable 1s later | 17% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 972 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 112 failed list refreshes in 97,170 cycles; list vs book disagreed on 245 of 955 checks.

Bot coverage: 3,239 minutes watched. Cycles (2s each) where some pair cost under $1: **7,396**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **5787** · total **$-21505.90** · per fill $-3.72 ± 0.07. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |      96 |    241.9  |   2.52 |
| kalshi  | True   |    4800 | -16625.2  |  -3.46 |
| polyus  | False  |      16 |    -45.49 |  -2.84 |
| polyus  | True   |     875 |  -5077.09 |  -5.8  |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |           8 |            7 |           406 |       63.66 |  -1067.46 |

