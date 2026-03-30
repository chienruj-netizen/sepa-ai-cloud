def make_decision(candidate, trend="bull", prob=0.5):

    symbol = candidate.get("symbol")

    # 🔥 做多
    if prob >= 0.7:
        return {
            "symbol": symbol,
            "action": "BUY",
            "side": "LONG",
            "score": prob
        }

    # 🔥 做空（關鍵）
    elif prob <= 0.3:
        return {
            "symbol": symbol,
            "action": "SELL",
            "side": "SHORT",
            "score": prob
        }

    # 🔥 不動
    else:
        return {
            "symbol": symbol,
            "action": "HOLD",
            "side": "NONE",
            "score": prob
        }
