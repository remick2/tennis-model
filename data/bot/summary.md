# Dry-run bot (Wed Nov 18 10:55PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$481.22**, Polymarket US **$481.22**; locked in 0 open matches: $0.00
- Bankroll now (cash + open at cost): **$962.44**
- Fires: 91 · settled: 76 · settled P&L **$+330.17** (includes unwinds: $-73.49)
- Paper rebalances (times Remick would have had to move money between venues): 17 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 91 fires, 88 traded, 14 with one leg short · simulated $262.46 vs $258.98 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 318 ms, fill check 62 ms

## Last 15 fires

| ts                        | key               | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-19T00:57:19+00:00 | alberto v boyer   | True   | polyus_first |      138 |  0.9743 |       3.55 |        138 |     136.36 |            0 |         3.52 |          3.55 |
| 2026-11-19T01:02:32+00:00 | alberto v boyer   | True   | polyus_first |      192 |  0.9944 |       1.08 |        192 |     192    |            0 |         1.08 |          1.08 |
| 2026-11-19T01:06:02+00:00 | alberto v boyer   | True   | polyus_first |      175 |  0.9574 |       7.46 |        175 |     175    |            0 |         7.47 |          7.47 |
| 2026-11-19T01:35:08+00:00 | banerjee v blanch | True   | polyus_first |      204 |  0.9868 |       2.69 |        204 |     204    |            0 |         2.69 |          2.69 |
| 2026-11-19T02:11:05+00:00 | bouzige v gorzny  | True   | polyus_first |       94 |  0.9676 |       3.05 |         94 |      94    |            0 |         3.05 |          3.05 |
| 2026-11-19T02:27:43+00:00 | bouzige v gorzny  | True   | polyus_first |      167 |  0.9926 |       1.24 |        167 |     167    |            0 |         1.24 |          1.24 |
| 2026-11-19T02:33:03+00:00 | banerjee v blanch | True   | polyus_first |      158 |  0.9911 |       1.41 |        158 |     158    |            0 |         1.42 |          1.42 |
| 2026-11-19T03:34:37+00:00 | friend v noguchi  | True   | polyus_first |      211 |  0.9817 |       3.86 |        211 |     211    |            0 |         3.86 |          3.86 |
| 2026-11-19T03:42:11+00:00 | samrej v staeheli | True   | polyus_first |      154 |  0.9934 |       1.01 |        154 |     154    |            0 |         1.01 |          1.01 |
| 2026-11-19T03:58:55+00:00 | friend v noguchi  | True   | polyus_first |      146 |  0.987  |       1.9  |        146 |     146    |            0 |         1.9  |          1.9  |
| 2026-11-19T04:00:06+00:00 | friend v noguchi  | True   | polyus_first |       71 |  0.9762 |       1.69 |         71 |      71    |            0 |         1.69 |          1.69 |
| 2026-11-19T04:09:50+00:00 | friend v noguchi  | True   | polyus_first |      137 |  0.9723 |       3.8  |        137 |     137    |            0 |         3.8  |          3.8  |
| 2026-11-19T04:12:31+00:00 | friend v noguchi  | True   | polyus_first |       50 |  0.88   |       6    |         50 |      50    |            0 |         6    |          6    |
| 2026-11-19T04:13:47+00:00 | friend v noguchi  | True   | polyus_first |      129 |  0.9709 |       3.76 |        129 |     129    |            0 |         3.76 |          3.76 |
| 2026-11-19T04:14:18+00:00 | friend v noguchi  | True   | polyus_first |       88 |  0.9744 |       2.25 |         88 |      88    |            0 |         2.25 |          2.25 |
