def detect_trend(features):

    price = features["price"]
    ma20 = features["ma20"]
    ma60 = features["ma60"]
    rsi = features["rsi"]
    macd = features["macd"]

    # 🚀 主升段（起漲點）
    if price > ma20 > ma60 and macd > 0 and rsi < 70:
        return "🚀 主升段"

    # 💣 主跌段（起跌點）
    elif price < ma20 < ma60 and macd < 0 and rsi > 30:
        return "💣 主跌段"

    # 🌀 盤整
    return "🌀 盤整"
