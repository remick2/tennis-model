# tennis-model

Tennis win-probability model + Phase 2 paper tracking. **No real bets until Phase 2 beats the close.**

## Phases
1. **Build** (done): surface Elo + point-level serve/return model, backtested vs consensus closing odds (2025–26).
2. **Paper** (running): snapshots every 2h of Kalshi + Polymarket (+ Pinnacle every 4h) next to the model, in `data/snapshots/`. Need 100+ logged matches beating the close before Phase 3.
3. **Small real bets** with a hard bankroll cap, only if Phase 2 holds up.

## Phase 1 results (2025-01 → 2026-11, ~9.6k ATP/WTA main-draw matches)
- Log loss, lower = better: model ATP 0.612 / WTA 0.604 vs market close 0.593 / 0.585. **Model loses to the close everywhere**, with no info beyond it.
- Line shopping vs consensus fair: price alone −6% to −14% ROI. Price + model agrees ≈ breakeven; price + model disagrees −10% to −22%. The model is a filter, not an edge.
- Point model: total-games and game-margin predictions beat a naive baseline modestly. No historical totals odds exist to test vs the market.
Full outputs: `data/backtest_elo_v1.txt`, `data/elo_variants.csv`, `data/points2_*_log.txt`.

## Layout
- `src/load.py`, `crosswalk.py`: data loading + player matching across sources
- `src/elo.py`: overall + surface Elo (margin-of-victory, slam weighting, layoff boost)
- `src/pointmodel.py`: serve/return skills → exact Markov game/set/match distributions (with day-to-day form noise)
- `src/backtest.py`, `experiments.py`, `evaluate_points*.py`: Phase 1 tests
- `src/ratings.py`: current ratings for pricing upcoming matches
- `src/snapshot.py`: Phase 2 cross-market snapshot (edge = all-in cost incl. fees vs Pinnacle no-vig and vs model; flag only if both ≥ 2¢)
- `.github/workflows/snapshot.yml`: runs the snapshot on a schedule and commits results

## Data (CC BY-NC-SA / CC BY, non-commercial personal use)
- Jeff Sackmann's ATP/WTA data via the [archival mirror](https://huggingface.co/datasets/Aneeshers/tennis-sackmann-archive) (through Roland Garros 2026)
- ["Min Maxxxer / Tennis Odds Actor"](https://huggingface.co/datasets/minmaxxxer/atp-wta-matches-with-odds): results + consensus open/close odds, weekly
- Live: The Odds API (Pinnacle), Kalshi and Polymarket public APIs

## Known gaps
- Challenger/ITF results stop June 2026 → ratings stale for rising players (e.g. Kouame). Fix in progress.
- No sharp reference for Challengers/WTA unless the Odds API covers the event.
- Polymarket's main exchange is restricted for US users; Polymarket US prices may differ.
- Fullstar not wired in yet (no API; via browser).

Run locally: `bash scripts/fetch_data.sh && cd src && python run_all.py` (backtest) or `python snapshot.py` (needs `ODDS_API_KEY`).
