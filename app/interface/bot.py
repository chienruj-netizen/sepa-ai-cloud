from telegram.ext import CommandHandler, MessageHandler, filters

from app.main import run
from app.core.ml_predictor import predict_stock

def register_handlers(app):

    async def start(update, context):
        print("✅ /start triggered")
        await update.message.reply_text("🤖 Bot 已啟動")

    async def handle_message(update, context):
        try:
            text = update.message.text.strip()
            print(f"📩 收到訊息: {text}")

            if text.endswith(".TW"):
                result = predict_stock(text)
            else:
                result = run()

            print(f"📤 回傳結果:\n{result}")

            await update.message.reply_text(result)

        except Exception as e:
            print(f"❌ handler error: {e}")
            await update.message.reply_text("⚠️ 系統錯誤")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

