import requests

def get_news_sentiment(symbol):

    try:
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={symbol}"
        data = requests.get(url, timeout=5).json()

        news = data.get("news", [])

        if not news:
            return 0, "中性"

        # 🔥 簡單情緒（標題）
        score = 0

        for n in news[:5]:
            title = n.get("title", "").lower()

            if "growth" in title or "profit" in title:
                score += 1
            elif "risk" in title or "loss" in title:
                score -= 1

        avg = score / max(len(news),1)

        if avg > 0:
            label = "偏多"
        elif avg < 0:
            label = "偏空"
        else:
            label = "中性"

        return round(avg,2), label

    except:
        return 0, "中性"
