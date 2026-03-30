from app.pipeline import run_market_scan
import os

def run():

    results = run_market_scan()

    model_status = "✅ ML模型" if os.path.exists("data/model.pkl") else "⚠️ 未載入模型"

    return {
        "market": "AI模型預測",
        "strategy": f"LightGBM + 多因子 + 雷達 ({model_status})",
        "results": results
    }
