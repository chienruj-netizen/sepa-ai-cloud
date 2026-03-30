from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_news(news_list):

    text = "\n".join(news_list)

    prompt = f"""
    以下是近期股票新聞：

    {text}

    請輸出JSON格式：
    {{
        "sentiment": "bullish / bearish / neutral",
        "score": 0-100
    }}
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        result = res.choices[0].message.content
        return json.loads(result)
    except:
        return {"sentiment": "neutral", "score": 50}
