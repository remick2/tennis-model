# Phase 2 scorecard  (Wed Nov 4 3:17PM MT)

Snapshots: 31 runs, Nov 3 to Nov 4 22:17Z. Phase 3 gate: price flags beat the close on average (CLV > 0 by ~2 SE) over 100+ graded sides.

| group                         |   sides |   avg_price_edge_c |   with_close |   avg_clv_c |   clv_se_c |   beat_close_% |   settled |   won |   roi_% |   roi_se_% |
|:------------------------------|--------:|-------------------:|-------------:|------------:|-----------:|---------------:|----------:|------:|--------:|-----------:|
| price flag (price edge >= 2c) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |     nan    |
| model+price flag (alert rule) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |     nan    |
| all sides (baseline)          |     123 |              -1.86 |          123 |       -1.85 |       0.12 |          10.57 |       101 |    50 |   16.31 |      14.44 |

## Tennis Tonic picks (graded vs Kalshi price; edge only if pick_won_% beats market_said_%)

|   graded_picks |   pick_won_% |   market_said_% |   roi_at_kalshi_% |   roi_se_% |   logged_picks |
|---------------:|-------------:|----------------:|------------------:|-----------:|---------------:|
|            107 |        65.42 |           66.93 |             -9.39 |       6.75 |            162 |

## Kalshi + Polymarket arbitrage check (best combo per match, all-in)

| day        |   runs |   best_total |   under_1 |   under_1_005 |
|:-----------|-------:|-------------:|----------:|--------------:|
| 2026-11-03 |      4 |       1.0014 |         0 |             4 |
| 2026-11-04 |     21 |       0.9769 |         3 |             7 |
