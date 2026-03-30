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
    # 🔥 全部轉一維（核心）
    # =========================
    close = df["Close"].squeeze()
    volume = df["Volume"].squeeze()

    # =========================
    # 📊 技術指標
    # =========================
    ma20 = close.rolling(20).mean()
    ma60 = close.rolling(60).mean()

    rsi = ta.momentum.RSIIndicator(close).rsi()
    macd = ta.trend.MACD(close).macd()

    # =========================
    # 🔒 安全取值
    # =========================
    try:
        price = float(close.iloc[-1])
        ma20_val = float(ma20.iloc[-1])
        ma60_val = float(ma60.iloc[-1])
        rsi_val = float(rsi.iloc[-1])
        macd_val = float(macd.iloc[-1])
    except:
        return None

    # =========================
    # 🚀 主升段（強制 bool）
    # =========================
    try:
        breakout_ready = bool(predict_breakout(df))
    except:
        breakout_ready = False

    # =========================
    # 📈 爆量
    # =========================
    try:
        volume_spike, vol_ratio = detect_volume_spike(df)
        volume_spike = bool(volume_spike)
        vol_ratio = float(vol_ratio)
    except:
        volume_spike = False
        vol_ratio = 0.0

    # =========================
    # 🏦 法人（強制 float）
    # =========================
    try:
        inst_flow = float(get_institutional_flow(stock_id))
    except:
        inst_flow = 0.0

    # =========================
    # 📰 新聞（強制 float）
    # =========================
    try:
        news = get_news_sentiment(stock_id)
        news_score = float(news.get("score", 0))
    except:
        news_score = 0.0

    # =========================
    # 🧠 評分
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

    if price > ma20_val:
        score += 10

    if rsi_val > 60:
        score += 10

    # =========================
    # 📊 型態
    # =========================
    if breakout_ready and volume_spike:
        pattern = "🚀 起漲前夜"

    elif inst_flow < 0 and news_score < 0:
        pattern = "💣 主力出貨"

    else:
        pattern = "🌀 盤整"

    # =========================
    # 📈 動能
    # =========================
    try:
        momentum = float(close.iloc[-1] - close.iloc[-3])
    except:
        momentum = 0.0

    # =========================
    # 📦 回傳（完整）
    # =========================
    return {
        "symbol": symbol,
        "price": round(price, 2),
        "pattern": pattern,
        "score": score,
        "vol_ratio": round(vol_ratio, 2),
        "inst_flow": inst_flow,
        "news_score": news_score,
        "rsi": round(rsi_val, 2),
        "macd": round(macd_val, 2),
        "momentum": round(momentum, 2),

        # 🔥 關鍵：給 decision 用
        "ma20": round(ma20_val, 2),
        "ma60": round(ma60_val, 2)
    }
