import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def explain_trade(data):

    prompt = f"""
股票：{data['symbol']}
方向：{data['side']}
AI分數：{data['prob']}

請用交易員角度說明：
1. 為何進場
2. 風險在哪
3. 建議策略
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )
        return res.choices[0].message.content
    except:
        return "AI解釋失敗"
