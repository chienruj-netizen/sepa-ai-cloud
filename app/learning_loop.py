from app.pipeline import run_market_scan
from app.core.backtest_engine import run_backtest
from app.core.performance import analyze_performance
from app.core.ai_optimizer import save_best
from app.core.optimizer import optimize

def run_learning_cycle():

    print("🧠 Learning cycle start")

    # 1️⃣ 選股
    picks = run_market_scan()

    if not picks:
        return "⚠️ 無選股"

    symbol = picks[0]["symbol"]

    # 2️⃣ 回測
    df = run_backtest(symbol)

    # 3️⃣ 分析績效
    perf = analyze_performance(df)

    print("📊 回測結果:", perf)

    # 4️⃣ 優化
    best, score = optimize()

    # 5️⃣ 儲存最佳參數
    save_best(best)

    return {
        "symbol": symbol,
        "performance": perf,
        "best": best
    }
