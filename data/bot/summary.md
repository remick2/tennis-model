# Dry-run bot (Wed Nov 18 6:45PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$364.24**, Polymarket US **$364.24**; locked in 1 open matches: $201.31
- Bankroll now (cash + open at cost): **$929.79**
- Fires: 80 · settled: 64 · settled P&L **$+297.50** (includes unwinds: $-73.49)
- Paper rebalances (times Remick would have had to move money between venues): 14 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 80 fires, 77 traded, 14 with one leg short · simulated $232.48 vs $229.00 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 342 ms, fill check 64 ms

## Last 15 fires

| ts                        | key                | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:-------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-18T14:22:28+00:00 | donald v taberner  | True   | polyus_first |      172 |  0.9353 |      11.13 |        172 |       0    |        -2.97 |        -2.97 |         -2.97 |
| 2026-11-18T20:22:28+00:00 | baris v tarvet     | True   | polyus_first |      172 |  0.9853 |       2.53 |          0 |     172    |        -3.98 |        -3.98 |         -3.98 |
| 2026-11-19T00:00:32+00:00 | kennedy v maxted   | True   | polyus_first |      123 |  0.9843 |       1.93 |        123 |     123    |         0    |         1.93 |          1.93 |
| 2026-11-19T00:17:08+00:00 | broska v langmo    | True   | polyus_first |      228 |  0.9399 |      13.71 |        228 |     228    |         0    |        13.71 |         13.71 |
| 2026-11-19T00:26:14+00:00 | geerlings v samson | True   | polyus_first |      243 |  0.9928 |       1.74 |        243 |     243    |         0    |         1.74 |          1.74 |
| 2026-11-19T00:26:56+00:00 | geerlings v samson | True   | polyus_first |      182 |  0.9827 |       3.15 |        182 |     182    |         0    |         3.16 |          3.16 |
| 2026-11-19T00:37:16+00:00 | broska v langmo    | True   | polyus_first |       95 |  0.9816 |       1.75 |         95 |      95    |         0    |         1.75 |          1.75 |
| 2026-11-19T00:45:58+00:00 | chan v kasnikowski | True   | polyus_first |       68 |  0.9754 |       1.67 |         68 |      68    |         0    |         1.67 |          1.67 |
| 2026-11-19T00:48:26+00:00 | alberto v boyer    | True   | polyus_first |       73 |  0.9785 |       1.57 |         73 |      73    |         0    |         1.57 |          1.57 |
| 2026-11-19T00:49:44+00:00 | alberto v boyer    | True   | polyus_first |      251 |  0.9828 |       4.32 |        251 |     251    |         0    |        11.66 |         11.66 |
| 2026-11-19T00:54:39+00:00 | alberto v boyer    | True   | polyus_first |       78 |  0.9856 |       1.12 |          0 |      78    |        -5.78 |        -5.78 |          1.12 |
| 2026-11-19T00:57:19+00:00 | alberto v boyer    | True   | polyus_first |      138 |  0.9743 |       3.55 |        138 |     136.36 |         0    |         3.52 |          3.55 |
| 2026-11-19T01:02:32+00:00 | alberto v boyer    | True   | polyus_first |      192 |  0.9944 |       1.08 |        192 |     192    |         0    |         1.08 |          1.08 |
| 2026-11-19T01:06:02+00:00 | alberto v boyer    | True   | polyus_first |      175 |  0.9574 |       7.46 |        175 |     175    |         0    |         7.47 |          7.47 |
| 2026-11-19T01:35:08+00:00 | banerjee v blanch  | True   | polyus_first |      204 |  0.9868 |       2.69 |        204 |     204    |         0    |         2.69 |          2.69 |
