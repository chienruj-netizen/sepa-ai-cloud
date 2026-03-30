import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from app.main import run
from app.core.ml_predictor import predict_stock

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update, context):
    await update.message.reply_text("🤖 Bot 已啟動")


async def handle_message(update, context):
    try:
        text = update.message.text.strip()

        if text.endswith(".TW"):
            result = predict_stock(text)
        else:
            result = run()

        await update.message.reply_text(str(result))

    except Exception as e:
        print(f"❌ handler error: {e}")
        await update.message.reply_text("⚠️ 系統錯誤")


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 🔥 官方 webhook（關鍵）
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"https://sepa-ai-cloud113.onrender.com/webhook/{TOKEN}",
    )


if __name__ == "__main__":
    main()
