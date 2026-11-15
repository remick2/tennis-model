# Dry-run bot (Sun Nov 15 5:04AM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$191.83**, Polymarket US **$367.83**; locked in 1 open matches: $148.37
- Bankroll now (cash + open at cost): **$708.03**
- Fires: 3 · settled: 2 · settled P&L **$+8.03** (includes unwinds: $+0.00)
- Paper rebalances (times Remick would have had to move money between venues): 1 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 3 fires, 3 traded, 0 with one leg short · simulated $9.66 vs $9.66 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 62 ms, fill check 37 ms

## Last 15 fires

| ts                        | key               | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-15T01:34:50+00:00 | fancutt v ibraimi | True   | polyus_first |      178 |  0.9883 |       2.09 |        178 |        178 |            0 |         2.09 |          2.09 |
| 2026-11-15T02:27:19+00:00 | alopaeus v cretu  | False  | polyus_first |      150 |  0.9891 |       1.63 |        150 |        150 |            0 |         1.63 |          1.63 |
| 2026-11-15T02:48:59+00:00 | kumasaka v zhukov | True   | polyus_first |      176 |  0.9662 |       5.94 |        176 |        176 |            0 |         5.94 |          5.94 |
