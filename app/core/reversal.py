def detect_reversal(features):

    rsi = features.get("rsi", 50)
    macd = features.get("macd", 0)
    momentum = features.get("momentum", 0)

    # 🔥 崩跌條件
    if rsi < 40 and macd < 0 and momentum < 0:
        return True

    return False
