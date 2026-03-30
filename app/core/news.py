import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_news_sentiment(symbol: str):
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

    except:
        return []


def get_news_sentiment(symbol: str):

    titles = fetch_news(symbol)

    if not titles:
        return {"score": 0, "label": "neutral"}

    text = " ".join(titles)

    # 👉 簡化版（穩定優先）
    if "upgrade" in text.lower() or "growth" in text.lower():
        return {"score": 0.5, "label": "positive"}
    elif "downgrade" in text.lower() or "decline" in text.lower():
        return {"score": -0.5, "label": "negative"}
    else:
        return {"score": 0, "label": "neutral"}
