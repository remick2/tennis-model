# Arb test status (Sun Nov 15 1:24AM MT)

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

Coverage: 77 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 2 failed list refreshes in 18,720 cycles; list vs book disagreed on 44 of 77 checks.

**DATA WARNING: Polymarket US list prices disagree with its order book too often; candidates from the list can't be trusted. Investigate before believing any result.**

Bot coverage: 624 minutes watched. Cycles (2s each) where some pair cost under $1: **586**. Best a single fire would have netted: **$5.94**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **869** · total **$-2991.54** · per fill $-3.44 ± 0.18. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      15 |   -32.68 |  -2.18 |
| kalshi  | True   |     754 | -2395.18 |  -3.18 |
| polyus  | False  |       2 |    -2.99 |  -1.5  |
| polyus  | True   |      98 |  -560.69 |  -5.72 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |           3 |            3 |           850 |        9.66 |  -2998.82 |

