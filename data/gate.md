# Arb test status (Wed Nov 18 10:39AM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (14/10 occasions, 4/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 14 | 10 |
| ...on different UTC days | 4 | 5 |
| ...found by the scanner / by the paper bot | 0 / 14 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 66 / 63 / 11 | - |
| Paper bot: simulated profit on traded fires | $+190.29 | > $0 |
| Paper bot: fires still fillable 1s later | 21% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 1219 candidate checks (list prices showed an arb), 29 got no Polymarket US book; 0 rate-limit hits; 117 failed list refreshes in 164,070 cycles; list vs book disagreed on 374 of 1190 checks.

**DATA WARNING: Polymarket US list prices disagree with its order book too often; candidates from the list can't be trusted. Investigate before believing any result.**

Bot coverage: 5,469 minutes watched. Cycles (2s each) where some pair cost under $1: **13,763**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **9100** · total **$-34693.71** · per fill $-3.81 ± 0.06. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |     137 |    188.88 |   1.38 |
| kalshi  | True   |    7487 | -26620.8  |  -3.56 |
| polyus  | False  |      21 |   -110.74 |  -5.27 |
| polyus  | True   |    1455 |  -8151.1  |  -5.6  |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          20 |           19 |          2654 |       82.47 | -10745.6  |
| 2026-11-18 |          13 |           13 |          1065 |       47.6  |  -3509.7  |

