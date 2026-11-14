# Dry-run bot (Sat Nov 14 2:15PM MT)

Paper only: no keys, no real orders. Started 2026-11-11 with $690 ($345 per venue).

- Cash: Kalshi **$16.26**, Polymarket US **$16.26**; locked in 4 open matches: $663.38
- Bankroll now (cash + open at cost): **$695.90**
- Fires: 19 · settled: 2 · settled P&L **$+5.90** (includes unwinds: $+0.00)
- Paper rebalances (times Remick would have had to move money between venues): 3 · cap $150 per venue per arb
- Since the Polymarket-US-first switch: 19 fires, 6 traded, 0 with one leg short · simulated $31.52 vs $-87.87 if both orders had gone at once
- All fires: 23 · expected $168.32 · simulated $-12.68
- Median book-read time 61 ms, fill check 37 ms

## Last 15 fires

| ts                        | key             | live   | mode         |   shares |   total |   expected |   filled_a |   filled_b |   unwind_pnl |   sim_profit |   both_profit |
|:--------------------------|:----------------|:-------|:-------------|---------:|--------:|-----------:|-----------:|-----------:|-------------:|-------------:|--------------:|
| 2026-11-14T21:06:00+00:00 | chidekh v zheng | True   | polyus_first |      274 |  0.9235 |      20.97 |          0 |          0 |            0 |         0    |        -12.31 |
| 2026-11-14T21:06:28+00:00 | chidekh v zheng | True   | polyus_first |      274 |  0.954  |      12.6  |          0 |          0 |            0 |         0    |        -11.83 |
| 2026-11-14T21:06:54+00:00 | chidekh v zheng | True   | polyus_first |      274 |  0.954  |      12.6  |          0 |          0 |            0 |         0    |        -12.31 |
| 2026-11-14T21:07:20+00:00 | chidekh v zheng | True   | polyus_first |      301 |  0.9848 |       4.57 |        301 |        301 |            0 |         4.57 |          4.57 |
| 2026-11-14T21:07:22+00:00 | chidekh v zheng | True   | polyus_first |      301 |  0.9848 |       4.57 |          0 |          0 |            0 |         0    |        -13.5  |
| 2026-11-14T21:07:34+00:00 | chidekh v zheng | True   | polyus_first |      301 |  0.9848 |       4.57 |          0 |          0 |            0 |         0    |        -13.5  |
| 2026-11-14T21:08:02+00:00 | chidekh v zheng | True   | polyus_first |      301 |  0.9848 |       4.57 |          0 |          0 |            0 |         0    |        -13.52 |
| 2026-11-14T21:09:20+00:00 | chidekh v zheng | True   | polyus_first |      259 |  0.9635 |       9.46 |        259 |        259 |            0 |         9.46 |          9.46 |
| 2026-11-14T21:09:22+00:00 | chidekh v zheng | True   | polyus_first |       84 |  0.9636 |       3.06 |          0 |          0 |            0 |         0    |         -3.58 |
| 2026-11-14T21:09:54+00:00 | chidekh v zheng | True   | polyus_first |      126 |  0.9537 |       5.84 |          0 |          0 |            0 |         0    |         -5.65 |
| 2026-11-14T21:09:56+00:00 | chidekh v zheng | True   | polyus_first |      126 |  0.9537 |       5.84 |          0 |          0 |            0 |         0    |         -5.65 |
| 2026-11-14T21:10:56+00:00 | chidekh v zheng | True   | polyus_first |       76 |  0.9717 |       2.15 |         76 |         76 |            0 |         2.15 |          2.15 |
| 2026-11-14T21:10:58+00:00 | chidekh v zheng | True   | polyus_first |       59 |  0.9717 |       1.67 |          0 |          0 |            0 |         0    |         -2.38 |
| 2026-11-14T21:11:26+00:00 | chidekh v zheng | True   | polyus_first |       53 |  0.8219 |       9.44 |         53 |         53 |            0 |         9.44 |          9.44 |
| 2026-11-14T21:11:28+00:00 | chidekh v zheng | True   | polyus_first |       23 |  0.8222 |       4.09 |          0 |          0 |            0 |         0    |         -0.54 |
