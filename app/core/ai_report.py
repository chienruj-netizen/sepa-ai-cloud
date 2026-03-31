import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze(symbol):

    prompt = f"""
    分析股票 {symbol}：
    1. 所屬產業
    2. 最近可能上漲原因
    3. 風險
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return res.choices[0].message.content
