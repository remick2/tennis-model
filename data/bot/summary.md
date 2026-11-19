# Dry-run bot (Wed Nov 18 5:30PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$236.61**, Polymarket US **$17.25**; locked in 3 open matches: $634.39
- Bankroll now (cash + open at cost): **$888.25**
- Fires: 71 · settled: 53 · settled P&L **$+255.95** (includes unwinds: $-67.71)
- Paper rebalances (times Remick would have had to move money between venues): 11 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 71 fires, 68 traded, 12 with one leg short · simulated $206.85 vs $196.44 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 376 ms, fill check 64 ms

## Last 15 fires

| ts                        | key                  | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:---------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-18T01:11:41+00:00 | aboian v kolar       | True   | polyus_first |       54 |  0.9754 |       1.33 |         54 |         54 |         0    |         1.33 |          1.33 |
| 2026-11-18T01:14:09+00:00 | aboian v kolar       | True   | polyus_first |      191 |  0.9936 |       1.23 |        191 |        191 |         0    |         1.23 |          1.23 |
| 2026-11-18T01:29:56+00:00 | labrana v rivera     | True   | polyus_first |      266 |  0.9687 |       8.33 |        266 |        266 |         0    |         8.34 |          8.34 |
| 2026-11-18T01:40:33+00:00 | aguiard v winter     | True   | polyus_first |       34 |  0.965  |       1.19 |         34 |         34 |         0    |         1.19 |          1.19 |
| 2026-11-18T02:16:36+00:00 | comesana v manuel    | True   | polyus_first |       80 |  0.9856 |       1.15 |         80 |         80 |         0    |         1.15 |          1.15 |
| 2026-11-18T02:17:54+00:00 | barton v galarneau   | True   | polyus_first |      274 |  0.9209 |      21.67 |        274 |        274 |         0    |        21.67 |         21.67 |
| 2026-11-18T03:08:02+00:00 | barton v galarneau   | True   | polyus_first |       78 |  0.9664 |       2.62 |         78 |         78 |         0    |         2.62 |          2.62 |
| 2026-11-18T03:19:53+00:00 | blancaneaux v viiala | True   | polyus_first |       79 |  0.9685 |       2.49 |         79 |         79 |         0    |         2.5  |          2.5  |
| 2026-11-18T03:36:55+00:00 | aboian v kolar       | True   | polyus_first |      128 |  0.9895 |       1.35 |        128 |        128 |         0    |         1.35 |          1.35 |
| 2026-11-18T14:22:28+00:00 | donald v taberner    | True   | polyus_first |      172 |  0.9353 |      11.13 |        172 |          0 |        -2.97 |        -2.97 |         -2.97 |
| 2026-11-18T20:22:28+00:00 | baris v tarvet       | True   | polyus_first |      172 |  0.9853 |       2.53 |          0 |        172 |        -3.98 |        -3.98 |         -3.98 |
| 2026-11-19T00:00:32+00:00 | kennedy v maxted     | True   | polyus_first |      123 |  0.9843 |       1.93 |        123 |        123 |         0    |         1.93 |          1.93 |
| 2026-11-19T00:17:08+00:00 | broska v langmo      | True   | polyus_first |      228 |  0.9399 |      13.71 |        228 |        228 |         0    |        13.71 |         13.71 |
| 2026-11-19T00:26:14+00:00 | geerlings v samson   | True   | polyus_first |      243 |  0.9928 |       1.74 |        243 |        243 |         0    |         1.74 |          1.74 |
| 2026-11-19T00:26:56+00:00 | geerlings v samson   | True   | polyus_first |      182 |  0.9827 |       3.15 |        182 |        182 |         0    |         3.16 |          3.16 |
