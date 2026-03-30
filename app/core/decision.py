def make_decision(features):

    price = features["price"]
    rsi = features["rsi"]
    macd = features["macd"]
    pattern = features["pattern"]

    # 可選（如果你有加）
    vol_ratio = features.get("vol_ratio", 1)
    news = features.get("news", "⚪ 中性")

    score = 50  # 基礎分

    # =====================
    # 📈 趨勢
    # =====================
    if pattern == "主升段":
        score += 20
    elif pattern == "空頭":
        score += 15

    # =====================
    # ⚡ 動能（MACD）
    # =====================
    if macd > 0:
        score += 10
    else:
        score -= 5

    # =====================
    # 📊 RSI
    # =====================
    if 50 < rsi < 70:
        score += 10
    elif rsi > 75:
        score -= 10  # 過熱
    elif rsi < 30:
        score += 5   # 可能反彈

    # =====================
    # 📦 量能
    # =====================
    if vol_ratio > 1.5:
        score += 10

    # =====================
    # 📰 新聞
    # =====================
    if "利多" in news:
        score += 10
    elif "利空" in news:
        score -= 10

    # 限制範圍
    score = max(0, min(score, 100))

    # =====================
    # 🎯 行動決策
    # =====================
    if pattern == "主升段" and score >= 70:
        action = "🟢 做多"
        tp = round(price * 1.06, 2)
        sl = round(price * 0.97, 2)

    elif pattern == "空頭" and score >= 65:
        action = "🔴 放空"
        tp = round(price * 0.94, 2)
        sl = round(price * 1.03, 2)

    else:
        action = "⚪ 觀察"
        tp = 0
        sl = 0

    return {
        "action": action,
        "tp": tp,
        "sl": sl,
        "score": score
    }
