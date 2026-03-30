from app.core.ml_predictor import predict_stock, build_features
from app.core.data_fetcher import fetch_stock_data

symbols = [
    "2330.TW","2317.TW","2454.TW","2308.TW","2603.TW",
    "2382.TW","3037.TW","3711.TW","3034.TW","3443.TW"
]


def check_sepa(df):
    df["ma20"] = df["close"].rolling(20).mean()
    df["avg_vol"] = df["volume"].rolling(20).mean()

    latest = df.iloc[-1]

    cond1 = latest["close"] > latest["ma20"]
    cond2 = latest["volume"] > latest["avg_vol"]
    cond3 = latest["close"] >= df["close"].rolling(20).max().iloc[-2]

    return cond1 and cond2 and cond3


def pick_stocks():
    results = []

    for s in symbols:
        try:
            df = fetch_stock_data(s)
            if df is None or len(df) < 50:
                continue

            # 🔥 SEPA 過濾
            if not check_sepa(df):
                continue

            r = predict_stock(s)

            if r and r["prob"] >= 0.7:
                results.append(r)

        except:
            pass

    results = sorted(results, key=lambda x: x["prob"], reverse=True)

    return results


if __name__ == "__main__":
    picks = pick_stocks()

    print("🛡 穩健型 AI 精選股：\n")

    if not picks:
        print("⚠️ 今日無符合條件標的（這是好事）")

    for p in picks:
        print(p)
