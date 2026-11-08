# Phase 2 scorecard  (Sun Nov 8 4:17PM MT)

Snapshots: 147 runs, Nov 3 to Nov 8 23:17Z. Phase 3 gate (GATE row): US-venue price flags beat the close on average (CLV > 0 by ~2 SE) over 100+ graded sides.

| group                                                  |   sides |   avg_price_edge_c |   with_close |   avg_clv_c |   clv_se_c |   beat_close_% |   settled |   won |   roi_% |   roi_se_% |
|:-------------------------------------------------------|--------:|-------------------:|-------------:|------------:|-----------:|---------------:|----------:|------:|--------:|-----------:|
| GATE: price flag on US venues (Kalshi + Polymarket US) |       0 |             nan    |          nan |      nan    |     nan    |         nan    |       nan |   nan |  nan    |     nan    |
| price flag, all venues incl. Polymarket intl           |       2 |               2.16 |            2 |        2.56 |       0.62 |         100    |         2 |     1 |   -0.57 |      37.55 |
| model+price flag (alert rule)                          |       2 |               2.16 |            2 |        2.56 |       0.62 |         100    |         2 |     1 |   -0.57 |      37.55 |
| all sides (baseline)                                   |     191 |              -1.9  |          191 |       -1.9  |       0.11 |          10.47 |       177 |    88 |    4.73 |       9.36 |

## Kalshi + Polymarket arbitrage check (best combo per match, all-in)

| day        |   runs |   best_total |   under_1 |   under_1_005 |
|:-----------|-------:|-------------:|----------:|--------------:|
| 2026-11-03 |      4 |       1.0014 |         0 |             4 |
| 2026-11-04 |     22 |       0.9769 |         3 |             7 |
| 2026-11-05 |     29 |       0.6918 |        17 |            19 |
| 2026-11-06 |     29 |       0.9679 |         2 |             2 |
| 2026-11-07 |     28 |       0.8883 |        69 |           109 |
| 2026-11-08 |     29 |       0.6709 |       128 |           147 |
