from app.core.ml_predictor import predict_stock
from app.core.sepa_filter import apply_sepa_filter


def pick_candidates():

    symbols = [
        "2330.TW","2317.TW","2454.TW","2308.TW","2603.TW",
        "2382.TW","3037.TW","3711.TW","3034.TW","3443.TW"
    ]

    results = []

    for s in symbols:
        try:
            ai = predict_stock(s)
            sepa = apply_sepa_filter(s)

            if not ai:
                continue

            score = ai["prob"]

            # 🔥 融合邏輯（關鍵）
            if sepa["breakout"]:
                score += 0.1

            if sepa["reversal"]:
                score -= 0.1

            results.append({
                "symbol": s,
                "prob": score,
                "breakout": sepa["breakout"],
                "reversal": sepa["reversal"]
            })

        except Exception as e:
            print(f"⚠️ 選股錯誤 {s}: {e}")

    # 🔥 排序
    results = sorted(results, key=lambda x: x["prob"], reverse=True)

    return results[:2]   # 🔥 Top 2
