# Arb test status (Tue Nov 17 1:15AM MT)

Fresh data only, since Nov 14 21:20 UTC. **NOT PASSED YET** (8/10 occasions, 3/5 days). Test ends Nov 22 00:00 UTC. Live trading is off and stays off.

| Check | Now | Needed |
|---|---|---|
| Arbs a ready bot would profit from (occasions: one per match per day) | 8 | 10 |
| ...on different UTC days | 3 | 5 |
| ...found by the scanner / by the paper bot | 0 / 8 | - |
| ...scanner total at the $690 bankroll | $0.00 | - |
| Paper bot: fires / traded / one leg short | 43 / 40 / 7 | - |
| Paper bot: simulated profit on traded fires | $+127.41 | > $0 |
| Paper bot: fires still fillable 1s later | 19% | - |
| Polymarket US reads refused as stale | 0.0% (oldest 1s) | < 5% |

Coverage: 992 candidate checks (list prices showed an arb), 17 got no Polymarket US book; 0 rate-limit hits; 112 failed list refreshes in 104,190 cycles; list vs book disagreed on 259 of 975 checks.

Bot coverage: 3,473 minutes watched. Cycles (2s each) where some pair cost under $1: **7,423**. Best a single fire would have netted: **$49.40**.

## Maker test (rest a bid on one venue, hedge on the other if it fills)

Fills: **6280** · total **$-24131.02** · per fill $-3.84 ± 0.07. No edge shown (needs 30+ fills with the mean above zero by 2 standard errors).

| venue   | live   |   fills |     total |   mean |
|:--------|:-------|--------:|----------:|-------:|
| kalshi  | False  |      99 |    201.83 |   2.04 |
| kalshi  | True   |    5147 | -18367.4  |  -3.57 |
| polyus  | False  |      19 |    -90.64 |  -4.77 |
| polyus  | True   |    1015 |  -5874.78 |  -5.79 |

## By UTC day

| day        |   bot fires |   bot traded |   maker fills |   bot sim $ |   maker $ |
|:-----------|------------:|-------------:|--------------:|------------:|----------:|
| 2026-11-14 |           0 |            0 |            19 |        0    |      7.28 |
| 2026-11-15 |          21 |           20 |          2740 |       79.75 |  -8654.03 |
| 2026-11-16 |          12 |           11 |          2622 |      -19.53 | -11791.7  |
| 2026-11-17 |          10 |            9 |           899 |       67.19 |  -3692.58 |

