import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.main import run

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 SEPA Cloud AI Engine 已啟動")

async def today_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = run()

    msg = f"🧠 SEPA Cloud AI Engine\n市場：{data['market']}\n策略：{data['strategy']}\n\n"
    for item in data["results"]:
        msg += f"{item['symbol']}｜{item['signal']}｜TP:{item['tp']} SL:{item['sl']}\n"

    await update.message.reply_text(msg)

def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN 未設定")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("today", today_cmd))
    app.run_polling()

if __name__ == "__main__":
    main()
