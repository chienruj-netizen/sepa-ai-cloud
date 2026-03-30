import requests
import os
from openai import OpenAI

NEWS_API = os.getenv("NEWS_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_news_sentiment(keyword):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": keyword,
        "language": "zh",
        "pageSize": 5,
        "apiKey": NEWS_API
    }

    res = requests.get(url, params=params).json()

    articles = res.get("articles", [])

    if not articles:
        return "中性", 0

    text = " ".join([a["title"] for a in articles])

    # 🧠 AI判斷情緒
    prompt = f"""
    判斷以下新聞情緒（利多/利空/中性）並給0~100分：

    {text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content

        if "利多" in content:
            return "🟢 利多", 70
        elif "利空" in content:
            return "🔴 利空", 30
        else:
            return "⚪ 中性", 50

    except:
        return "⚪ 中性", 50
