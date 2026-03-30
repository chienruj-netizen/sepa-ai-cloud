import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gpt_explain(features, decision, trend):

    try:
        prompt = f"""
你是一位專業股票分析師，請簡短分析：

價格: {features.get('price')}
RSI: {features.get('rsi')}
MACD: {features.get('macd')}
量比: {features.get('vol_ratio')}
動能: {features.get('momentum')}
趨勢: {trend}
決策: {decision.get('action')}

請用繁體中文，100字內分析：
"""

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return res.choices[0].message.content

    except Exception as e:
        return f"AI分析失敗: {e}"
