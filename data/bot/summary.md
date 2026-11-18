# Dry-run bot (Tue Nov 17 5:37PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$220.93**, Polymarket US **$220.93**; locked in 2 open matches: $400.84
- Bankroll now (cash + open at cost): **$842.70**
- Fires: 55 · settled: 40 · settled P&L **$+203.45** (includes unwinds: $-60.76)
- Paper rebalances (times Remick would have had to move money between venues): 9 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 55 fires, 52 traded, 10 with one leg short · simulated $150.85 vs $140.44 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 420 ms, fill check 64 ms

## Last 15 fires

| ts                        | key                  | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:---------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
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
| 2026-11-17T23:31:16+00:00 | garcia v gatica      | True   | polyus_first |       74 |  0.9826 |       1.29 |          0 |         74 |        -2.8  |        -2.8  |         -2.8  |
| 2026-11-18T00:18:24+00:00 | nicholas v zahraj    | True   | polyus_first |      239 |  0.9721 |       6.68 |        239 |        239 |         0    |         6.68 |          6.68 |
| 2026-11-18T00:32:47+00:00 | nicholas v zahraj    | True   | polyus_first |      170 |  0.9913 |       1.48 |        170 |        170 |         0    |         1.48 |          1.48 |
