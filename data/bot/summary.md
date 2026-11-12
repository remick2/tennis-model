# Dry-run bot (Wed Nov 11 9:41PM MT)

Paper only: no keys, no real orders. Started 2026-11-11 with $690 ($345 per venue).

- Cash: Kalshi **$693.74**, Polymarket US **$0.27**; locked in 0 open matches: $0.00
- Bankroll now (cash + open at cost): **$694.01**
- Fires: 1 · settled: 1 · settled P&L **$+4.01** (includes unwinds: $+0.00)
- Since the Polymarket-US-first switch: 1 fires, 1 traded, 0 with one leg short · simulated $4.01 vs $4.01 if both orders had gone at once
- All fires: 5 · expected $18.49 · simulated $-40.19
- Median book-read time 64 ms, fill check 62 ms

## Last 15 fires

| ts                        | key                 | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:--------------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-11T21:58:36+00:00 | bellucci v gueymard | True   | nan          |      457 |  0.9958 |       1.92 |          0 |        457 |       -15.73 |       -15.73 |        nan    |
| 2026-11-11T22:01:04+00:00 | bellucci v gueymard | True   | nan          |      442 |  0.9965 |       1.55 |        442 |          0 |       -16.76 |       -16.76 |        nan    |
| 2026-11-11T22:03:32+00:00 | bellucci v gueymard | True   | nan          |      431 |  0.9864 |       5.85 |        431 |          0 |       -16.87 |       -16.87 |        nan    |
| 2026-11-11T22:07:00+00:00 | muchova v svitolina | True   | nan          |      406 |  0.9873 |       5.16 |        406 |        406 |         0    |         5.16 |        nan    |
| 2026-11-11T22:24:03+00:00 | bellucci v gueymard | True   | polyus_first |      559 |  0.9928 |       4.01 |        559 |        559 |         0    |         4.01 |          4.01 |
