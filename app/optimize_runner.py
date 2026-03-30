from app.core.optimizer import optimize
from app.core.ai_optimizer import save_best


def run():

    best, log = optimize()

    print("🔥 最佳參數：", best)

    save_best(best)

    print("✅ 已更新策略")
