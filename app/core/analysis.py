import pandas as pd
import ta
from app.core.data_fetcher import get_stock_data


def analyze_stock(stock):

    symbol = stock["symbol"]

    df = get_stock_data(symbol)

    if df is None or len(df) < 50:
        return None

    # === 技術指標 ===
    df["ma20"] = df["close"].rolling(20).mean()
    df["ma60"] = df["close"].rolling(60).mean()

    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()

    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd_diff()

    latest = df.iloc[-1]

    price = latest["close"]

    # === 判斷型態 ===
    if price > latest["ma20"] > latest["ma60"]:
        pattern = "主升段"
    elif price < latest["ma20"] < latest["ma60"]:
        pattern = "空頭"
    else:
        pattern = "盤整"

    return {
        "symbol": symbol,
        "price": round(price, 2),
        "ma20": round(latest["ma20"], 2),
        "ma60": round(latest["ma60"], 2),
        "rsi": round(latest["rsi"], 2),
        "macd": round(latest["macd"], 2),
        "pattern": pattern
    }
