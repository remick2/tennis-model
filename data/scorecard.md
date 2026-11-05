# Phase 2 scorecard  (Thu Nov 5 6:17AM MT)

Snapshots: 49 runs, Nov 3 to Nov 5 13:17Z. Phase 3 gate (GATE row): US-venue price flags beat the close on average (CLV > 0 by ~2 SE) over 100+ graded sides.

| group                                                  |   sides |   avg_price_edge_c |   with_close |   avg_clv_c |   clv_se_c |   beat_close_% |   settled |   won |   roi_% |   roi_se_% |
|:-------------------------------------------------------|--------:|-------------------:|-------------:|------------:|-----------:|---------------:|----------:|------:|--------:|-----------:|
| GATE: price flag on US venues (Kalshi + Polymarket US) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |     nan    |
| price flag, all venues incl. Polymarket intl           |       1 |               2.04 |            1 |        3.18 |     nan    |         100    |         0 |     0 |  nan    |     nan    |
| model+price flag (alert rule)                          |       1 |               2.04 |            1 |        3.18 |     nan    |         100    |         0 |     0 |  nan    |     nan    |
| all sides (baseline)                                   |     143 |              -1.88 |          143 |       -1.87 |       0.12 |          11.19 |       105 |    52 |   14.43 |      13.98 |

## Tennis Tonic picks (graded vs Kalshi price; edge only if pick_won_% beats market_said_%)

|   graded_picks |   pick_won_% |   market_said_% |   roi_at_kalshi_% |   roi_se_% |   logged_picks |
|---------------:|-------------:|----------------:|------------------:|-----------:|---------------:|
|            120 |        66.67 |           67.29 |             -8.23 |       6.28 |            212 |

## Kalshi + Polymarket arbitrage check (best combo per match, all-in)

| day        |   runs |   best_total |   under_1 |   under_1_005 |
|:-----------|-------:|-------------:|----------:|--------------:|
| 2026-11-03 |      4 |       1.0014 |         0 |             4 |
| 2026-11-04 |     22 |       0.9769 |         3 |             7 |
| 2026-11-05 |     17 |       0.6918 |        11 |            12 |
