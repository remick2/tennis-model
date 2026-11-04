# Phase 2 scorecard  (Wed Nov 4 12:17PM MT)

Snapshots: 27 runs, Nov 3 to Nov 4 19:17Z. Phase 3 gate: price flags beat the close on average (CLV > 0 by ~2 SE) over 100+ graded sides.

| group                         |   sides |   avg_price_edge_c |   with_close |   avg_clv_c |   clv_se_c |   beat_close_% |   settled |   won |   roi_% |   roi_se_% |
|:------------------------------|--------:|-------------------:|-------------:|------------:|-----------:|---------------:|----------:|------:|--------:|-----------:|
| price flag (price edge >= 2c) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |     nan    |
| model+price flag (alert rule) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |     nan    |
| all sides (baseline)          |     111 |              -1.86 |          111 |       -1.85 |       0.13 |          11.71 |        87 |    43 |   22.65 |      16.31 |

## Tennis Tonic picks (graded vs Kalshi price; edge only if pick_won_% beats market_said_%)

|   graded_picks |   pick_won_% |   market_said_% |   roi_at_kalshi_% |   roi_se_% |   logged_picks |
|---------------:|-------------:|----------------:|------------------:|-----------:|---------------:|
|             97 |        64.95 |           66.72 |              -9.7 |       7.16 |            162 |

## Kalshi + Polymarket arbitrage check (best combo per match, all-in)

| day        |   runs |   best_total |   under_1 |   under_1_005 |
|:-----------|-------:|-------------:|----------:|--------------:|
| 2026-11-03 |      4 |       1.0014 |         0 |             4 |
| 2026-11-04 |     17 |       0.9769 |         3 |             7 |
