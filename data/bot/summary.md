# Dry-run bot (Tue Nov 17 4:22PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$292.04**, Polymarket US **$384.46**; locked in 1 open matches: $165.93
- Bankroll now (cash + open at cost): **$842.43**
- Fires: 52 · settled: 39 · settled P&L **$+200.38** (includes unwinds: $-57.96)
- Paper rebalances (times Remick would have had to move money between venues): 8 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 52 fires, 49 traded, 9 with one leg short · simulated $145.49 vs $135.08 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 378 ms, fill check 62 ms

## Last 15 fires

| ts                        | key                  | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:---------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-17T01:42:24+00:00 | dellavedova v kubler | True   | polyus_first |      111 |  0.9873 |       1.41 |        111 |        111 |         0    |         1.41 |          1.2  |
| 2026-11-17T02:35:10+00:00 | delaney v marinkov   | True   | polyus_first |      284 |  0.9947 |       1.5  |        284 |        284 |         0    |         1.5  |          1.5  |
| 2026-11-17T02:57:42+00:00 | delaney v marinkov   | True   | polyus_first |      336 |  0.853  |      49.4  |        336 |        336 |         0    |        49.4  |         49.4  |
| 2026-11-17T04:13:25+00:00 | staeheli v zhang     | True   | polyus_first |      134 |  0.9284 |       9.59 |          0 |          0 |         0    |         0    |         -2.16 |
| 2026-11-17T05:01:17+00:00 | li tu v mccabe       | True   | polyus_first |      162 |  0.9891 |       1.76 |        162 |        162 |         0    |         1.76 |          1.76 |
| 2026-11-17T05:01:40+00:00 | li tu v mccabe       | True   | polyus_first |      162 |  0.9891 |       1.77 |        162 |        162 |         0    |         1.77 |          1.77 |
| 2026-11-17T19:07:41+00:00 | angelo v midon       | True   | polyus_first |      130 |  0.9582 |       5.44 |        130 |        130 |         0    |         5.44 |          5.44 |
| 2026-11-17T19:54:22+00:00 | mejia v wessels      | True   | polyus_first |      232 |  0.9917 |       1.92 |        232 |        232 |         0    |         1.92 |          1.92 |
| 2026-11-17T20:07:42+00:00 | mejia v wessels      | True   | polyus_first |      192 |  0.9944 |       1.08 |        192 |        192 |         0    |         1.08 |          1.08 |
| 2026-11-17T20:31:47+00:00 | mejia v wessels      | True   | polyus_first |      180 |  0.9177 |      14.81 |        180 |        180 |         0    |        14.81 |         14.81 |
| 2026-11-17T20:36:23+00:00 | mejia v wessels      | True   | polyus_first |      159 |  0.9799 |       3.2  |          0 |        159 |        -6.97 |        -6.97 |         -6.97 |
| 2026-11-17T20:53:59+00:00 | shelton v zverev     | True   | polyus_first |      164 |  0.9874 |       2.06 |        164 |        164 |         0    |         2.06 |          2.06 |
| 2026-11-17T21:44:06+00:00 | papamichail v samson | True   | polyus_first |      251 |  0.9935 |       1.64 |        251 |        251 |         0    |         1.64 |          1.64 |
| 2026-11-17T22:11:58+00:00 | papamichail v samson | True   | polyus_first |      182 |  0.9822 |       3.24 |        182 |          0 |        -4.97 |        -4.97 |         -4.97 |
| 2026-11-17T22:52:31+00:00 | aguilar v jover      | True   | polyus_first |      169 |  0.9819 |       3.06 |        169 |        169 |         0    |         3.07 |          3.07 |
