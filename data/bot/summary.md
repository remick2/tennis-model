# Dry-run bot (Mon Nov 16 2:39PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$214.81**, Polymarket US **$558.52**; locked in 0 open matches: $0.00
- Bankroll now (cash + open at cost): **$773.33**
- Fires: 29 · settled: 23 · settled P&L **$+102.66** (includes unwinds: $-29.34)
- Paper rebalances (times Remick would have had to move money between venues): 4 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 29 fires, 27 traded, 4 with one leg short · simulated $73.32 vs $65.28 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 271 ms, fill check 54 ms

## Last 15 fires

| ts                        | key                    | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:-----------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-15T21:09:30+00:00 | fils v shelton         | True   | polyus_first |      201 |  0.981  |       3.82 |        201 |        201 |         0    |         3.82 |          3.82 |
| 2026-11-15T21:10:33+00:00 | gogineni v gurenko     | True   | polyus_first |      100 |  0.9855 |       1.45 |        100 |        100 |         0    |         1.45 |          1.45 |
| 2026-11-15T21:23:11+00:00 | fils v shelton         | True   | polyus_first |       99 |  0.9769 |       2.29 |         99 |         99 |         0    |         3.24 |          3.24 |
| 2026-11-15T22:05:17+00:00 | bakonyi v nefve        | True   | polyus_first |      100 |  0.9815 |       1.85 |        100 |        100 |         0    |         1.85 |          1.85 |
| 2026-11-15T22:06:08+00:00 | bakonyi v nefve        | True   | polyus_first |      259 |  0.9737 |       6.82 |        259 |        259 |         0    |         6.82 |          6.82 |
| 2026-11-15T22:13:30+00:00 | bakonyi v nefve        | True   | polyus_first |      175 |  0.9769 |       4.04 |        175 |        175 |         0    |         4.04 |          4.04 |
| 2026-11-15T22:14:14+00:00 | bakonyi v nefve        | True   | polyus_first |      122 |  0.943  |       6.96 |        122 |        122 |         0    |         6.96 |          6.96 |
| 2026-11-16T00:39:31+00:00 | bigun v colleu         | True   | polyus_first |      192 |  0.9645 |       6.81 |        192 |        192 |         0    |         6.81 |          6.81 |
| 2026-11-16T01:40:38+00:00 | bigun v colleu         | True   | polyus_first |      178 |  0.9672 |       5.83 |        178 |        178 |         0    |         5.83 |          5.83 |
| 2026-11-16T02:13:38+00:00 | jones v marterer       | True   | polyus_first |       50 |  0.9422 |       2.89 |         50 |         50 |         0    |         2.89 |          2.89 |
| 2026-11-16T17:28:52+00:00 | brancaccio v costoulas | True   | polyus_first |      176 |  0.9827 |       3.04 |          0 |        176 |        -5.14 |        -5.14 |         -5.14 |
| 2026-11-16T17:31:12+00:00 | brancaccio v costoulas | True   | polyus_first |      176 |  0.9841 |       2.79 |          0 |        176 |        -5.14 |        -5.14 |         -5.14 |
| 2026-11-16T20:27:28+00:00 | dominko v viiala       | True   | polyus_first |      179 |  0.9942 |       1.04 |        179 |        179 |         0    |         1.04 |          1.04 |
| 2026-11-16T21:08:03+00:00 | charlton v zamora      | True   | polyus_first |      191 |  0.9103 |      17.14 |          0 |          0 |         0    |         0    |         -4.64 |
| 2026-11-16T21:28:26+00:00 | strakhova v tikhonova  | True   | polyus_first |      289 |  0.9646 |      10.24 |        289 |          0 |       -12.72 |       -12.72 |        -12.72 |
