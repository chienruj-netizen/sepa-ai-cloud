import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# =========================
# 📰 抓新聞
# =========================
def fetch_news(symbol: str):
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": symbol,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5,
            "apiKey": NEWS_API_KEY
        }

        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        articles = data.get("articles", [])
        return [a["title"] for a in articles if a.get("title")]

    except Exception as e:
        print("❌ fetch_news error:", e)
        return []


# =========================
# 🤖 情緒分析
# =========================
def get_news_sentiment(symbol: str):

    titles = fetch_news(symbol)

    if not titles:
        return {"score": 0, "label": "neutral"}

    text = " ".join(titles).lower()

    if "upgrade" in text or "growth" in text or "beat" in text:
        return {"score": 0.5, "label": "positive"}

    elif "downgrade" in text or "decline" in text or "miss" in text:
        return {"score": -0.5, "label": "negative"}

    else:
        return {"score": 0, "label": "neutral"}
