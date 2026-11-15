# Dry-run bot (Sun Nov 15 12:30PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$325.43**, Polymarket US **$6.16**; locked in 2 open matches: $390.32
- Bankroll now (cash + open at cost): **$721.91**
- Fires: 11 · settled: 8 · settled P&L **$+21.91** (includes unwinds: $+0.00)
- Paper rebalances (times Remick would have had to move money between venues): 2 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 11 fires, 10 traded, 0 with one leg short · simulated $54.59 vs $51.19 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 81 ms, fill check 54 ms

## Last 15 fires

| ts                        | key                       | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:--------------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-15T01:34:50+00:00 | fancutt v ibraimi         | True   | polyus_first |      178 |  0.9883 |       2.09 |        178 |        178 |            0 |         2.09 |          2.09 |
| 2026-11-15T02:27:19+00:00 | alopaeus v cretu          | False  | polyus_first |      150 |  0.9891 |       1.63 |        150 |        150 |            0 |         1.63 |          1.63 |
| 2026-11-15T02:48:59+00:00 | kumasaka v zhukov         | True   | polyus_first |      176 |  0.9662 |       5.94 |        176 |        176 |            0 |         5.94 |          5.94 |
| 2026-11-15T14:02:34+00:00 | latinovic v vandermeersch | True   | polyus_first |       83 |  0.9502 |       4.13 |         83 |         83 |            0 |         4.13 |          4.13 |
| 2026-11-15T18:02:05+00:00 | coulibaly v moroni        | True   | polyus_first |      211 |  0.9293 |      14.92 |        211 |        211 |            0 |        21.41 |         21.36 |
| 2026-11-15T18:07:47+00:00 | carou v jover             | True   | polyus_first |      154 |  0.9935 |       1    |        154 |        154 |            0 |         1    |          1    |
| 2026-11-15T18:13:05+00:00 | george v slavic           | True   | polyus_first |      126 |  0.9725 |       3.46 |        126 |        126 |            0 |         3.46 |          3.46 |
| 2026-11-15T18:26:32+00:00 | brostrom v orderlain      | True   | polyus_first |      169 |  0.9726 |       4.63 |          0 |          0 |            0 |         0    |         -3.35 |
| 2026-11-15T18:31:31+00:00 | brostrom v orderlain      | True   | polyus_first |      154 |  0.9828 |       2.65 |        154 |        154 |            0 |         2.65 |          2.65 |
| 2026-11-15T18:31:45+00:00 | brostrom v orderlain      | True   | polyus_first |      154 |  0.9934 |       1.01 |        154 |        154 |            0 |         1.01 |          1.01 |
| 2026-11-15T19:01:40+00:00 | coulibaly v moroni        | True   | polyus_first |      212 |  0.9468 |      11.27 |        212 |        212 |            0 |        11.27 |         11.27 |
