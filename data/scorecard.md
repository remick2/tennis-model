# Phase 2 scorecard  (Thu Nov 5 1:17AM MT)

Snapshots: 43 runs, Nov 3 to Nov 5 08:17Z. Phase 3 gate: price flags beat the close on average (CLV > 0 by ~2 SE) over 100+ graded sides.

| group                         |   sides |   avg_price_edge_c |   with_close |   avg_clv_c |   clv_se_c |   beat_close_% |   settled |   won |   roi_% |   roi_se_% |
|:------------------------------|--------:|-------------------:|-------------:|------------:|-----------:|---------------:|----------:|------:|--------:|-----------:|
| price flag (price edge >= 2c) |       1 |               2.04 |            1 |        2.04 |     nan    |         100    |         0 |     0 |  nan    |     nan    |
| model+price flag (alert rule) |       1 |               2.04 |            1 |        2.04 |     nan    |         100    |         0 |     0 |  nan    |     nan    |
| all sides (baseline)          |     143 |              -1.88 |          143 |       -1.87 |       0.11 |           9.79 |       101 |    50 |   16.31 |      14.44 |

## Price flags (most recent 25)

| ts           | source   | player         | opp               |   cost |   pin_fair |   close |   clv |   won |
|:-------------|:---------|:---------------|:------------------|-------:|-----------:|--------:|------:|------:|
| Nov 4 7:17PM | poly     | Carlos Alcaraz | Matteo Berrettini |  0.808 |      0.828 |   0.828 |  0.02 |   nan |

## Tennis Tonic picks (graded vs Kalshi price; edge only if pick_won_% beats market_said_%)

|   graded_picks |   pick_won_% |   market_said_% |   roi_at_kalshi_% |   roi_se_% |   logged_picks |
|---------------:|-------------:|----------------:|------------------:|-----------:|---------------:|
|            115 |        66.09 |           67.14 |             -8.82 |       6.46 |            162 |

## Kalshi + Polymarket arbitrage check (best combo per match, all-in)

| day        |   runs |   best_total |   under_1 |   under_1_005 |
|:-----------|-------:|-------------:|----------:|--------------:|
| 2026-11-03 |      4 |       1.0014 |         0 |             4 |
| 2026-11-04 |     22 |       0.9769 |         3 |             7 |
| 2026-11-05 |     11 |       0.9669 |        10 |            10 |
