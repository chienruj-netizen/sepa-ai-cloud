from app.core.selector import select_stocks
from app.core.trade_logger import log_trade
from app.core.performance_tracker import get_performance
from app.core.auto_trainer_v2 import retrain

def run():
    try:

        long_list, short_list = select_stocks()

        if not long_list and not short_list:
            return "⚠️ 無交易機會"

        result = "📊 今日策略（AI）\n\n"

        # ===== 多單 =====
        if long_list:
            result += "🟢 做多策略\n\n"
            for s in long_list:
                symbol = s["symbol"]
                price = s["price"]
                prob = s["long"]

                tp = round(price * 1.05, 2)
                sl = round(price * 0.97, 2)

                log_trade(symbol, price, tp, sl, prob)

                result += f"{symbol}\n"
                result += f"AI：{prob:.2f}\n"
                result += f"進場：{price}\n"
                result += f"TP：{tp}\n"
                result += f"SL：{sl}\n\n"

        # ===== 空單 =====
        if short_list:
            result += "🔴 做空策略\n\n"
            for s in short_list:
                symbol = s["symbol"]
                price = s["price"]
                prob = s["short"]

                tp = round(price * 0.95, 2)
                sl = round(price * 1.03, 2)

                log_trade(symbol, price, tp, sl, prob)

                result += f"{symbol}\n"
                result += f"AI：{prob:.2f}\n"
                result += f"進場：{price}\n"
                result += f"TP：{tp}\n"
                result += f"SL：{sl}\n\n"

        perf = get_performance()

        if perf:
            result += "📈 系統績效\n"
            result += f"交易數：{perf['trades']}\n"
            result += f"勝率：{perf['win_rate']}\n"
            result += f"平均報酬：{perf['avg_return']}\n\n"

        retrain()

        return result

    except Exception as e:
        return f"❌ 系統錯誤: {e}"
