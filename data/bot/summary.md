# Dry-run bot (Wed Nov 18 8:55PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$443.03**, Polymarket US **$289.03**; locked in 1 open matches: $207.14
- Bankroll now (cash + open at cost): **$939.20**
- Fires: 85 · settled: 69 · settled P&L **$+306.91** (includes unwinds: $-73.49)
- Paper rebalances (times Remick would have had to move money between venues): 15 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 85 fires, 82 traded, 14 with one leg short · simulated $243.06 vs $239.58 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 329 ms, fill check 64 ms

## Last 15 fires

| ts                        | key                | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:-------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
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
| 2026-11-19T02:11:05+00:00 | bouzige v gorzny   | True   | polyus_first |       94 |  0.9676 |       3.05 |         94 |      94    |         0    |         3.05 |          3.05 |
| 2026-11-19T02:27:43+00:00 | bouzige v gorzny   | True   | polyus_first |      167 |  0.9926 |       1.24 |        167 |     167    |         0    |         1.24 |          1.24 |
| 2026-11-19T02:33:03+00:00 | banerjee v blanch  | True   | polyus_first |      158 |  0.9911 |       1.41 |        158 |     158    |         0    |         1.42 |          1.42 |
| 2026-11-19T03:34:37+00:00 | friend v noguchi   | True   | polyus_first |      211 |  0.9817 |       3.86 |        211 |     211    |         0    |         3.86 |          3.86 |
| 2026-11-19T03:42:11+00:00 | samrej v staeheli  | True   | polyus_first |      154 |  0.9934 |       1.01 |        154 |     154    |         0    |         1.01 |          1.01 |
