from flask import Flask, request
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder
import os

from app.interface.bot import register_handlers

TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)

# ===== 建立 loop =====
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# ===== 建立 application =====
application = ApplicationBuilder().token(TOKEN).build()

# 🔥 關鍵：先 initialize 再 register
loop.run_until_complete(application.initialize())

# 🔥 再綁 handler
register_handlers(application)


@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)

        update = Update.de_json(data, application.bot)

        # 🔥 用 create_task（更穩）
        loop.create_task(application.process_update(update))

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
