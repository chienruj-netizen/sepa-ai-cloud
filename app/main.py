from app.core.selector import pick_candidates
from app.core.analysis import analyze_stock
from app.core.decision import make_decision
from app.core.scoring import score_signal
from app.core.news import get_news
from app.core.news_ai import analyze_news

def run():

    stocks = pick_candidates()
    results = []

    for s in stocks:

        try:
            features = analyze_stock(s)
            if features is None:
                continue

            decision = make_decision(features)
            tech_score = score_signal(features)

            # 🔥 新聞分析
            news = get_news(s["symbol"])
            news_result = analyze_news(news)

            news_score = news_result["score"]

            # 💥 融合分數（超關鍵）
            final_score = int(tech_score * 0.7 + news_score * 0.3)

            results.append({
                "symbol": s.get("symbol"),
                "signal": decision.get("action"),
                "tp": decision.get("tp"),
                "sl": decision.get("sl"),
                "score": final_score,
                "news_sentiment": news_result["sentiment"]
            })

        except Exception as e:
            print(f"❌ Error: {e}")
            continue

    return {
        "market": "sideways",
        "strategy": "AI融合決策",
        "results": results
    }
