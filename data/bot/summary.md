# Dry-run bot (Sun Nov 15 2:00PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$257.03**, Polymarket US **$300.54**; locked in 1 open matches: $192.25
- Bankroll now (cash + open at cost): **$749.82**
- Fires: 14 · settled: 11 · settled P&L **$+56.16** (includes unwinds: $-6.34)
- Paper rebalances (times Remick would have had to move money between venues): 3 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 14 fires, 13 traded, 1 with one leg short · simulated $51.57 vs $48.17 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 84 ms, fill check 57 ms

## Last 15 fires

| ts                        | key                       | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:--------------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-15T01:34:50+00:00 | fancutt v ibraimi         | True   | polyus_first |      178 |  0.9883 |       2.09 |        178 |        178 |         0    |         2.09 |          2.09 |
| 2026-11-15T02:27:19+00:00 | alopaeus v cretu          | False  | polyus_first |      150 |  0.9891 |       1.63 |        150 |        150 |         0    |         1.63 |          1.63 |
| 2026-11-15T02:48:59+00:00 | kumasaka v zhukov         | True   | polyus_first |      176 |  0.9662 |       5.94 |        176 |        176 |         0    |         5.94 |          5.94 |
| 2026-11-15T14:02:34+00:00 | latinovic v vandermeersch | True   | polyus_first |       83 |  0.9502 |       4.13 |         83 |         83 |         0    |         4.13 |          4.13 |
| 2026-11-15T18:02:05+00:00 | coulibaly v moroni        | True   | polyus_first |      211 |  0.9293 |      14.92 |        211 |        211 |         0    |        21.41 |         21.36 |
| 2026-11-15T18:07:47+00:00 | carou v jover             | True   | polyus_first |      154 |  0.9935 |       1    |        154 |        154 |         0    |         1    |          1    |
| 2026-11-15T18:13:05+00:00 | george v slavic           | True   | polyus_first |      126 |  0.9725 |       3.46 |        126 |        126 |         0    |         3.46 |          3.46 |
| 2026-11-15T18:26:32+00:00 | brostrom v orderlain      | True   | polyus_first |      169 |  0.9726 |       4.63 |          0 |          0 |         0    |         0    |         -3.35 |
| 2026-11-15T18:31:31+00:00 | brostrom v orderlain      | True   | polyus_first |      154 |  0.9828 |       2.65 |        154 |        154 |         0    |         2.65 |          2.65 |
| 2026-11-15T18:31:45+00:00 | brostrom v orderlain      | True   | polyus_first |      154 |  0.9934 |       1.01 |        154 |        154 |         0    |         1.01 |          1.01 |
| 2026-11-15T19:01:40+00:00 | coulibaly v moroni        | True   | polyus_first |      212 |  0.9468 |      11.27 |        212 |        212 |         0    |        11.27 |         11.27 |
| 2026-11-15T20:09:59+00:00 | fils v shelton            | True   | polyus_first |      194 |  0.991  |       1.75 |        194 |        194 |         0    |         1.75 |          1.75 |
| 2026-11-15T20:10:28+00:00 | izquierdo v roncadelli    | True   | polyus_first |      175 |  0.991  |       1.57 |        175 |        175 |         0    |         1.57 |          1.57 |
| 2026-11-15T20:17:38+00:00 | andreeva v svitolina      | True   | polyus_first |      194 |  0.9943 |       1.1  |        194 |          0 |        -6.34 |        -6.34 |         -6.34 |
