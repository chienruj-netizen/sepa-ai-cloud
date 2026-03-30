import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app.core.selector import pick_candidates
from app.core.gpt_explainer import explain_trade

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 AI操盤系統已啟動")


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):

    picks = pick_candidates()

    msg = "📊 今日策略\n\n"

    for p in picks:
        explain = explain_trade(p)

        msg += f"{p['symbol']} ({p['side']})\n"
        msg += f"AI: {round(p['prob'],2)}\n"
        msg += f"{explain}\n\n"

    await update.message.reply_text(msg)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", today))

    app.run_polling()


if __name__ == "__main__":
    main()
