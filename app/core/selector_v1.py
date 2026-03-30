from app.core.ml_predictor import predict_stock

# 👉 先簡單股票池（之後可以擴大）
symbols = [
    "2330.TW","2317.TW","2454.TW","2308.TW","2603.TW",
    "2382.TW","3037.TW","3711.TW","3034.TW","3443.TW"
]

def pick_stocks():
    results = []

    for s in symbols:
        try:
            r = predict_stock(s)
            if r:
                results.append(r)
        except:
            pass

    # 🔥 排序（機率最高）
    results = sorted(results, key=lambda x: x["prob"], reverse=True)

    return results[:5]


if __name__ == "__main__":
    picks = pick_stocks()

    print("🚀 今日 AI 精選股：\n")
    for p in picks:
        print(p)
