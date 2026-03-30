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
    # 📥 抓資料
    # =========================
    df = yf.download(symbol, period="3mo", interval="1d")

    if df.empty:
        return None

    close = df["Close"].squeeze()
    volume = df["Volume"].squeeze()

    # =========================
    # 📊 技術指標
    # =========================
    ma20 = close.rolling(20).mean()
    ma60 = close.rolling(60).mean()

    rsi = ta.momentum.RSIIndicator(close).rsi()
    macd = ta.trend.MACD(close).macd()

    try:
        price = float(close.iloc[-1])
        ma20_val = float(ma20.iloc[-1])
        ma60_val = float(ma60.iloc[-1])
        rsi_val = float(rsi.iloc[-1])
        macd_val = float(macd.iloc[-1])
    except:
        return None

    # =========================
    # 🚀 breakout
    # =========================
    try:
        breakout_ready = bool(predict_breakout(df))
    except:
        breakout_ready = False

    # =========================
    # 📈 volume
    # =========================
    try:
        volume_spike, vol_ratio = detect_volume_spike(df)
        vol_ratio = float(vol_ratio)
    except:
        vol_ratio = 1.0

    # =========================
    # 🏦 法人
    # =========================
    try:
        inst_flow = float(get_institutional_flow(stock_id))
    except:
        inst_flow = 0.0

    # =========================
    # 📰 新聞
    # =========================
    try:
        news = get_news_sentiment(stock_id)
        news_score = float(news.get("score", 0))
    except:
        news_score = 0.0

    # =========================
    # 📈 動能
    # =========================
    try:
        momentum = float(close.iloc[-1] - close.iloc[-3])
    except:
        momentum = 0.0

    # =========================
    # 🔥 V7：波動率（重要）
    # =========================
    volatility = abs(rsi_val - 50)

    # =========================
    # 📊 型態（保留）
    # =========================
    if breakout_ready and vol_ratio > 1.5:
        pattern = "🚀 起漲"
    elif inst_flow < 0 and news_score < 0:
        pattern = "💣 出貨"
    else:
        pattern = "🌀 盤整"

    # =========================
    # 📦 回傳（🔥完全對齊模型）
    # =========================
    return {
        "symbol": symbol,
        "price": round(price, 2),
        "pattern": pattern,

        # 🔥 ML核心特徵
        "rsi": round(rsi_val, 2),
        "macd": round(macd_val, 2),
        "volume_ratio": round(vol_ratio, 2),
        "ma20": round(ma20_val, 2),

        # 🔥 V7新增
        "volatility": round(volatility, 2),
        "institution": inst_flow,
        "news_score": news_score,

        # 其他
        "momentum": round(momentum, 2)
    }
