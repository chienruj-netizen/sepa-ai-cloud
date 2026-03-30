from flask import Flask, request
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)

# 建立 Telegram Application
application = ApplicationBuilder().token(TOKEN).build()

# ===== 🔥 接收 webhook =====
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    asyncio.run(application.process_update(update))
    return "ok"


# ===== 🔥 健康檢查 =====
@app.route("/")
def index():
    return "Bot is running 🚀"

