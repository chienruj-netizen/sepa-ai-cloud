import requests
import os

NEWS_API = os.getenv("NEWS_API_KEY")


def get_news_score(keyword):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": keyword,
        "language": "zh",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API
    }

    res = requests.get(url, params=params)
    data = res.json()

    if "articles" not in data:
        return 0

    score = 0

    for a in data["articles"][:5]:
        title = a["title"]

        if "漲" in title or "利多" in title:
            score += 1
        elif "跌" in title or "利空" in title:
            score -= 1

    return score
