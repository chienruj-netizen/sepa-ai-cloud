def calculate_score(features, trend, news_score):

    score = 0.5

    # 技術面
    if features.get("vol_ratio", 1) > 1.2:
        score += 0.1

    if features.get("momentum", 0) > 0:
        score += 0.1

    if features.get("rsi", 50) > 60:
        score += 0.05

    # 趨勢
    if trend == "bull":
        score += 0.1
    elif trend == "bear":
        score -= 0.1

    # 新聞
    score += news_score * 0.2

    return max(0, min(1, score))
