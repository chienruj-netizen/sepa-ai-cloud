import requests
import os

def get_news(symbol):

    api_key = os.getenv("NEWS_API_KEY")

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": symbol,
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": api_key
    }

    try:
        res = requests.get(url, params=params).json()
        articles = res.get("articles", [])
        news_list = [a["title"] for a in articles if "title" in a]
        return news_list

    except Exception as e:
        print("News error:", e)
        return []
