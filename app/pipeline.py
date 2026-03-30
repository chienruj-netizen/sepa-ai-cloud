from app.core.data_provider import get_data
from app.core.analysis import analyze_stock
from app.core.radar import detect_trend
from app.core.decision import make_decision
from app.core.gpt_explainer import gpt_explain
from app.core.selector import get_candidate_pool

# 🔥 改這裡：用 ML 模型
from app.core.ml_predictor import predict_return


# ========================
# 🔥 單股（AI + GPT）
# ========================
def run_pipeline(symbol, use_gpt=False):

    # 1️⃣ 單一資料來源（避免爆 API）
    base_data = get_data(symbol)

    features = analyze_stock({
        "symbol": symbol,
        "base": base_data
    })

    trend = detect_trend(features)

    # 🔥 真模型預測（未來報酬）
    try:
        score = predict_return(features)
    except:
        score = 0

    decision = make_decision(features, trend, score)

    gpt_text = None

    if use_gpt:
        try:
            gpt_text = gpt_explain(features, decision, trend)
        except Exception as e:
            gpt_text = f"⚠️ GPT錯誤：{e}"

    return {
        "symbol": symbol,
        "features": features,
        "trend": trend,
        "decision": decision,
        "score": score,
        "gpt": gpt_text
    }


# ========================
# 🔥 全市場掃描（核心）
# ========================
def run_market_scan():

    pool = get_candidate_pool()
    results = []

    for symbol in pool[:80]:  # 控制負載

        try:
            result = run_pipeline(symbol, use_gpt=False)

            # 🔥 過濾垃圾訊號
            if result["decision"]["action"] != "⚪ 觀察" and result["score"] > 0:

                results.append({
                    "symbol": symbol,
                    "score": round(result["score"], 4),
                    "trend": result["trend"],
                    "price": result["features"]["price"],
                    "action": result["decision"]["action"]
                })

        except Exception as e:
            print("SCAN ERROR:", e)
            continue

    return sorted(results, key=lambda x: x["score"], reverse=True)[:5]
