# Arb test status (Sat Nov 14 4:43PM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (0/10 occasions, 0/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 0 | 10 |
| ...on different UTC days | 0 | 5 |
| ...found by the scanner / by the paper bot | 0 / 0 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 0 / 0 / 0 | - |
| Paper bot: simulated profit on traded fires | $+0.00 | > $0 |
| Paper bot: fires still fillable 1s later | n/a | - |
| Polymarket US reads refused as stale | 0.0% (oldest 0s) | < 5% |

Coverage: 2 candidate checks (list prices showed an arb), 0 got no Polymarket US book; 0 rate-limit hits; 0 failed list refreshes in 3,150 cycles; list vs book disagreed on 1 of 2 checks.

Bot coverage: 105 minutes watched. Cycles where some pair cost under $1: **174**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **16** · total **$+2.96** · per fill $+0.18 ± 0.78. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |   total |   mean |
|:--------|:-------|--------:|--------:|-------:|
| kalshi  | False  |       5 |    4.04 |   0.81 |
| kalshi  | True   |      11 |   -1.08 |  -0.1  |

## By UTC day

| day        |   maker fills |   maker $ |
|:-----------|--------------:|----------:|
| 2026-11-14 |            16 |      2.96 |

