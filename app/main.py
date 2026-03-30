import time
from app.core.selector import select_stocks

def run():
    try:
        print("🚀 RUN START")

        start = time.time()

        stocks = select_stocks()

        if not stocks:
            return "⚠️ 今日無符合條件股票"

        result = "📊 今日策略\n\n"

        for s in stocks[:5]:
            result += f"🚀 {s}\n"

        print(f"⏱ 完成時間: {time.time()-start:.2f}s")

        return result

    except Exception as e:
        print(f"❌ run error: {e}")
        return f"❌ 系統錯誤: {e}"
