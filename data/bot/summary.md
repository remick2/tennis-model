# Dry-run bot (Sun Nov 15 4:56PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$339.88**, Polymarket US **$439.88**; locked in 0 open matches: $0.00
- Bankroll now (cash + open at cost): **$779.76**
- Fires: 21 · settled: 19 · settled P&L **$+86.09** (includes unwinds: $-6.34)
- Paper rebalances (times Remick would have had to move money between venues): 4 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 21 fires, 20 traded, 1 with one leg short · simulated $79.75 vs $76.35 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 142 ms, fill check 56 ms

## Last 15 fires

| ts                        | key                    | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:-----------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-15T18:13:05+00:00 | george v slavic        | True   | polyus_first |      126 |  0.9725 |       3.46 |        126 |        126 |         0    |         3.46 |          3.46 |
| 2026-11-15T18:26:32+00:00 | brostrom v orderlain   | True   | polyus_first |      169 |  0.9726 |       4.63 |          0 |          0 |         0    |         0    |         -3.35 |
| 2026-11-15T18:31:31+00:00 | brostrom v orderlain   | True   | polyus_first |      154 |  0.9828 |       2.65 |        154 |        154 |         0    |         2.65 |          2.65 |
| 2026-11-15T18:31:45+00:00 | brostrom v orderlain   | True   | polyus_first |      154 |  0.9934 |       1.01 |        154 |        154 |         0    |         1.01 |          1.01 |
| 2026-11-15T19:01:40+00:00 | coulibaly v moroni     | True   | polyus_first |      212 |  0.9468 |      11.27 |        212 |        212 |         0    |        11.27 |         11.27 |
| 2026-11-15T20:09:59+00:00 | fils v shelton         | True   | polyus_first |      194 |  0.991  |       1.75 |        194 |        194 |         0    |         1.75 |          1.75 |
| 2026-11-15T20:10:28+00:00 | izquierdo v roncadelli | True   | polyus_first |      175 |  0.991  |       1.57 |        175 |        175 |         0    |         1.57 |          1.57 |
| 2026-11-15T20:17:38+00:00 | andreeva v svitolina   | True   | polyus_first |      194 |  0.9943 |       1.1  |        194 |          0 |        -6.34 |        -6.34 |         -6.34 |
| 2026-11-15T21:09:30+00:00 | fils v shelton         | True   | polyus_first |      201 |  0.981  |       3.82 |        201 |        201 |         0    |         3.82 |          3.82 |
| 2026-11-15T21:10:33+00:00 | gogineni v gurenko     | True   | polyus_first |      100 |  0.9855 |       1.45 |        100 |        100 |         0    |         1.45 |          1.45 |
| 2026-11-15T21:23:11+00:00 | fils v shelton         | True   | polyus_first |       99 |  0.9769 |       2.29 |         99 |         99 |         0    |         3.24 |          3.24 |
| 2026-11-15T22:05:17+00:00 | bakonyi v nefve        | True   | polyus_first |      100 |  0.9815 |       1.85 |        100 |        100 |         0    |         1.85 |          1.85 |
| 2026-11-15T22:06:08+00:00 | bakonyi v nefve        | True   | polyus_first |      259 |  0.9737 |       6.82 |        259 |        259 |         0    |         6.82 |          6.82 |
| 2026-11-15T22:13:30+00:00 | bakonyi v nefve        | True   | polyus_first |      175 |  0.9769 |       4.04 |        175 |        175 |         0    |         4.04 |          4.04 |
| 2026-11-15T22:14:14+00:00 | bakonyi v nefve        | True   | polyus_first |      122 |  0.943  |       6.96 |        122 |        122 |         0    |         6.96 |          6.96 |
