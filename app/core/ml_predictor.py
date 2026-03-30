from app.core.data_fetcher import fetch_stock_data
from app.core.indicators import calc_indicators

def predict(features):

    rsi, macd, ma_ratio = features

    long_score = 0.5
    short_score = 0.5

    if rsi > 55:
        long_score += 0.2
    if macd > 0:
        long_score += 0.2
    if ma_ratio > 1:
        long_score += 0.2

    if rsi < 45:
        short_score += 0.2
    if macd < 0:
        short_score += 0.2
    if ma_ratio < 1:
        short_score += 0.2

    return min(long_score, 1), min(short_score, 1)


# ===== 🔥 正確版本 =====
def predict_stock(symbol):

    df = fetch_stock_data(symbol)
    if df is None or len(df) < 50:
        return "❌ 資料不足"

    df = calc_indicators(df)

    row = df.iloc[-1]

    close = row["close"]
    ma20 = row["ma20"]
    rsi = row["rsi"]
    macd = row["macd"]

    ma_ratio = close / ma20 if ma20 else 1

    long_score, short_score = predict([rsi, macd, ma_ratio])

    result = f"📊 {symbol}\n\n"
    result += f"🟢 多：{round(long_score,2)}\n"
    result += f"🔴 空：{round(short_score,2)}\n"

    return result

