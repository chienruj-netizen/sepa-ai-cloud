def predict(features):

    rsi, macd, ma_ratio = features

    long_score = 0.5
    short_score = 0.5

    # 多頭條件
    if rsi > 55:
        long_score += 0.2
    if macd > 0:
        long_score += 0.2
    if ma_ratio > 1:
        long_score += 0.2

    # 空頭條件
    if rsi < 45:
        short_score += 0.2
    if macd < 0:
        short_score += 0.2
    if ma_ratio < 1:
        short_score += 0.2

    return min(long_score, 1), min(short_score, 1)
