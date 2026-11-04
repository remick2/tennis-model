# tennis-model

Tennis model + Phase 2 paper tracking. **No real bets until Phase 2 beats the close.**

## Phases
1. **Build** (done): surface Elo + point-level serve/return model, backtested against markets.
2. **Paper** (running since 2026-11-03): automated snapshots of Kalshi + Polymarket + Pinnacle, alerts, and a scorecard.
3. **Small real bets** with a hard bankroll cap ($700 total), only if the Phase 3 gate passes. Remick decides; nothing is ever bet automatically.

## Decisions (2026-11-03)
- **Alerts fire on price alone**: Kalshi/Polymarket all-in cost (ask + fee) at least 2c below Pinnacle's no-vig fair price. The model is shown as info only (it showed no edge over the market in any test). The scorecard still grades "price + model agree" separately.
- **Phase 3 gate**: 100+ graded price-flag sides whose average CLV (Pinnacle's last fair price before the start minus our cost) is positive by about 2 standard errors. ROI is reported but too noisy to be the gate.
- **Sizing (paper)**: quarter Kelly off Pinnacle fair, capped at 2% of $700 ($14). Fullstar: below its $10 minimum = no bet. Kalshi/Polymarket: any number of shares.
- **Schedule**: GitHub's cron dropped most scheduled runs on day 1 (1 of 8 ran), so once the repo is public each run loops hourly (:17) for ~5h40m and then starts the next run itself (`scripts/loop.sh`); minutes are free for public repos. While private, the hourly cron runs one cycle per run (`scripts/cycle.sh`).
- **Pinnacle credits**: 500/month free. `pinnacle_due()` spreads them over the month (every 2h, 4h or 8h depending on what's left).
- **Daily check-in**: a scheduled Claude session around 8pm MT checks runs, fixes breakages, and posts a short GitHub issue summary.
- **Fullstar withdrawals**: Mondays and Fridays only, 8am–6pm ET (6am–4pm MT). Money on Fullstar can take up to ~4 days to reach Kalshi, so the Phase 3 bankroll split has to be set ahead of time; it can't move to wherever an edge shows up that day.
- **Fullstar**: manual only. It needs Remick's logged-in browser. He says "check fullstar" when he's on, best in the evening when new lines post.
- **Tennis Tonic**: picks (winner + set count, no probabilities) load via JavaScript, so the automatic fetch is off. Instead Claude reads them from Remick's Chrome tab whenever it's in the tab group (with Fullstar checks or "log tonic"), surnames only, ITF excluded (not on Kalshi) → `data/tonic/picks.csv`. The scorecard grades pick win rate vs Kalshi's price; it only matters if it beats the market over a few hundred picks.

## Phase 1 results: the model does not beat the market
| Test | Sample | Result |
|---|---|---|
| Moneyline vs consensus close | ~9.6k main-tour matches 2025–26 | log loss 0.612/0.604 (model) vs 0.593/0.585 (close); no info beyond it |
| Challengers vs Kalshi pre-match | 3.3k matches Aug–Nov 2026 | model worse by 0.055–0.073; ROI −14% to −16% |
| Underdogs the model likes | 971 main tour + 1,184 Challenger | dogs win at the market's rate, not the model's; ROI −10% to −31% (`data/underdog_test.txt`) |
| Total games vs Kalshi | 840 matches, 2,116 lines | ATP Kalshi better, WTA tie; ROI within noise; "closer match → over" lost (`data/totals_backtest.txt`) |
| Game spreads vs Kalshi | 393 ATP matches, 990 lines | Kalshi better; dog +games −12%, fav −games −8% (`data/spread_backtest.txt`) |

Any edge has to come from **prices**: Kalshi/Polymarket gaps vs Pinnacle, Kalshi+Polymarket arbitrage, and slow Fullstar lines.

## What runs automatically (`.github/workflows/snapshot.yml`)
1. `kalshi_results.py`: Challenger results from Kalshi settlements (keeps ratings current)
2. `snapshot.py`: Kalshi + Polymarket + Pinnacle + model → `data/snapshots/`, arbitrage combos → `data/arbs/`
3. `notify.py`: new price flags and true arbs → GitHub issue (phone notification)
4. `scorecard.py`: CLV + results for flags and baseline, arbitrage near-misses → `data/scorecard.md`

## Side project: Polymarket copy-consensus tracker (`consensus/`, Nov 3–10 2026)
Paper tracking only, separate from the tennis model. `.github/workflows/consensus.yml` runs 4×/day (8:40am, 12:40pm, 4:40pm, 7:40pm MT). Each run pulls the open positions of 15 profitable Polymarket sports traders, logs games where 2+ hold $1k+ on the same side to `consensus/signals.csv`, grades finished ones, and rewrites `consensus/summary.md`. A **paper play** (3+ agree, nobody in the 15 against, game not started) opens a GitHub issue. The 2-agree version lost money in the Oct 27–Nov 3 backtest, so it's logged for comparison only. After Nov 10 it stops scanning, keeps grading, and opens one final-record issue.

## Manual tools
- `fullstar.py`: parse Fullstar page text, compare to Pinnacle/Kalshi, size paper bets → `data/fullstar_log.csv`
- Backtests: `backtest.py`, `challenger_backtest.py`, `totals_backtest.py`, `spread_backtest.py`

## Data (non-commercial personal use)
- Jeff Sackmann's ATP/WTA data via the [archival mirror](https://huggingface.co/datasets/Aneeshers/tennis-sackmann-archive) (through June 2026)
- [minmaxxxer odds dataset](https://huggingface.co/datasets/minmaxxxer/atp-wta-matches-with-odds): results + consensus open/close odds
- Live: The Odds API (Pinnacle), Kalshi and Polymarket public APIs

## Known gaps
- Pinnacle via the Odds API covers main-tour events only, so price flags are main tour only.
- Polymarket's international exchange is restricted for US users; Polymarket US prices may differ.
- Pinnacle is pulled every 2–4h, so the "close" can be a few hours before the start.
