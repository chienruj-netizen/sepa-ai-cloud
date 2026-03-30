import pandas as pd
import numpy as np
import requests
import os
import ta
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =========================
# 📰 取得新聞
# =========================
def get_news(stock_id):

    api_key = os.getenv("NEWS_API_KEY")

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": stock_id,
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": api_key
    }

    try:
        res = requests.get(url, params=params).json()
        articles = res.get("articles", [])
        texts = [a["title"] for a in articles if "title" in a]
        return texts
    except:
        return []


# =========================
# 🤖 新聞情緒分析
# =========================
def analyze_news(news_list):

    if not news_list:
        return "neutral"

    text = "\n".join(news_list)

    prompt = f"""
請判斷以下新聞對股票影響（只回傳 bullish / bearish / neutral）：

{text}
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return res.choices[0].message.content.strip().lower()
    except:
        return "neutral"


# =========================
# 📊 主分析
# =========================
def analyze_stock(stock):

    df = stock["df"]
    price = stock["price"]
    symbol = stock["symbol"].replace(".TW", "")

    if df is None or df.empty or price is None:
        return None

    # ===== 技術指標 =====
    df["ma5"] = df["close"].rolling(5).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["vol_ma20"] = df["Trading_Volume"].rolling(20).mean()

    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd_diff()

    # ===== 最新資料 =====
    prev_high = df["close"].rolling(20).max().iloc[-2]
    prev_low = df["close"].rolling(20).min().iloc[-2]

    vol_ratio = df["Trading_Volume"].iloc[-1] / df["vol_ma20"].iloc[-1]

    ma5 = df["ma5"].iloc[-1]
    ma20 = df["ma20"].iloc[-1]
    rsi = df["rsi"].iloc[-1]
    macd_val = df["macd"].iloc[-1]

    # ===== 判斷條件 =====
    breakout = price > prev_high
    breakdown = price < prev_low

    trend_up = ma5 > ma20
    trend_down = ma5 < ma20

    volume_boost = vol_ratio > 1.5

    # =========================
    # 🧠 型態判斷
    # =========================
    if breakout and volume_boost and trend_up:
        pattern = "主升段🔥"
        action = "🟢 做多"

    elif breakdown and volume_boost and trend_down:
        pattern = "起跌點💣"
        action = "🔴 放空"

    else:
        pattern = "盤整🌀"
        action = "⚪ 觀察"

    # =========================
    # 📰 新聞分析
    # =========================
    news = get_news(symbol)
    news_sentiment = analyze_news(news)

    # =========================
    # 🤖 AI 評分（0~100）
    # =========================
    score = 50

    if breakout:
        score += 15
    if volume_boost:
        score += 10
    if trend_up:
        score += 10
    if rsi > 60:
        score += 5
    if macd_val > 0:
        score += 5

    if news_sentiment == "bullish":
        score += 10
    elif news_sentiment == "bearish":
        score -= 10

    score = max(0, min(100, score))

    # =========================
    # 🎯 TP / SL
    # =========================
    tp = round(price * 1.05, 2)
    sl = round(price * 0.97, 2)

    if action == "🔴 放空":
        tp = round(price * 0.95, 2)
        sl = round(price * 1.03, 2)

    return {
        "symbol": stock["symbol"],
        "pattern": pattern,
        "action": action,
        "score": score,
        "tp": tp,
        "sl": sl,
        "news": news_sentiment,
        "vol_ratio": round(vol_ratio, 2),
        "rsi": round(rsi, 1)
    }
