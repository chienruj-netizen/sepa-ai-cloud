def detect_volume_spike(df):

    # 🔥 關鍵：轉一維
    volume = df["Volume"].squeeze()

    avg_vol = float(volume.rolling(20).mean().iloc[-1])
    latest_vol = float(volume.iloc[-1])

    # 避免除以0
    ratio = latest_vol / avg_vol if avg_vol > 0 else 0

    spike = ratio > 1.8

    return bool(spike), round(float(ratio), 2)
