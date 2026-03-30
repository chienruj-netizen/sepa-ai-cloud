import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from app.main import run

TOKEN = os.getenv("TELEGRAM_TOKEN")

# =========================
# 📌 主選單
# =========================
keyboard = [
    ["📊 今日AI選股", "🔍 單股分析"],
    ["⚙️ 系統狀態"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# =========================
# 🚀 start
# =========================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 SEPA Cloud AI Engine 啟動\n\n請選擇功能👇",
        reply_markup=reply_markup
    )


# =========================
# 📊 今日選股
# =========================
async def today_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = run()

    results = data["results"]

    # 🔥 排序（高分優先）
    results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)

    # 🔥 過濾垃圾訊號
    results = [r for r in results if r.get("score", 0) >= 55]

    msg = f"🧠 AI市場分析\n市場：{data['market']}\n策略：{data['strategy']}\n\n"

    if not results:
        msg += "⚠️ 今日無高勝率機會\n"
    else:
        for item in results:
            msg += (
                f"{item['symbol']}｜{item['action']}\n"
                f"📈 勝率:{item['score']}%\n"
                f"📊 型態:{item['pattern']}\n"
                f"📰 新聞:{item['news']}\n"
                f"🎯 TP:{item['tp']}｜🛑 SL:{item['sl']}\n\n"
            )

    await update.message.reply_text(msg)


# =========================
# 🔍 單股分析（預留）
# =========================
async def single_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("請輸入股票代碼，例如：2330")


# =========================
# ⚙️ 系統狀態
# =========================
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "⚙️ 系統狀態\n"
        "✔ 雲端運行\n"
        "✔ AI決策\n"
        "✔ 即時資料（FinMind）\n"
        "✔ 新聞分析（OpenAI）\n"
    )
    await update.message.reply_text(msg)


# =========================
# 📌 按鍵處理（重點🔥）
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📊 今日AI選股":
        await today_cmd(update, context)

    elif text == "🔍 單股分析":
        await single_stock(update, context)

    elif text == "⚙️ 系統狀態":
        await status_cmd(update, context)

    else:
        await update.message.reply_text("請使用選單操作👇")


# =========================
# 🚀 主程式
# =========================
def main():

    if not TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN 未設定")

    app = Application.builder().token(TOKEN).build()

    # 指令
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("today", today_cmd))

    # 按鍵處理
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
