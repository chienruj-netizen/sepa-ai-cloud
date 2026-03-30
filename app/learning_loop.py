import joblib
import os

from app.core.ml_trainer import train_models
from app.core.performance import evaluate_performance


MODEL_PATH = "data/model_v8.pkl"


def learning_loop(results):

    print("\n🧠 ===== Learning Loop =====")

    if not results:
        print("⚠️ 無交易資料，跳過學習")
        return

    ev = evaluate_performance(results)

    # 🔥 若策略有效 → 更新模型
    if ev > 0:
        print("📈 EV > 0 → 強化模型")

        model = train_models()

        joblib.dump(model, MODEL_PATH)

        print("✅ 新模型已儲存")

    else:
        print("⚠️ EV <= 0 → 保留舊模型")
