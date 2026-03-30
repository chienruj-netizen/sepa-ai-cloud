import random

def predict_score(features):

    score = 0

    # 🔥 簡化邏輯（先能跑）
    if features.get("volume_ratio", 1) > 1.2:
        score += 0.2

    if features.get("rsi", 50) > 60:
        score += 0.2

    if features.get("macd", 0) > 0:
        score += 0.2

    # 🔥 加隨機避免同分（未來改模型）
    score += random.uniform(0, 0.3)

    return round(score, 3)
