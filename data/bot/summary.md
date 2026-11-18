# Dry-run bot (Tue Nov 17 6:17PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$255.00**, Polymarket US **$167.45**; locked in 3 open matches: $428.41
- Bankroll now (cash + open at cost): **$850.86**
- Fires: 58 · settled: 42 · settled P&L **$+211.61** (includes unwinds: $-60.76)
- Paper rebalances (times Remick would have had to move money between venues): 9 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 58 fires, 55 traded, 10 with one leg short · simulated $154.44 vs $144.03 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 430 ms, fill check 64 ms

## Last 15 fires

| ts                        | key                  | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:---------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
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
| 2026-11-18T01:10:25+00:00 | barrios v roncadelli | True   | polyus_first |      187 |  0.9945 |       1.03 |        187 |        187 |         0    |         1.03 |          1.03 |
| 2026-11-18T01:11:41+00:00 | aboian v kolar       | True   | polyus_first |       54 |  0.9754 |       1.33 |         54 |         54 |         0    |         1.33 |          1.33 |
| 2026-11-18T01:14:09+00:00 | aboian v kolar       | True   | polyus_first |      191 |  0.9936 |       1.23 |        191 |        191 |         0    |         1.23 |          1.23 |
