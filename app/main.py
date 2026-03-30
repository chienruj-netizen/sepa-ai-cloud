from app.core.selector import select_stocks

def run():
    try:

        regime, long_list, short_list = select_stocks()

        result = f"📊 今日策略（AI）\n\n🌍 市場：{regime}\n\n"

        if long_list:
            result += "🟢 做多\n\n"
            for s in long_list:
                p = s["price"]
                result += f"{s['symbol']}\nAI：{s['long']}\n進場：{p}\nTP：{round(p*1.05,2)}\nSL：{round(p*0.97,2)}\n\n"

        if short_list:
            result += "🔴 做空\n\n"
            for s in short_list:
                p = s["price"]
                result += f"{s['symbol']}\nAI：{s['short']}\n進場：{p}\nTP：{round(p*0.95,2)}\nSL：{round(p*1.03,2)}\n\n"

        if not long_list and not short_list:
            result += "⚠️ 無明確機會"

        return result

    except Exception as e:
        return f"❌ 系統錯誤: {e}"
