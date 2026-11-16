# Arb test status (Mon Nov 16 2:08PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (5/10 occasions, 2/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 5 | 10 |
| ...on different UTC days | 2 | 5 |
| ...found by the scanner / by the paper bot | 0 / 5 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 28 / 26 / 3 | - |
| Paper bot: simulated profit on traded fires | $+86.04 | > $0 |
| Paper bot: fires still fillable 1s later | 18% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 859 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 111 failed list refreshes in 84,330 cycles; list vs book disagreed on 197 of 842 checks.

Bot coverage: 2,811 minutes watched. Cycles (2s each) where some pair cost under $1: **7,206**. Best a single fire would have netted: **$17.14**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **5000** · total **$-18652.88** · per fill $-3.73 ± 0.08. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |      94 |    249.58 |   2.66 |
| kalshi  | True   |    4142 | -14526.6  |  -3.51 |
| polyus  | False  |      14 |    -37.17 |  -2.66 |
| polyus  | True   |     750 |  -4338.65 |  -5.78 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |           7 |            6 |          2241 |        6.29 | -10006.1  |

