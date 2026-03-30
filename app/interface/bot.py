import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from app.main import run
from app.core.analysis import analyze_stock
from app.core.decision import make_decision

TOKEN = os.getenv("TELEGRAM_TOKEN")

# 👉 主選單
keyboard = [
    ["📊 今日 AI 選股"],
    ["🔍 單股分析"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# =====================
# 🚀 /start
# =====================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 SEPA Cloud AI Engine 已啟動\n請選擇功能👇",
        reply_markup=reply_markup
    )


# =====================
# 📊 今日選股（🔥升級版）
# =====================
async def today_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = run()

    results = data.get("results", [])

    # 🔥 排序（高分優先）
    results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)

    msg = f"🧠 AI市場分析\n市場：{data.get('market')}\n策略：{data.get('strategy')}\n\n"

    if not results:
        msg += "⚠️ 今日無機會（或資料不足）"
    else:
        for item in results:
            msg += (
                f"{item.get('symbol')}｜{item.get('signal')}\n"
                f"📊 分數:{item.get('score', 0)}\n"
                f"{item.get('trend', '🌀 未判斷')}｜{item.get('news', '⚪ 中性')}\n"
                f"🎯 TP:{item.get('tp')} SL:{item.get('sl')}\n\n"
            )

    await update.message.reply_text(msg)


# =====================
# 🔍 單股分析（按鈕）
# =====================
async def stock_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_stock"] = True

    await update.message.reply_text("請輸入股票代碼，例如：2330")


# =====================
# 🧠 單股分析（🔥即時版）
# =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if context.user_data.get("waiting_stock"):

        context.user_data["waiting_stock"] = False

        symbol = f"{text}.TW"

        try:
            features = analyze_stock({"symbol": symbol})

            if features is None:
                await update.message.reply_text("❌ 無法取得該股票資料")
                return

            decision = make_decision(features)

            msg = (
                f"📊 {symbol}\n\n"
                f"💰 現價：{features.get('price')}\n"
                f"📈 型態：{features.get('pattern')}\n"
                f"📊 MA20：{features.get('ma20')}｜MA60：{features.get('ma60')}\n"
                f"⚡ RSI：{features.get('rsi')}｜MACD：{features.get('macd')}\n\n"
                f"🧠 AI決策：{decision.get('action')}\n"
                f"🎯 TP：{decision.get('tp')}\n"
                f"🛑 SL：{decision.get('sl')}\n"
                f"📊 分數：{decision.get('score')}"
            )

        except Exception as e:
            msg = f"❌ 分析失敗：{e}"

        await update.message.reply_text(msg)
        return

    await update.message.reply_text("請使用選單操作👇")


# =====================
# 🧠 主程式
# =====================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("today", today_cmd))

    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("單股分析"), stock_prompt))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("今日 AI 選股"), today_cmd))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
