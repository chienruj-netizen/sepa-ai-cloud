from app.core.selector import pick_candidates
from app.core.decision import make_decision
from app.core.backtest_engine import run_backtest
from app.core.performance import evaluate_performance
from app.core.ai_optimizer import optimize_model
from app.core.market_regime import get_market_regime


def run_pipeline():

    # 🔥 市場判斷
    market = get_market_regime()
    print(f"\n🌍 市場狀態: {market}")

    print("\n🚀 STEP 1: 選股")
    candidates = pick_candidates()
    print(f"📊 選出 {len(candidates)} 檔")

    print("\n🚀 STEP 2: 決策")
    decisions = []

    for c in candidates:
        d = make_decision(c, market, c["prob"])
        decisions.append(d)
        print(f"📌 {c['symbol']} → {d['action']} (score={c['prob']})")

    print("\n🚀 STEP 3: 回測")
    results = run_backtest(decisions)

    print("\n🚀 STEP 4: 評估")
    evaluate_performance(results)

    print("\n🚀 STEP 5: AI市場學習")
    optimize_model(results, market)

    print("\n🔥 Pipeline 完成")

    return decisions


if __name__ == "__main__":
    run_pipeline()
