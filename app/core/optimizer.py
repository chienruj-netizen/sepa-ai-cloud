from app.core.backtest_engine import run_backtest
from app.core.performance import analyze_performance


def optimize():

    best_score = -999
    best_params = None

    # 🔥 搜尋空間（你可以調整）
    thresholds = [0.5, 0.6, 0.7]
    vol_levels = [1.1, 1.2, 1.3]

    results_log = []

    for t in thresholds:
        for v in vol_levels:

            # 👉 暫時用 global（簡單版）
            config = {
                "threshold": t,
                "vol_ratio": v
            }

            df = run_backtest("2330.TW")

            perf = analyze_performance(df)

            score = perf["total_return"]

            results_log.append({
                "params": config,
                "performance": perf
            })

            if score > best_score:
                best_score = score
                best_params = config

    return best_params, results_log
