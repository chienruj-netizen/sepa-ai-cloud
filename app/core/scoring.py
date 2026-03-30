def calculate_score(features, trend, news_score):

    score = 0

    # 📈 趨勢加分
    if trend == "🚀 主升段":
        score += 30
    elif trend == "💣 主跌段":
        score += 25

    # ⚡ 動能
    if features["macd"] > 0:
        score += 15

    # RSI
    if 50 < features["rsi"] < 70:
        score += 15

    # 均線
    if features["price"] > features["ma20"]:
        score += 10

    # 📰 新聞
    score += int(news_score * 0.3)

    return min(score, 100)
