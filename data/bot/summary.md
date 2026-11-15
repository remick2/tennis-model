# Dry-run bot (Sun Nov 15 11:15AM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$248.07**, Polymarket US **$0.59**; locked in 3 open matches: $465.13
- Bankroll now (cash + open at cost): **$713.79**
- Fires: 7 · settled: 4 · settled P&L **$+13.79** (includes unwinds: $+0.00)
- Paper rebalances (times Remick would have had to move money between venues): 2 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 7 fires, 7 traded, 0 with one leg short · simulated $39.66 vs $39.61 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 68 ms, fill check 44 ms

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
