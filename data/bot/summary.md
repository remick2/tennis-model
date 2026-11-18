# Dry-run bot (Tue Nov 17 9:47PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$452.63**, Polymarket US **$440.64**; locked in 0 open matches: $0.00
- Bankroll now (cash + open at cost): **$893.27**
- Fires: 65 · settled: 52 · settled P&L **$+254.02** (includes unwinds: $-60.76)
- Paper rebalances (times Remick would have had to move money between venues): 11 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 65 fires, 62 traded, 10 with one leg short · simulated $193.26 vs $182.85 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 380 ms, fill check 64 ms

## Last 15 fires

| ts                        | key                  | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:---------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-17T22:11:58+00:00 | papamichail v samson | True   | polyus_first |      182 |  0.9822 |       3.24 |        182 |          0 |        -4.97 |        -4.97 |         -4.97 |
| 2026-11-17T22:52:31+00:00 | aguilar v jover      | True   | polyus_first |      169 |  0.9819 |       3.06 |        169 |        169 |         0    |         3.07 |          3.07 |
| 2026-11-17T23:31:16+00:00 | garcia v gatica      | True   | polyus_first |       74 |  0.9826 |       1.29 |          0 |         74 |        -2.8  |        -2.8  |         -2.8  |
| 2026-11-18T00:18:24+00:00 | nicholas v zahraj    | True   | polyus_first |      239 |  0.9721 |       6.68 |        239 |        239 |         0    |         6.68 |          6.68 |
| 2026-11-18T00:32:47+00:00 | nicholas v zahraj    | True   | polyus_first |      170 |  0.9913 |       1.48 |        170 |        170 |         0    |         1.48 |          1.48 |
| 2026-11-18T01:10:25+00:00 | barrios v roncadelli | True   | polyus_first |      187 |  0.9945 |       1.03 |        187 |        187 |         0    |         1.03 |          1.03 |
| 2026-11-18T01:11:41+00:00 | aboian v kolar       | True   | polyus_first |       54 |  0.9754 |       1.33 |         54 |         54 |         0    |         1.33 |          1.33 |
| 2026-11-18T01:14:09+00:00 | aboian v kolar       | True   | polyus_first |      191 |  0.9936 |       1.23 |        191 |        191 |         0    |         1.23 |          1.23 |
| 2026-11-18T01:29:56+00:00 | labrana v rivera     | True   | polyus_first |      266 |  0.9687 |       8.33 |        266 |        266 |         0    |         8.34 |          8.34 |
| 2026-11-18T01:40:33+00:00 | aguiard v winter     | True   | polyus_first |       34 |  0.965  |       1.19 |         34 |         34 |         0    |         1.19 |          1.19 |
| 2026-11-18T02:16:36+00:00 | comesana v manuel    | True   | polyus_first |       80 |  0.9856 |       1.15 |         80 |         80 |         0    |         1.15 |          1.15 |
| 2026-11-18T02:17:54+00:00 | barton v galarneau   | True   | polyus_first |      274 |  0.9209 |      21.67 |        274 |        274 |         0    |        21.67 |         21.67 |
| 2026-11-18T03:08:02+00:00 | barton v galarneau   | True   | polyus_first |       78 |  0.9664 |       2.62 |         78 |         78 |         0    |         2.62 |          2.62 |
| 2026-11-18T03:19:53+00:00 | blancaneaux v viiala | True   | polyus_first |       79 |  0.9685 |       2.49 |         79 |         79 |         0    |         2.5  |          2.5  |
| 2026-11-18T03:36:55+00:00 | aboian v kolar       | True   | polyus_first |      128 |  0.9895 |       1.35 |        128 |        128 |         0    |         1.35 |          1.35 |
