from app.core.analysis import analyze_stock
from app.core.radar import detect_trend
from app.core.scoring import calculate_score
from app.core.decision import make_decision


def run():

    symbols = ["2330.TW", "2317.TW", "2454.TW"]

    results = []

    for symbol in symbols:

        # =========================
        # 📊 技術分析（已包含新聞）
        # =========================
        features = analyze_stock({"symbol": symbol})

        if not features:
            continue

        # =========================
        # 🌍 趨勢判斷
        # =========================
        trend = detect_trend(features)

        # =========================
        # 🧠 AI評分（直接用 features）
        # =========================
        score = calculate_score(
            features,
            trend,
            features["news_score"]
        )

        # =========================
        # 🤖 AI決策
        # =========================
        decision = make_decision(features, trend, score)

        # =========================
        # 🚨 過濾
        # =========================
        if decision["action"] != "⚪ 觀察":
            results.append({
                "symbol": symbol,
                "signal": decision["action"],
                "score": decision["score"],
                "tp": decision["tp"],
                "sl": decision["sl"],
                "trend": trend,
                "rr": decision["rr"],
                "mode": decision["mode"]
            })

        # Debug（保留）
        print(symbol, trend, score, decision)

    return {
        "market": "AI智能判斷",
        "strategy": "雷達 + 多因子 + 新聞 + 風控",
        "results": sorted(results, key=lambda x: x["score"], reverse=True)
    }
