# Dry-run bot (Mon Nov 16 8:49PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$444.61**, Polymarket US **$379.29**; locked in 0 open matches: $0.00
- Bankroll now (cash + open at cost): **$823.90**
- Fires: 40 · settled: 31 · settled P&L **$+169.90** (includes unwinds: $-46.02)
- Paper rebalances (times Remick would have had to move money between venues): 7 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 40 fires, 38 traded, 7 with one leg short · simulated $123.88 vs $115.63 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 318 ms, fill check 60 ms

## Last 15 fires

| ts                        | key                    | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:-----------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-16T17:31:12+00:00 | brancaccio v costoulas | True   | polyus_first |      176 |  0.9841 |       2.79 |          0 |        176 |        -5.14 |        -5.14 |         -5.14 |
| 2026-11-16T20:27:28+00:00 | dominko v viiala       | True   | polyus_first |      179 |  0.9942 |       1.04 |        179 |        179 |         0    |         1.04 |          1.04 |
| 2026-11-16T21:08:03+00:00 | charlton v zamora      | True   | polyus_first |      191 |  0.9103 |      17.14 |          0 |          0 |         0    |         0    |         -4.64 |
| 2026-11-16T21:28:26+00:00 | strakhova v tikhonova  | True   | polyus_first |      289 |  0.9646 |      10.24 |        289 |          0 |       -12.72 |       -12.72 |        -12.72 |
| 2026-11-16T22:01:40+00:00 | kennedy v krueger      | True   | polyus_first |      113 |  0.9683 |       3.58 |        113 |        113 |         0    |         3.58 |          3.58 |
| 2026-11-16T22:34:38+00:00 | strakhova v tikhonova  | True   | polyus_first |      101 |  0.9899 |       1.02 |        101 |          0 |        -3.88 |        -3.88 |         -3.88 |
| 2026-11-16T23:32:40+00:00 | strakhova v tikhonova  | True   | polyus_first |      127 |  0.9861 |       1.76 |        127 |          0 |        -3.59 |        -3.59 |         -3.59 |
| 2026-11-16T23:36:40+00:00 | strakhova v tikhonova  | True   | polyus_first |      222 |  0.9775 |       4.99 |          0 |        222 |        -9.21 |        -9.21 |         -9.21 |
| 2026-11-17T00:37:07+00:00 | chan v mmoh            | True   | polyus_first |      218 |  0.9795 |       4.46 |        218 |        218 |         0    |         4.46 |          4.46 |
| 2026-11-17T00:50:09+00:00 | chan v mmoh            | True   | polyus_first |      172 |  0.9852 |       2.54 |        172 |        172 |         0    |         2.54 |          2.54 |
| 2026-11-17T01:27:54+00:00 | dellavedova v kubler   | True   | polyus_first |      184 |  0.991  |       1.65 |        184 |        184 |         0    |         1.65 |          1.65 |
| 2026-11-17T01:36:44+00:00 | dellavedova v kubler   | True   | polyus_first |      170 |  0.9841 |       2.7  |        170 |        170 |         0    |         2.7  |          2.7  |
| 2026-11-17T01:42:24+00:00 | dellavedova v kubler   | True   | polyus_first |      111 |  0.9873 |       1.41 |        111 |        111 |         0    |         1.41 |          1.2  |
| 2026-11-17T02:35:10+00:00 | delaney v marinkov     | True   | polyus_first |      284 |  0.9947 |       1.5  |        284 |        284 |         0    |         1.5  |          1.5  |
| 2026-11-17T02:57:42+00:00 | delaney v marinkov     | True   | polyus_first |      336 |  0.853  |      49.4  |        336 |        336 |         0    |        49.4  |         49.4  |
