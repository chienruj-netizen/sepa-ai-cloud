from app.core.analysis import analyze_stock
from app.core.radar import detect_trend
from app.core.news import get_news_sentiment
from app.core.scoring import calculate_score
from app.core.decision import make_decision


def run():

    symbols = ["2330.TW", "2317.TW", "2454.TW"]

    results = []

    for symbol in symbols:

        features = analyze_stock({"symbol": symbol})

        if not features:
            continue

        trend = detect_trend(features)

        news_label, news_score = get_news_sentiment(symbol.split(".")[0])

        score = calculate_score(features, trend, news_score)

        decision = make_decision(features, trend, score)

        if decision["action"] != "⚪ 觀察":
            results.append({
                "symbol": symbol,
                "signal": decision["action"],
                "score": decision["score"],
                "tp": decision["tp"],
                "sl": decision["sl"],
                "trend": trend,
                "news": news_label
            })

    return {
        "market": "AI智能判斷",
        "strategy": "雷達 + 多因子 + 新聞",
        "results": sorted(results, key=lambda x: x["score"], reverse=True)
    }
