# Phase 2 scorecard  (Fri Nov 6 10:17AM MT)

Snapshots: 82 runs, Nov 3 to Nov 6 17:17Z. Phase 3 gate (GATE row): US-venue price flags beat the close on average (CLV > 0 by ~2 SE) over 100+ graded sides.

| group                                                  |   sides |   avg_price_edge_c |   with_close |   avg_clv_c |   clv_se_c |   beat_close_% |   settled |   won |   roi_% |   roi_se_% |
|:-------------------------------------------------------|--------:|-------------------:|-------------:|------------:|-----------:|---------------:|----------:|------:|--------:|-----------:|
| GATE: price flag on US venues (Kalshi + Polymarket US) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |     nan    |
| price flag, all venues incl. Polymarket intl           |       1 |               2.04 |            1 |        3.18 |     nan    |         100    |         1 |     0 |  -38.12 |     nan    |
| model+price flag (alert rule)                          |       1 |               2.04 |            1 |        3.18 |     nan    |         100    |         1 |     0 |  -38.12 |     nan    |
| all sides (baseline)                                   |     173 |              -1.91 |          173 |       -1.91 |       0.11 |           9.83 |       153 |    76 |   10.25 |      10.52 |

## Tennis Tonic picks (graded vs Kalshi price; edge only if pick_won_% beats market_said_%)

|   graded_picks |   pick_won_% |   market_said_% |   roi_at_kalshi_% |   roi_se_% |   logged_picks |
|---------------:|-------------:|----------------:|------------------:|-----------:|---------------:|
|            163 |        65.64 |           65.96 |             -7.47 |       5.57 |            227 |

## Kalshi + Polymarket arbitrage check (best combo per match, all-in)

| day        |   runs |   best_total |   under_1 |   under_1_005 |
|:-----------|-------:|-------------:|----------:|--------------:|
| 2026-11-03 |      4 |       1.0014 |         0 |             4 |
| 2026-11-04 |     22 |       0.9769 |         3 |             7 |
| 2026-11-05 |     29 |       0.6918 |        17 |            19 |
| 2026-11-06 |     21 |       0.9679 |         2 |             2 |
