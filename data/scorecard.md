# Phase 2 scorecard  (Tue Nov 3 5:44PM MT)

Snapshots: 11 runs, Nov 3 to Nov 4 00:07Z. Phase 3 gate: price flags beat the close on average (CLV > 0 by ~2 SE) over 100+ graded sides.

| group                         |   sides |   avg_price_edge_c |   with_close |   avg_clv_c |   clv_se_c |   beat_close_% |   settled |   won |   roi_% |   roi_se_% |
|:------------------------------|--------:|-------------------:|-------------:|------------:|-----------:|---------------:|----------:|------:|--------:|-----------:|
| price flag (price edge >= 2c) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |      nan   |
| model+price flag (alert rule) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |      nan   |
| all sides (baseline)          |      99 |              -1.86 |           99 |       -1.86 |       0.12 |           9.09 |        47 |    23 |   -4.45 |       15.3 |

## Tennis Tonic picks (graded vs Kalshi price; edge only if pick_won_% beats market_said_%)

|   graded_picks |   pick_won_% |   market_said_% |   roi_at_kalshi_% |   roi_se_% |   logged_picks |
|---------------:|-------------:|----------------:|------------------:|-----------:|---------------:|
|             56 |        71.43 |            66.7 |              -0.6 |       9.02 |            152 |

## Kalshi + Polymarket arbitrage check (best combo per match, all-in)

| day        |   runs |   best_total |   under_1 |   under_1_005 |
|:-----------|-------:|-------------:|----------:|--------------:|
| 2026-11-03 |      4 |       1.0014 |         0 |             4 |
| 2026-11-04 |      1 |       0.9769 |         1 |             2 |
