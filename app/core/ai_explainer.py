def explain(features, decision, trend):

    score = features.get("score", 0)
    rsi = features.get("rsi", 50)
    macd = features.get("macd", 0)
    vol = features.get("vol_ratio", 1)
    momentum = features.get("momentum", 0)

    action = decision.get("action")

    text = "📖 AI解讀：\n\n"

    # =====================
    # 🎯 核心判斷
    # =====================
    if action == "🟢 做多":
        text += "👉 偏多訊號成立\n"

    elif action == "🔴 做空":
        text += "👉 偏空訊號成立\n"

    else:
        text += "👉 無明確方向\n"

    # =====================
    # 📊 技術分析
    # =====================
    text += "\n📊 技術面：\n"

    if rsi < 40:
        text += "- RSI偏弱（空方）\n"
    elif rsi > 60:
        text += "- RSI偏強（多方）\n"
    else:
        text += "- RSI中性\n"

    if macd > 0:
        text += "- MACD多頭\n"
    else:
        text += "- MACD空頭\n"

    if vol > 1.5:
        text += "- 有量能支持\n"
    else:
        text += "- 量能不足\n"

    # =====================
    # ⚡ 動能
    # =====================
    text += "\n⚡ 動能：\n"

    if momentum > 0:
        text += "- 上漲動能\n"
    else:
        text += "- 下跌動能\n"

    # =====================
    # 🌍 市場
    # =====================
    text += "\n🌍 市場狀態：\n"

    if trend == "bull":
        text += "- 多頭市場\n"
    elif trend == "bear":
        text += "- 空頭市場\n"
    else:
        text += "- 震盪市場\n"

    # =====================
    # ⚠️ 風險
    # =====================
    text += "\n⚠️ 風險提醒：\n"

    if score < 0.5:
        text += "- 勝率偏低\n"

    if vol < 1.2:
        text += "- 量能不足\n"

    return text
