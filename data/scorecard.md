# Phase 2 scorecard  (Sun Nov 8 3:17AM MT)

Snapshots: 131 runs, Nov 3 to Nov 8 10:17Z. Phase 3 gate (GATE row): US-venue price flags beat the close on average (CLV > 0 by ~2 SE) over 100+ graded sides.

| group                                                  |   sides |   avg_price_edge_c |   with_close |   avg_clv_c |   clv_se_c |   beat_close_% |   settled |   won |   roi_% |   roi_se_% |
|:-------------------------------------------------------|--------:|-------------------:|-------------:|------------:|-----------:|---------------:|----------:|------:|--------:|-----------:|
| GATE: price flag on US venues (Kalshi + Polymarket US) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |     nan    |
| price flag, all venues incl. Polymarket intl           |       2 |               2.16 |            2 |        2.56 |       0.62 |         100    |         2 |     1 |   -0.57 |      37.55 |
| model+price flag (alert rule)                          |       2 |               2.16 |            2 |        2.56 |       0.62 |         100    |         2 |     1 |   -0.57 |      37.55 |
| all sides (baseline)                                   |     191 |              -1.9  |          191 |       -1.9  |       0.11 |          10.47 |       175 |    87 |    5.19 |       9.44 |

## Tennis Tonic picks (graded vs Kalshi price; edge only if pick_won_% beats market_said_%)

|   graded_picks |   pick_won_% |   market_said_% |   roi_at_kalshi_% |   roi_se_% |   logged_picks |
|---------------:|-------------:|----------------:|------------------:|-----------:|---------------:|
|            181 |        65.75 |           65.61 |             -6.31 |       5.32 |            369 |

## Kalshi + Polymarket arbitrage check (best combo per match, all-in)

| day        |   runs |   best_total |   under_1 |   under_1_005 |
|:-----------|-------:|-------------:|----------:|--------------:|
| 2026-11-03 |      4 |       1.0014 |         0 |             4 |
| 2026-11-04 |     22 |       0.9769 |         3 |             7 |
| 2026-11-05 |     29 |       0.6918 |        17 |            19 |
| 2026-11-06 |     29 |       0.9679 |         2 |             2 |
| 2026-11-07 |     28 |       0.8883 |        69 |           109 |
| 2026-11-08 |     13 |       0.7128 |        53 |            64 |
