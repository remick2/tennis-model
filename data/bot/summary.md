# Dry-run bot (Thu Nov 19 11:10PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$23.09**, Polymarket US **$229.24**; locked in 4 open matches: $713.60
- Bankroll now (cash + open at cost): **$965.93**
- Fires: 97 · settled: 78 · settled P&L **$+333.66** (includes unwinds: $-73.49)
- Paper rebalances (times Remick would have had to move money between venues): 18 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 97 fires, 94 traded, 14 with one leg short · simulated $272.35 vs $268.87 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 322 ms, fill check 63 ms

## Last 15 fires

| ts                        | key               | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-19T02:33:03+00:00 | banerjee v blanch | True   | polyus_first |      158 |  0.9911 |       1.41 |        158 |        158 |            0 |         1.42 |          1.42 |
| 2026-11-19T03:34:37+00:00 | friend v noguchi  | True   | polyus_first |      211 |  0.9817 |       3.86 |        211 |        211 |            0 |         3.86 |          3.86 |
| 2026-11-19T03:42:11+00:00 | samrej v staeheli | True   | polyus_first |      154 |  0.9934 |       1.01 |        154 |        154 |            0 |         1.01 |          1.01 |
| 2026-11-19T03:58:55+00:00 | friend v noguchi  | True   | polyus_first |      146 |  0.987  |       1.9  |        146 |        146 |            0 |         1.9  |          1.9  |
| 2026-11-19T04:00:06+00:00 | friend v noguchi  | True   | polyus_first |       71 |  0.9762 |       1.69 |         71 |         71 |            0 |         1.69 |          1.69 |
| 2026-11-19T04:09:50+00:00 | friend v noguchi  | True   | polyus_first |      137 |  0.9723 |       3.8  |        137 |        137 |            0 |         3.8  |          3.8  |
| 2026-11-19T04:12:31+00:00 | friend v noguchi  | True   | polyus_first |       50 |  0.88   |       6    |         50 |         50 |            0 |         6    |          6    |
| 2026-11-19T04:13:47+00:00 | friend v noguchi  | True   | polyus_first |      129 |  0.9709 |       3.76 |        129 |        129 |            0 |         3.76 |          3.76 |
| 2026-11-19T04:14:18+00:00 | friend v noguchi  | True   | polyus_first |       88 |  0.9744 |       2.25 |         88 |         88 |            0 |         2.25 |          2.25 |
| 2026-11-19T09:12:28+00:00 | alcaraz v cobolli | False  | polyus_first |      180 |  0.9912 |       1.59 |        180 |        180 |            0 |         1.6  |          1.6  |
| 2026-11-19T09:14:34+00:00 | alcaraz v cobolli | False  | polyus_first |      180 |  0.9912 |       1.59 |        180 |        180 |            0 |         1.6  |          1.6  |
| 2026-11-19T09:16:45+00:00 | alcaraz v cobolli | False  | polyus_first |      180 |  0.9912 |       1.59 |        180 |        180 |            0 |         1.6  |          1.6  |
| 2026-11-19T09:18:52+00:00 | alcaraz v cobolli | False  | polyus_first |      180 |  0.9912 |       1.59 |        180 |        180 |            0 |         1.6  |          1.6  |
| 2026-11-19T18:54:40+00:00 | gaston v mayot    | True   | polyus_first |       57 |  0.9814 |       1.06 |         57 |         57 |            0 |         1.06 |          1.06 |
| 2026-11-20T00:18:39+00:00 | lee v martin      | True   | polyus_first |      154 |  0.9842 |       2.43 |        154 |        154 |            0 |         2.43 |          2.43 |
