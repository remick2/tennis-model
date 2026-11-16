# Arb test status (Mon Nov 16 3:09PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (6/10 occasions, 2/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 6 | 10 |
| ...on different UTC days | 2 | 5 |
| ...found by the scanner / by the paper bot | 0 / 6 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 30 / 28 / 4 | - |
| Paper bot: simulated profit on traded fires | $+76.90 | > $0 |
| Paper bot: fires still fillable 1s later | 20% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 866 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 112 failed list refreshes in 86,130 cycles; list vs book disagreed on 202 of 849 checks.

Bot coverage: 2,871 minutes watched. Cycles (2s each) where some pair cost under $1: **7,219**. Best a single fire would have netted: **$17.14**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **5131** · total **$-19296.30** · per fill $-3.76 ± 0.08. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |      94 |    249.58 |   2.66 |
| kalshi  | True   |    4250 | -15087.3  |  -3.55 |
| polyus  | False  |      14 |    -37.17 |  -2.66 |
| polyus  | True   |     773 |  -4421.37 |  -5.72 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |           9 |            8 |          2372 |       -2.85 | -10649.5  |

