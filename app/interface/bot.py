import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from app.pipeline_v2 import run_pipeline
from app.core.market_regime import get_market_regime
from app.core.ai_optimizer import CONFIG
from app.core.ml_predictor import predict_stock

TOKEN = os.getenv("TELEGRAM_TOKEN")

main_keyboard = [
    ["📊 今日策略"],
    ["🔍 單股分析"],
    ["🌍 市場判斷"],
    ["⚙️ 系統狀態"]
]


# ======================
# 工具
# ======================

def calc_metrics(prob, tp, sl):

    ev = (prob * tp) - ((1 - prob) * abs(sl))

    if ev > 0.02:
        level = "🟢 低風險"
    elif ev > 0:
        level = "🟡 中風險"
    else:
        level = "🔴 高風險"

    return round(ev,4), level


# ======================
# 主選單
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    await update.message.reply_text("🤖 AI操盤系統已啟動", reply_markup=reply_markup)


# ======================
# 核心
# ======================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # 📊 今日策略
    if text == "📊 今日策略":

        await update.message.reply_text("🚀 AI分析中...")

        trades = run_pipeline()

        if not trades:
            await update.message.reply_text("⚠️ 今日無交易機會")
            return

        market = get_market_regime()
        msg = f"📊 今日策略（AI）\n\n🌍 市場：{market}\n\n"

        for t in trades:

            tp = CONFIG["tp"]
            sl = CONFIG["sl"]

            prob = t["prob"]
            price = t["price"]

            if t["side"] == "LONG":
                tp_price = price * (1 + tp)
                sl_price = price * (1 + sl)
                icon = "🟢"
            else:
                tp_price = price * (1 - tp)
                sl_price = price * (1 - sl)
                icon = "🔴"

            ev, level = calc_metrics(prob, tp, sl)

            msg += f"{icon} {t['symbol']}\n"
            msg += f"AI：{round(prob,2)}\n"
            msg += f"進場：{round(price,2)}\n"
            msg += f"TP：{round(tp_price,2)}\n"
            msg += f"SL：{round(sl_price,2)}\n"
            msg += f"EV：{ev}\n"
            msg += f"{level}\n\n"

        await update.message.reply_text(msg)

    # 🔍 單股分析
    elif text == "🔍 單股分析":
        await update.message.reply_text("請輸入股票代碼，例如：2330.TW")

    # 🔥 👉 新增：單股輸入判斷
    elif ".TW" in text:

        await update.message.reply_text("🔍 分析中...")

        result = predict_stock(text)

        if not result:
            await update.message.reply_text("⚠️ 無資料")
            return

        prob = float(result["prob"])
        price = float(result["price"])

        tp = CONFIG["tp"]
        sl = CONFIG["sl"]

        ev, level = calc_metrics(prob, tp, sl)

        msg = f"📊 單股分析\n\n{text}\n"
        msg += f"AI：{round(prob,2)}\n"
        msg += f"價格：{price}\n"
        msg += f"EV：{ev}\n"
        msg += f"{level}"

        await update.message.reply_text(msg)

    # 🌍 市場
    elif text == "🌍 市場判斷":
        market = get_market_regime()
        await update.message.reply_text(f"🌍 市場狀態：{market}")

    # ⚙️ 系統
    elif text == "⚙️ 系統狀態":

        msg = "⚙️ 系統參數\n\n"
        msg += f"TP：{CONFIG['tp']}\n"
        msg += f"SL：{CONFIG['sl']}\n"
        msg += f"門檻：{CONFIG['threshold']}\n"
        msg += f"選股數：{CONFIG['top_k']}"

        await update.message.reply_text(msg)

    else:
        await update.message.reply_text("⚠️ 請使用按鈕或輸入股票代碼")


# ======================
# 啟動
# ======================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
