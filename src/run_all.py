"""Full rebuild: ratings -> predictions -> backtest.  python run_all.py"""
import elo, backtest
DATA = backtest.DATA
for tour in ("atp", "wta"):
    stream, odds = elo.build_stream(tour)
    preds, _, _ = elo.run(stream)
    preds.to_parquet(f"{DATA}/preds_{tour}.parquet")
    odds.to_parquet(f"{DATA}/odds_{tour}.parquet")
backtest.main()
