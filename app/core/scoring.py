def score_signal(features):

    score = 50

    if features["pattern"] == "主升段":
        score += 20

    if features["pattern"] == "起跌點":
        score += 10

    # 之後這裡會接 RSI / 量能 / AI模型
    score += 5

    return min(score, 95)
