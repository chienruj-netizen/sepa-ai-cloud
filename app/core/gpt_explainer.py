import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def explain_trade(symbol, side, prob):

    prompt = f"""
股票：{symbol}
方向：{side}
AI信心：{prob}

請用專業交易員角度簡短說明：
1. 為什麼做這個方向
2. 目前風險
（50字內）
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )
        return res.choices[0].message.content.strip()
    except:
        return "AI解釋失敗"
