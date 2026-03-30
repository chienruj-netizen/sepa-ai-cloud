import pandas as pd

def predict_breakout(df):

    # 最近資料
    recent = df.tail(5)

    # 價格收斂（壓縮）
    price_range = (recent["High"].max() - recent["Low"].min()) / recent["Close"].mean()

    # 均線糾結
    ma20 = df["Close"].rolling(20).mean().iloc[-1]
    ma60 = df["Close"].rolling(60).mean().iloc[-1]

    ma_diff = abs(ma20 - ma60) / ma60

    # 成交量逐步增加
    vol_trend = recent["Volume"].iloc[-1] > recent["Volume"].mean()

    if price_range < 0.05 and ma_diff < 0.03 and vol_trend:
        return True

    return False
