from flask import Flask, request
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder
import os

from app.interface.bot import register_handlers

TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)

# ===== 建立 event loop =====
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# ===== Application =====
application = ApplicationBuilder().token(TOKEN).build()

# 🔥 正確初始化流程（關鍵）
async def init():
    await application.initialize()
    register_handlers(application)
    await application.start()

loop.run_until_complete(init())


@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)

        # 🔥 正確 dispatch（這行才是關鍵）
        asyncio.run_coroutine_threadsafe(
            application.process_update(update),
            loop
        )

        return "ok"

    except Exception as e:
        print(f"❌ webhook error: {e}")
        return "ok", 200


@app.route("/")
def index():
    return "Bot is running 🚀"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
