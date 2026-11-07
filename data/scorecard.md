# Phase 2 scorecard  (Fri Nov 6 10:17PM MT)

Snapshots: 97 runs, Nov 3 to Nov 7 05:17Z. Phase 3 gate (GATE row): US-venue price flags beat the close on average (CLV > 0 by ~2 SE) over 100+ graded sides.

| group                                                  |   sides |   avg_price_edge_c |   with_close |   avg_clv_c |   clv_se_c |   beat_close_% |   settled |   won |   roi_% |   roi_se_% |
|:-------------------------------------------------------|--------:|-------------------:|-------------:|------------:|-----------:|---------------:|----------:|------:|--------:|-----------:|
| GATE: price flag on US venues (Kalshi + Polymarket US) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |     nan    |
| price flag, all venues incl. Polymarket intl           |       2 |               2.16 |            2 |        2.73 |       0.45 |         100    |         1 |     0 |  -38.12 |     nan    |
| model+price flag (alert rule)                          |       2 |               2.16 |            2 |        2.73 |       0.45 |         100    |         1 |     0 |  -38.12 |     nan    |
| all sides (baseline)                                   |     183 |              -1.9  |          183 |       -1.9  |       0.11 |           9.84 |       167 |    83 |    7.15 |       9.81 |

## Tennis Tonic picks (graded vs Kalshi price; edge only if pick_won_% beats market_said_%)

|   graded_picks |   pick_won_% |   market_said_% |   roi_at_kalshi_% |   roi_se_% |   logged_picks |
|---------------:|-------------:|----------------:|------------------:|-----------:|---------------:|
|            173 |         65.9 |           65.46 |             -6.24 |       5.44 |            227 |

## Kalshi + Polymarket arbitrage check (best combo per match, all-in)

| day        |   runs |   best_total |   under_1 |   under_1_005 |
|:-----------|-------:|-------------:|----------:|--------------:|
| 2026-11-03 |      4 |       1.0014 |         0 |             4 |
| 2026-11-04 |     22 |       0.9769 |         3 |             7 |
| 2026-11-05 |     29 |       0.6918 |        17 |            19 |
| 2026-11-06 |     29 |       0.9679 |         2 |             2 |
| 2026-11-07 |      7 |       0.9828 |         1 |             8 |
