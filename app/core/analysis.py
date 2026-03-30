import yfinance as yf
import pandas as pd
import ta

from app.core.data_fetcher import get_price
from app.core.news import get_news_score


def analyze_stock(stock):

    symbol = stock["symbol"]

    # === 即時價格 ===
    realtime = get_price(symbol)

    if realtime is None:
        return None

    price = realtime["price"]

    # === 技術資料 ===
    df = yf.download(symbol, period="3mo", interval="1d")

    if df.empty:
        return None

    df["ma20"] = df["Close"].rolling(20).mean()
    df["ma60"] = df["Close"].rolling(60).mean()

    df["rsi"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    macd = ta.trend.MACD(df["Close"])

    df["macd"] = macd.macd()

    latest = df.iloc[-1]

    ma20 = latest["ma20"]
    ma60 = latest["ma60"]
    rsi = latest["rsi"]
    macd_val = latest["macd"]

    # === 型態判斷 ===
    if price > ma20 > ma60 and macd_val > 0 and rsi > 55:
        pattern = "主升段🔥"
        trend_score = 30
    elif price < ma20 < ma60 and macd_val < 0:
        pattern = "主跌段💣"
        trend_score = 30
    else:
        pattern = "盤整"
        trend_score = 10

    # === 新聞 ===
    news_score = get_news_score(symbol)

    total_score = trend_score + news_score * 5

    return {
        "symbol": symbol,
        "price": price,
        "ma20": round(ma20, 2),
        "ma60": round(ma60, 2),
        "rsi": round(rsi, 2),
        "macd": round(macd_val, 2),
        "pattern": pattern,
        "score": total_score,
        "news": news_score
    }
