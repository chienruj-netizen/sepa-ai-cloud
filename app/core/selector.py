from app.core.ml_predictor import predict_stock

def pick_candidates():

    symbols = [
        "2330.TW","2317.TW","2454.TW","2308.TW","2603.TW",
        "2382.TW","3037.TW","3711.TW","3034.TW","3443.TW"
    ]

    results = []

    for s in symbols:
        try:
            r = predict_stock(s)
            if r:
                results.append(r)  # 🔥 保留完整資訊
        except:
            pass

    # 🔥 排序（最重要）
    results = sorted(results, key=lambda x: x["prob"], reverse=True)

    return results[:5]
