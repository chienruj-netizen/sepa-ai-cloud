def make_decision(candidate, trend="bull", prob=0.5):

    symbol = candidate.get("symbol")

    # 🔥 放寬條件（讓系統動起來）
    if prob >= 0.52:
        return {
            "symbol": symbol,
            "action": "BUY",
            "side": "LONG",
            "score": prob
        }

    elif prob <= 0.48:
        return {
            "symbol": symbol,
            "action": "SELL",
            "side": "SHORT",
            "score": prob
        }

    else:
        # 🔥 關鍵：給一個「偏向」
        return {
            "symbol": symbol,
            "action": "BUY",   # 強制交易
            "side": "LONG",
            "score": prob
        }
