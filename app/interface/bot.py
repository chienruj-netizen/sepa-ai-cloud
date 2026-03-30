import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.main import run

TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 SEPA Cloud AI Engine 已啟動")


async def today_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = run()

    results = data["results"]

    # 💣 1️⃣ 排序（最強的在前）
    results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)

    # 💣 2️⃣ 過濾（只留高品質）
    results = [r for r in results if r.get("score", 0) >= 55]

    msg = f"🧠 SEPA Cloud AI Engine\n市場：{data['market']}\n策略：{data['strategy']}\n\n"

    if not results:
        msg += "⚠️ 今日無高勝率機會\n"
    else:
        for item in results:
            msg += (
                f"{item['symbol']}｜{item['signal']}｜"
                f"勝率:{item.get('score', 0)}%｜"
                f"新聞:{item.get('news_sentiment', 'N/A')}｜"
                f"TP:{item['tp']} SL:{item['sl']}\n"
            )

    await update.message.reply_text(msg)


def main():
    if not TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN 未設定")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("today", today_cmd))

    print("🚀 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
