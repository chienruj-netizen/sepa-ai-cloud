from flask import Flask, request
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder
import os

from app.interface.bot import register_handlers

TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)

application = ApplicationBuilder().token(TOKEN).build()
register_handlers(application)

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)

        update = Update.de_json(data, application.bot)

        asyncio.run(application.process_update(update))

        return "ok"

    except Exception as e:
        print(f"❌ webhook error: {e}")
        return "error", 200   # ⚠️ 一定要回200


@app.route("/")
def index():
    return "Bot is running 🚀"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
