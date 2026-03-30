from app.core.selector import pick_candidates
from app.core.decision import make_decision
from app.core.backtest_engine import run_backtest
from app.core.performance import evaluate_performance
from app.core.ai_optimizer import optimize_model


def run_pipeline():

    print("🚀 STEP 1: 選股")
    candidates = pick_candidates()

    if not candidates:
        print("⚠️ 無選股")
        return

    print(f"📊 選出 {len(candidates)} 檔")

    print("\n🚀 STEP 2: 決策")
    decisions = []
    for c in candidates:
        d = make_decision(c["symbol"], score=c["prob"])
        decisions.append(d)

    print("\n🚀 STEP 3: 回測")
    results = run_backtest(decisions)

    print("\n🚀 STEP 4: 評估")
    score = evaluate_performance(results)

    print(f"📈 績效評分: {score}")

    print("\n🚀 STEP 5: AI優化")
    optimize_model(results)

    print("\n🔥 Pipeline 完成")


if __name__ == "__main__":
    run_pipeline()
