# Arb test status (Sun Nov 15 5:34AM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (0/10 occasions, 0/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 0 | 10 |
| ...on different UTC days | 0 | 5 |
| ...found by the scanner / by the paper bot | 0 / 0 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 3 / 3 / 0 | - |
| Paper bot: simulated profit on traded fires | $+9.66 | > $0 |
| Paper bot: fires still fillable 1s later | 0% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 0s) | < 5% |

Coverage: 100 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 26,190 cycles; list vs book disagreed on 58 of 100 checks.

**DATA WARNING: Polymarket US list prices disagree with its order book too often; candidates from the list can't be trusted. Investigate before believing any result.**

Bot coverage: 873 minutes watched. Cycles (2s each) where some pair cost under $1: **1,581**. Best a single fire would have netted: **$5.94**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **1361** · total **$-5290.65** · per fill $-3.89 ± 0.15. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      31 |   -62.73 |  -2.02 |
| kalshi  | True   |    1181 | -4361.67 |  -3.69 |
| polyus  | False  |       4 |   -17.25 |  -4.31 |
| polyus  | True   |     145 |  -849    |  -5.86 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |           3 |            3 |          1342 |        9.66 |  -5297.93 |

