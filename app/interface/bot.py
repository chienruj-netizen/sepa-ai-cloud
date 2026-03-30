from telegram.ext import CommandHandler, MessageHandler, filters
from app.main import run
from app.core.ml_predictor import predict_stock

def register_handlers(app):

    async def start(update, context):
        await update.message.reply_text("🤖 Bot 已啟動")

    async def handle_message(update, context):
        text = update.message.text.strip()

        if text.endswith(".TW"):
            result = predict_stock(text)
        else:
            result = run()

        await update.message.reply_text(result)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

