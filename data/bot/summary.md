# Dry-run bot (Mon Nov 16 10:04PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$284.37**, Polymarket US **$219.06**; locked in 2 open matches: $320.47
- Bankroll now (cash + open at cost): **$823.90**
- Fires: 43 · settled: 31 · settled P&L **$+169.90** (includes unwinds: $-46.02)
- Paper rebalances (times Remick would have had to move money between venues): 7 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 43 fires, 40 traded, 7 with one leg short · simulated $127.41 vs $117.00 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 300 ms, fill check 58 ms

## Last 15 fires

| ts                        | key                   | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:----------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-16T21:28:26+00:00 | strakhova v tikhonova | True   | polyus_first |      289 |  0.9646 |      10.24 |        289 |          0 |       -12.72 |       -12.72 |        -12.72 |
| 2026-11-16T22:01:40+00:00 | kennedy v krueger     | True   | polyus_first |      113 |  0.9683 |       3.58 |        113 |        113 |         0    |         3.58 |          3.58 |
| 2026-11-16T22:34:38+00:00 | strakhova v tikhonova | True   | polyus_first |      101 |  0.9899 |       1.02 |        101 |          0 |        -3.88 |        -3.88 |         -3.88 |
| 2026-11-16T23:32:40+00:00 | strakhova v tikhonova | True   | polyus_first |      127 |  0.9861 |       1.76 |        127 |          0 |        -3.59 |        -3.59 |         -3.59 |
| 2026-11-16T23:36:40+00:00 | strakhova v tikhonova | True   | polyus_first |      222 |  0.9775 |       4.99 |          0 |        222 |        -9.21 |        -9.21 |         -9.21 |
| 2026-11-17T00:37:07+00:00 | chan v mmoh           | True   | polyus_first |      218 |  0.9795 |       4.46 |        218 |        218 |         0    |         4.46 |          4.46 |
| 2026-11-17T00:50:09+00:00 | chan v mmoh           | True   | polyus_first |      172 |  0.9852 |       2.54 |        172 |        172 |         0    |         2.54 |          2.54 |
| 2026-11-17T01:27:54+00:00 | dellavedova v kubler  | True   | polyus_first |      184 |  0.991  |       1.65 |        184 |        184 |         0    |         1.65 |          1.65 |
| 2026-11-17T01:36:44+00:00 | dellavedova v kubler  | True   | polyus_first |      170 |  0.9841 |       2.7  |        170 |        170 |         0    |         2.7  |          2.7  |
| 2026-11-17T01:42:24+00:00 | dellavedova v kubler  | True   | polyus_first |      111 |  0.9873 |       1.41 |        111 |        111 |         0    |         1.41 |          1.2  |
| 2026-11-17T02:35:10+00:00 | delaney v marinkov    | True   | polyus_first |      284 |  0.9947 |       1.5  |        284 |        284 |         0    |         1.5  |          1.5  |
| 2026-11-17T02:57:42+00:00 | delaney v marinkov    | True   | polyus_first |      336 |  0.853  |      49.4  |        336 |        336 |         0    |        49.4  |         49.4  |
| 2026-11-17T04:13:25+00:00 | staeheli v zhang      | True   | polyus_first |      134 |  0.9284 |       9.59 |          0 |          0 |         0    |         0    |         -2.16 |
| 2026-11-17T05:01:17+00:00 | li tu v mccabe        | True   | polyus_first |      162 |  0.9891 |       1.76 |        162 |        162 |         0    |         1.76 |          1.76 |
| 2026-11-17T05:01:40+00:00 | li tu v mccabe        | True   | polyus_first |      162 |  0.9891 |       1.77 |        162 |        162 |         0    |         1.77 |          1.77 |
