import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from app.pipeline_v2 import run_pipeline
from app.core.market_regime import get_market_regime
from app.core.ai_optimizer import CONFIG

TOKEN = os.getenv("TELEGRAM_TOKEN")

# 主選單
main_keyboard = [
    ["📊 今日策略"],
    ["🌍 市場判斷"],
    ["⚙️ 系統狀態"]
]

# ======================
# 工具函數（關鍵）
# ======================

def calc_metrics(prob, tp, sl):

    win_rate = prob

    reward = tp
    risk = abs(sl)

    ev = (win_rate * reward) - ((1 - win_rate) * risk)

    # 🔥 風險等級
    if ev > 0.02:
        level = "🟢 低風險"
    elif ev > 0:
        level = "🟡 中風險"
    else:
        level = "🔴 高風險"

    return round(win_rate,2), round(ev,4), level


def format_trade(c):

    tp = CONFIG["tp"]
    sl = CONFIG["sl"]

    price = c.get("price", 0)
    prob = c.get("prob", 0)

    action = c.get("side", "HOLD")

    if action == "LONG":
        tp_price = price * (1 + tp)
        sl_price = price * (1 + sl)
        icon = "🟢"
    else:
        tp_price = price * (1 - tp)
        sl_price = price * (1 - sl)
        icon = "🔴"

    win_rate, ev, level = calc_metrics(prob, tp, sl)

    msg = f"{icon} {c['symbol']}\n"
    msg += f"AI：{round(prob,2)}\n"
    msg += f"進場：{round(price,2)}\n"
    msg += f"TP：{round(tp_price,2)}\n"
    msg += f"SL：{round(sl_price,2)}\n"
    msg += f"勝率：{win_rate}\n"
    msg += f"EV：{ev}\n"
    msg += f"{level}\n\n"

    return msg


# ======================
# 主選單
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    await update.message.reply_text("🤖 AI操盤系統已啟動", reply_markup=reply_markup)


# ======================
# 核心邏輯
# ======================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # 📊 今日策略（核心）
    if text == "📊 今日策略":

        await update.message.reply_text("🚀 AI分析中...")

        candidates = run_pipeline()

        if not candidates:
            await update.message.reply_text("⚠️ 今日無交易機會")
            return

        market = get_market_regime()

        msg = f"📊 今日策略（AI）\n\n🌍 市場：{market}\n\n"

        for c in candidates:
            msg += format_trade(c)

        await update.message.reply_text(msg)

    # 🌍 市場判斷
    elif text == "🌍 市場判斷":
        market = get_market_regime()
        await update.message.reply_text(f"🌍 市場狀態：{market}")

    # ⚙️ 系統狀態
    elif text == "⚙️ 系統狀態":
        msg = "⚙️ 系統參數\n\n"
        msg += f"TP：{CONFIG['tp']}\n"
        msg += f"SL：{CONFIG['sl']}\n"
        msg += f"門檻：{CONFIG['threshold']}\n"
        msg += f"選股數：{CONFIG['top_k']}\n"

        await update.message.reply_text(msg)

    else:
        await update.message.reply_text("⚠️ 請使用按鈕操作")


# ======================
# 主程式
# ======================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
