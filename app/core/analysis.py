import yfinance as yf
import pandas as pd
import ta

from app.core.predictor import predict_breakout
from app.core.volume import detect_volume_spike
from app.core.institution import get_institutional_flow
from app.core.news import get_news_score


def analyze_stock(stock):

    symbol = stock["symbol"]
    stock_id = symbol.replace(".TW", "")

    df = yf.download(symbol, period="3mo", interval="1d")

    if df.empty:
        return None

    df["ma20"] = df["Close"].rolling(20).mean()
    df["ma60"] = df["Close"].rolling(60).mean()

    df["rsi"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    macd = ta.trend.MACD(df["Close"])
    df["macd"] = macd.macd()

    latest = df.iloc[-1]

    price = latest["Close"]

    # 🔥 主升段預測
    breakout_ready = predict_breakout(df)

    # 🔥 爆量
    volume_spike, vol_ratio = detect_volume_spike(df)

    # 🔥 法人
    inst_flow = get_institutional_flow(stock_id)

    # 🔥 新聞
    news_score = get_news_score(stock_id)

    # === 評分 ===
    score = 0

    if breakout_ready:
        score += 30

    if volume_spike:
        score += 20

    if inst_flow > 0:
        score += 20

    if news_score > 0:
        score += 10

    # === 型態 ===
    if breakout_ready and volume_spike:
        pattern = "🚀 起漲前夜"
    elif inst_flow < 0:
        pattern = "💣 主力出貨"
    else:
        pattern = "🌀 盤整"

    return {
        "symbol": symbol,
        "price": round(price, 2),
        "pattern": pattern,
        "score": score,
        "vol_ratio": vol_ratio,
        "inst_flow": inst_flow,
        "news": news_score
    }
