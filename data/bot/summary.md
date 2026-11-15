# Dry-run bot (Sat Nov 14 7:28PM MT)

Paper only: no keys, no real orders. Started 2026-11-14 with $700 (Kalshi $345, Polymarket US $355).

- Cash: Kalshi **$185.90**, Polymarket US **$189.82**; locked in 2 open matches: $324.28
- Bankroll now (cash + open at cost): **$700.00**
- Fires: 2 · settled: 0 · settled P&L **$+0.00** (includes unwinds: $+0.00)
- Paper rebalances (times Remick would have had to move money between venues): 0 · cap $150 per venue per arb
- On fresh (uncached) Polymarket US books, since Nov 14: 2 fires, 2 traded, 0 with one leg short · simulated $3.72 vs $3.72 if both orders had gone at once
- Earlier fires (23) used Polymarket US books up to 30s stale: not evidence either way
- Median book-read time 62 ms, fill check 37 ms

## Last 15 fires

| ts                        | key               | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-15T01:34:50+00:00 | fancutt v ibraimi | True   | polyus_first |      178 |  0.9883 |       2.09 |        178 |        178 |            0 |         2.09 |          2.09 |
| 2026-11-15T02:27:19+00:00 | alopaeus v cretu  | False  | polyus_first |      150 |  0.9891 |       1.63 |        150 |        150 |            0 |         1.63 |          1.63 |
