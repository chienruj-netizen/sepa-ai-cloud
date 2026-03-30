import os
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from app.main import run
from app.core.ml_predictor import predict_stock

TOKEN = os.getenv("TELEGRAM_TOKEN")


# ===== 主選單 =====
def get_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["📊 今日策略", "🔍 單股分析"],
            ["🌍 市場判斷", "⚙️ 系統狀態"]
        ],
        resize_keyboard=True
    )


# ===== 指令 =====
async def start(update, context):
    await update.message.reply_text(
        "🤖 AI交易系統已啟動",
        reply_markup=get_keyboard()
    )


# ===== 處理訊息 =====
async def handle_message(update, context):
    try:
        text = update.message.text.strip()
        print(f"📩 收到訊息: {text}")

        # ===== 按鈕功能 =====
        if text == "📊 今日策略":
            result = run()

        elif text == "🌍 市場判斷":
            result = run()

        elif text == "⚙️ 系統狀態":
            result = "🟢 系統正常運作中"

        elif text == "🔍 單股分析":
            await update.message.reply_text("請輸入股票代碼，例如：2330.TW")
            return

        # ===== 股票查詢 =====
        elif text.endswith(".TW"):
            result = predict_stock(text)

        else:
            result = "請使用下方按鈕操作"

        result = str(result)

        print(f"📤 回傳結果: {result}")

        await update.message.reply_text(result, reply_markup=get_keyboard())

    except Exception as e:
        print(f"❌ handler error: {e}")
        await update.message.reply_text("⚠️ 系統錯誤", reply_markup=get_keyboard())


# ===== 主程式 =====
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 🔥 穩定版（關鍵）
    print("🚀 Starting Polling Bot...")
    app.run_polling()


if __name__ == "__main__":
    main()
