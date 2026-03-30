def detect_volume_spike(df):

    avg_vol = df["Volume"].rolling(20).mean().iloc[-1]
    latest_vol = df["Volume"].iloc[-1]

    ratio = latest_vol / avg_vol if avg_vol > 0 else 0

    if ratio > 1.8:
        return True, round(ratio, 2)

    return False, round(ratio, 2)
