import os
from openai import OpenAI
from app.core.data_fetcher import fetch_stock_data
from app.core.indicators import calc_indicators
from app.core.ml_predictor import predict

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze(symbol):

    df = fetch_stock_data(symbol)

    # 🔥 防 close 錯誤
    if df is None or "close" not in df.columns or len(df) < 50:
        return {
            "symbol": symbol,
            "price": 0,
            "prob": 0,
            "trend": "N/A",
            "reason": "資料不足或異常"
        }

    df = calc_indicators(df)

    row = df.iloc[-1]

    ma_ratio = row["close"] / row["ma20"] if row["ma20"] else 1

    vol_ma20 = df["volume"].rolling(20).mean().iloc[-1]
    vol_ratio = row["volume"] / vol_ma20 if vol_ma20 else 1

    momentum = df["close"].pct_change().iloc[-1]

    features = [
        row["rsi"],
        row["macd"],
        ma_ratio,
        vol_ratio,
        momentum
    ]

    prob = predict(features)

    try:
        prompt = f"分析股票 {symbol}，RSI={row['rsi']}，MACD={row['macd']}，量比={round(vol_ratio,2)}"

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )

        reason = res.choices[0].message.content

    except:
        reason = "AI分析失敗"

    return {
        "symbol": symbol,
        "price": row["close"],
        "prob": prob,
        "trend": "UP" if prob > 0.6 else "DOWN",
        "reason": reason
    }
