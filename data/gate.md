# Arb test status (Sun Nov 15 5:04AM MT)

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

Coverage: 88 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 3 failed list refreshes in 25,290 cycles; list vs book disagreed on 53 of 88 checks.

**DATA WARNING: Polymarket US list prices disagree with its order book too often; candidates from the list can't be trusted. Investigate before believing any result.**

Bot coverage: 843 minutes watched. Cycles (2s each) where some pair cost under $1: **1,512**. Best a single fire would have netted: **$5.94**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **1309** · total **$-5173.03** · per fill $-3.95 ± 0.15. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |    total |   mean |
|:--------|:-------|--------:|---------:|-------:|
| kalshi  | False  |      24 |   -92.07 |  -3.84 |
| kalshi  | True   |    1136 | -4214.71 |  -3.71 |
| polyus  | False  |       4 |   -17.25 |  -4.31 |
| polyus  | True   |     145 |  -849    |  -5.86 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |           3 |            3 |          1290 |        9.66 |  -5180.31 |

