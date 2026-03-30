import pandas as pd
from app.core.data_fetcher import get_stock_data


def detect_breakout(symbol):

    df = get_stock_data(symbol)

    if df is None or len(df) < 60:
        return False

    try:
        close = df["close"] if "close" in df.columns else df["Close"]
        volume = df["volume"] if "volume" in df.columns else df["Volume"]

        ma20 = close.rolling(20).mean()
        max20 = close.rolling(20).max()

        # 🔥 條件 1：突破前高
        cond1 = close.iloc[-1] >= max20.iloc[-2]

        # 🔥 條件 2：站上均線
        cond2 = close.iloc[-1] > ma20.iloc[-1]

        # 🔥 條件 3：放量
        vol_ratio = volume.iloc[-1] / volume.rolling(20).mean().iloc[-1]
        cond3 = vol_ratio > 1.2

        return cond1 and cond2 and cond3

    except:
        return False
