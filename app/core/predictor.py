import pandas as pd


def predict_breakout(df):

    # 🔥 強制轉一維（關鍵）
    close = df["Close"].squeeze()
    high = df["High"].squeeze()
    low = df["Low"].squeeze()
    volume = df["Volume"].squeeze()

    # 最近資料
    recent_close = close.tail(5)
    recent_high = high.tail(5)
    recent_low = low.tail(5)
    recent_volume = volume.tail(5)

    # =========================
    # 📊 價格壓縮（VCP概念）
    # =========================
    price_range = (recent_high.max() - recent_low.min()) / recent_close.mean()

    # =========================
    # 📉 均線糾結
    # =========================
    ma20 = close.rolling(20).mean().iloc[-1]
    ma60 = close.rolling(60).mean().iloc[-1]

    ma_diff = abs(ma20 - ma60) / ma60

    # =========================
    # 📈 成交量放大
    # =========================
    vol_trend = recent_volume.iloc[-1] > recent_volume.mean()

    # =========================
    # 🚀 突破條件
    # =========================
    if price_range < 0.05 and ma_diff < 0.03 and vol_trend:
        return True

    return False
