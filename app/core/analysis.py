import yfinance as yf
import pandas as pd
import ta

from app.core.predictor import predict_breakout
from app.core.volume import detect_volume_spike
from app.core.institution import get_institutional_flow
from app.core.news import get_news_sentiment


def analyze_stock(stock):

    symbol = stock["symbol"]
    stock_id = symbol.replace(".TW", "")

    # =========================
    # 📥 下載資料
    # =========================
    df = yf.download(symbol, period="3mo", interval="1d")

    if df.empty:
        return None

    # =========================
    # 🔥 關鍵修正：確保一維資料
    # =========================
    close = df["Close"].squeeze()

    # =========================
    # 📊 技術指標
    # =========================
    df["ma20"] = close.rolling(20).mean()
    df["ma60"] = close.rolling(60).mean()

    df["rsi"] = ta.momentum.RSIIndicator(close).rsi()
    macd = ta.trend.MACD(close)
    df["macd"] = macd.macd()

    latest = df.iloc[-1]
    price = float(close.iloc[-1])

    # =========================
    # 🚀 主升段預測
    # =========================
    breakout_ready = predict_breakout(df)

    # =========================
    # 📈 爆量偵測
    # =========================
    volume_spike, vol_ratio = detect_volume_spike(df)

    # =========================
    # 🏦 法人資金
    # =========================
    inst_flow = get_institutional_flow(stock_id)

    # =========================
    # 📰 新聞情緒
    # =========================
    news = get_news_sentiment(stock_id)
    news_score = news["score"]

    # =========================
    # 🧠 評分系統（強化版）
    # =========================
    score = 0

    if breakout_ready:
        score += 30

    if volume_spike:
        score += 20

    if inst_flow > 0:
        score += 20

    if news_score > 0:
        score += 10

    # 🔥 技術加強
    if price > latest["ma20"]:
        score += 10

    if latest["rsi"] > 60:
        score += 10

    # =========================
    # 📊 型態判斷
    # =========================
    if breakout_ready and volume_spike:
        pattern = "🚀 起漲前夜"

    elif inst_flow < 0 and news_score < 0:
        pattern = "💣 主力出貨"

    else:
        pattern = "🌀 盤整"

    # =========================
    # 📈 動能（修正）
    # =========================
    momentum = float(close.iloc[-1] - close.iloc[-3])

    return {
        "symbol": symbol,
        "price": round(price, 2),
        "pattern": pattern,
        "score": score,
        "vol_ratio": round(float(vol_ratio), 2),
        "inst_flow": inst_flow,
        "news_score": news_score,
        "rsi": round(float(latest["rsi"]), 2),
        "macd": round(float(latest["macd"]), 2),
        "momentum": round(momentum, 2)
    }
