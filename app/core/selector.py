from app.core.data_fetcher import fetch_stock_data
from app.core.indicators import calc_indicators
from app.core.ml_predictor import predict
from app.core.market_regime import get_market_regime

SYMBOLS = ["2330.TW","2317.TW","1308.TW","2603.TW","2409.TW","1582.TW","1528.TW"]

def select_stocks():

    regime = get_market_regime()

    long_list = []
    short_list = []

    for symbol in SYMBOLS:

        df = fetch_stock_data(symbol)
        if df is None or len(df) < 50:
            continue

        df = calc_indicators(df)

        row = df.iloc[-1]

        close = row["close"]
        ma20 = row["ma20"]
        rsi = row["rsi"]
        macd = row["macd"]

        ma_ratio = close / ma20 if ma20 else 1

        long_score, short_score = predict([rsi, macd, ma_ratio])

        data = {
            "symbol": symbol,
            "price": round(close,2),
            "long": round(long_score,2),
            "short": round(short_score,2)
        }

        # ===== 策略切換 =====

        if regime == "bull":
            if long_score > 0.7:
                long_list.append(data)

        elif regime == "bear":
            if short_score > 0.7:
                short_list.append(data)

        else:  # sideways
            if long_score > 0.75:
                long_list.append(data)
            if short_score > 0.75:
                short_list.append(data)

    long_list = sorted(long_list, key=lambda x: x["long"], reverse=True)
    short_list = sorted(short_list, key=lambda x: x["short"], reverse=True)

    return regime, long_list[:3], short_list[:3]

# ===== 🔥 相容舊系統（重要） =====
def pick_candidates():
    regime, long_list, short_list = select_stocks()

    result = []

    for s in long_list:
        result.append({
            "symbol": s["symbol"],
            "score": s["long"],
            "entry": s["price"],
            "tp": round(s["price"] * 1.05, 2),
            "sl": round(s["price"] * 0.97, 2)
        })

    for s in short_list:
        result.append({
            "symbol": s["symbol"],
            "score": s["short"],
            "entry": s["price"],
            "tp": round(s["price"] * 0.95, 2),
            "sl": round(s["price"] * 1.03, 2)
        })

    return result

