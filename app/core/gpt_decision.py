import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gpt_decide(features, trend):

    prompt = f"""
你是一位專業量化交易員，請根據以下資料做出交易決策：

【市場資料】
價格: {features.get('price')}
RSI: {features.get('rsi')}
MACD: {features.get('macd')}
量比: {features.get('vol_ratio')}
動能: {features.get('momentum')}
趨勢: {trend}

【請輸出JSON】
{{
  "action": "做多 / 做空 / 觀察",
  "confidence": 0~1,
  "tp": 建議停利價格,
  "sl": 建議停損價格,
  "reason": "簡短原因"
}}

限制：
- 僅輸出JSON
- 不要多餘文字
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        text = res.choices[0].message.content

        import json
        return json.loads(text)

    except Exception as e:
        return {
            "action": "觀察",
            "confidence": 0,
            "tp": features.get("price"),
            "sl": features.get("price"),
            "reason": f"GPT錯誤: {e}"
        }
