# Dry-run bot (Wed Nov 18 9:10PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$192.72**, Polymarket US **$192.72**; locked in 4 open matches: $553.75
- Bankroll now (cash + open at cost): **$939.19**
- Fires: 88 · settled: 69 · settled P&L **$+306.91** (includes unwinds: $-73.49)
- Paper rebalances (times Remick would have had to move money between venues): 16 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 88 fires, 85 traded, 14 with one leg short · simulated $250.45 vs $246.97 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 325 ms, fill check 63 ms

## Last 15 fires

| ts                        | key               | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-19T00:48:26+00:00 | alberto v boyer   | True   | polyus_first |       73 |  0.9785 |       1.57 |         73 |      73    |         0    |         1.57 |          1.57 |
| 2026-11-19T00:49:44+00:00 | alberto v boyer   | True   | polyus_first |      251 |  0.9828 |       4.32 |        251 |     251    |         0    |        11.66 |         11.66 |
| 2026-11-19T00:54:39+00:00 | alberto v boyer   | True   | polyus_first |       78 |  0.9856 |       1.12 |          0 |      78    |        -5.78 |        -5.78 |          1.12 |
| 2026-11-19T00:57:19+00:00 | alberto v boyer   | True   | polyus_first |      138 |  0.9743 |       3.55 |        138 |     136.36 |         0    |         3.52 |          3.55 |
| 2026-11-19T01:02:32+00:00 | alberto v boyer   | True   | polyus_first |      192 |  0.9944 |       1.08 |        192 |     192    |         0    |         1.08 |          1.08 |
| 2026-11-19T01:06:02+00:00 | alberto v boyer   | True   | polyus_first |      175 |  0.9574 |       7.46 |        175 |     175    |         0    |         7.47 |          7.47 |
| 2026-11-19T01:35:08+00:00 | banerjee v blanch | True   | polyus_first |      204 |  0.9868 |       2.69 |        204 |     204    |         0    |         2.69 |          2.69 |
| 2026-11-19T02:11:05+00:00 | bouzige v gorzny  | True   | polyus_first |       94 |  0.9676 |       3.05 |         94 |      94    |         0    |         3.05 |          3.05 |
| 2026-11-19T02:27:43+00:00 | bouzige v gorzny  | True   | polyus_first |      167 |  0.9926 |       1.24 |        167 |     167    |         0    |         1.24 |          1.24 |
| 2026-11-19T02:33:03+00:00 | banerjee v blanch | True   | polyus_first |      158 |  0.9911 |       1.41 |        158 |     158    |         0    |         1.42 |          1.42 |
| 2026-11-19T03:34:37+00:00 | friend v noguchi  | True   | polyus_first |      211 |  0.9817 |       3.86 |        211 |     211    |         0    |         3.86 |          3.86 |
| 2026-11-19T03:42:11+00:00 | samrej v staeheli | True   | polyus_first |      154 |  0.9934 |       1.01 |        154 |     154    |         0    |         1.01 |          1.01 |
| 2026-11-19T03:58:55+00:00 | friend v noguchi  | True   | polyus_first |      146 |  0.987  |       1.9  |        146 |     146    |         0    |         1.9  |          1.9  |
| 2026-11-19T04:00:06+00:00 | friend v noguchi  | True   | polyus_first |       71 |  0.9762 |       1.69 |         71 |      71    |         0    |         1.69 |          1.69 |
| 2026-11-19T04:09:50+00:00 | friend v noguchi  | True   | polyus_first |      137 |  0.9723 |       3.8  |        137 |     137    |         0    |         3.8  |          3.8  |
