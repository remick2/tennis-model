# Dry-run bot (Mon Nov 16 5:40PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$237.07**, Polymarket US **$309.61**; locked in 1 open matches: $213.54
- Bankroll now (cash + open at cost): **$760.22**
- Fires: 34 · settled: 24 · settled P&L **$+106.24** (includes unwinds: $-46.02)
- Paper rebalances (times Remick would have had to move money between venues): 5 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 34 fires, 32 traded, 7 with one leg short · simulated $64.68 vs $56.64 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 305 ms, fill check 58 ms

## Last 15 fires

| ts                        | key                    | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:-----------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
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
| 2026-11-16T22:01:40+00:00 | kennedy v krueger      | True   | polyus_first |      113 |  0.9683 |       3.58 |        113 |        113 |         0    |         3.58 |          3.58 |
| 2026-11-16T22:34:38+00:00 | strakhova v tikhonova  | True   | polyus_first |      101 |  0.9899 |       1.02 |        101 |          0 |        -3.88 |        -3.88 |         -3.88 |
| 2026-11-16T23:32:40+00:00 | strakhova v tikhonova  | True   | polyus_first |      127 |  0.9861 |       1.76 |        127 |          0 |        -3.59 |        -3.59 |         -3.59 |
| 2026-11-16T23:36:40+00:00 | strakhova v tikhonova  | True   | polyus_first |      222 |  0.9775 |       4.99 |          0 |        222 |        -9.21 |        -9.21 |         -9.21 |
| 2026-11-17T00:37:07+00:00 | chan v mmoh            | True   | polyus_first |      218 |  0.9795 |       4.46 |        218 |        218 |         0    |         4.46 |          4.46 |
