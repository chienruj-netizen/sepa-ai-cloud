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

            # 🔥 關鍵：一定要起漲
            if not sepa["breakout"]:
                continue

            # 🔥 關鍵：不能是起跌
            if sepa["reversal"]:
                continue

            score = ai["prob"]

            results.append({
                "symbol": s,
                "prob": score,
                "breakout": True
            })

        except Exception as e:
            print(f"⚠️ 選股錯誤 {s}: {e}")

    results = sorted(results, key=lambda x: x["prob"], reverse=True)

    return results[:2]
