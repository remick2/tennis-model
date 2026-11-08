# Weekly review (Sat Nov 07 2026)

## Arb scanner deep dive

Hourly snapshots, US venues only (Kalshi + Polymarket US): 507 match-runs, 114 matches.
Best all-in total per match-run: p1 1.0137, p5 1.0187, p25 1.0301, median 1.034.

| slice            |   n |   under_1 |   within_0.5c |   within_1c |   best |
|:-----------------|----:|----------:|--------------:|------------:|-------:|
| all              | 507 |         0 |             0 |           1 |  1.007 |
| phase=pre-match  | 507 |         0 |             0 |           1 |  1.007 |
| level=challenger | 342 |         0 |             0 |           1 |  1.007 |
| level=main       | 165 |         0 |             0 |           0 |  1.014 |
| fav_venue=kalshi | 243 |         0 |             0 |           0 |  1.011 |
| fav_venue=polyus | 264 |         0 |             0 |           1 |  1.007 |

By hour (MT):

|   hour_MT |      n |   within_1c |   best |
|----------:|-------:|------------:|-------:|
|     0.000 | 13.000 |       0.000 |  1.014 |
|     1.000 | 31.000 |       0.000 |  1.014 |
|     2.000 | 25.000 |       0.000 |  1.014 |
|     3.000 | 21.000 |       0.000 |  1.014 |
|     4.000 | 34.000 |       0.000 |  1.017 |
|     5.000 | 18.000 |       0.000 |  1.024 |
|     6.000 | 38.000 |       1.000 |  1.007 |
|     7.000 | 20.000 |       0.000 |  1.014 |
|     8.000 | 21.000 |       0.000 |  1.023 |
|     9.000 | 19.000 |       0.000 |  1.014 |
|    10.000 | 22.000 |       0.000 |  1.014 |
|    11.000 | 22.000 |       0.000 |  1.014 |
|    12.000 | 22.000 |       0.000 |  1.014 |
|    13.000 | 11.000 |       0.000 |  1.030 |
|    14.000 | 11.000 |       0.000 |  1.021 |
|    15.000 | 28.000 |       0.000 |  1.025 |
|    16.000 | 17.000 |       0.000 |  1.020 |
|    17.000 | 16.000 |       0.000 |  1.014 |
|    18.000 | 24.000 |       0.000 |  1.011 |
|    19.000 | 24.000 |       0.000 |  1.010 |
|    20.000 | 21.000 |       0.000 |  1.019 |
|    21.000 | 20.000 |       0.000 |  1.019 |
|    22.000 | 14.000 |       0.000 |  1.022 |
|    23.000 | 15.000 |       0.000 |  1.014 |

1-minute scanner: 64 scans (2026-11-08T01:16 to 2026-11-08T02:19Z), median 27 matched matches/scan, best 0.934; scans with best < $1.01: 18, < $1.005: 16.
Sub-$1 combo rows: 9 (9 live); executable (≥ $1 locked): 1 rows on 1 matches. Rows with zero verified depth: 8 (quote moved before the book check).
Lifetimes (any): n=7, median upper bound 1.0 min, lower bound nan min.

Maker on one leg (post bid+1c, take the other venue; hourly snapshots, fills NOT modeled):

| polyus_rebate   | maker_venue   |   pairs |   under_1 |   under_0.99 |   median_total |
|:----------------|:--------------|--------:|----------:|-------------:|---------------:|
| 0%              | kalshi        |    2968 |        55 |           20 |          1.021 |
| 0%              | polyus        |    2968 |        68 |            5 |          1.017 |
| 25%             | kalshi        |    2968 |        55 |           20 |          1.021 |
| 25%             | polyus        |    2968 |        90 |            8 |          1.013 |

## Price-flag near-misses (price edge 0–2c) and CLV slices

First-sighting sides with Pinnacle fair: 191 (43 matches); near-misses (edge 0–2c): 6, of which US venues: 3.

| slice         |   sides |   matches |   avg_clv_c |   se_c |   beat_close_% |   near_miss |
|:--------------|--------:|----------:|------------:|-------:|---------------:|------------:|
| source=kalshi |      86 |        43 |      -2.103 |  0.058 |         10.465 |           3 |
| source=poly   |      85 |        43 |      -1.657 |  0.051 |         12.941 |           3 |
| source=polyus |      20 |        10 |      -2.087 |  0.072 |          5.000 |           0 |
| tour=atp      |     191 |        43 |      -1.889 |  0.044 |         10.995 |           6 |
| level=main    |     191 |        43 |      -1.889 |  0.044 |         10.995 |           6 |
| hrs_b=0-3h    |       6 |         2 |      -1.947 |  0.199 |          0.000 |           0 |
| hrs_b=3-12h   |      67 |        19 |      -1.965 |  0.060 |          7.463 |           3 |
| hrs_b=12h+    |     118 |        27 |      -1.861 |  0.059 |         13.559 |           3 |
| role=favorite |      96 |        43 |      -1.823 |  0.204 |         11.458 |           1 |
| role=underdog |      95 |        43 |      -1.950 |  0.215 |         10.526 |           5 |

Slices tested: 10. With that many, expect ~0.2 to look 2 SE good by chance.

## Data quality

Latest snapshot: Kalshi 28 matches, Polymarket US 96, matched 28; Kalshi-only 0, Polymarket-US-only 68.
Possible unmatched name pairs (one shared surname): 0
US-venue rows missing ask: 0 of 14134; missing start time: 0.
kalshi: start time moved > 2h between snapshots for 23 of 333 matches (order-of-play changes; 'hours before start' uses the first-sighting start).
polyus: start time moved > 2h between snapshots for 16 of 218 matches (order-of-play changes; 'hours before start' uses the first-sighting start).
Pinnacle quote age at pull: median 0 min, >60 min: 0.
