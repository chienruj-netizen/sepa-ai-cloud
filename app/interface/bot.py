import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from app.pipeline_v2 import run_pipeline
from app.core.market_regime import get_market_regime

TOKEN = os.getenv("TELEGRAM_TOKEN")

# 🔥 主選單
main_keyboard = [
    ["📊 今日策略"],
    ["🔍 單股分析"],
    ["🌍 市場判斷"],
    ["⚙️ 系統狀態"]
]

# 🔥 進階選單
advanced_keyboard = [
    ["📈 回測分析", "🤖 AI優化"],
    ["💰 資產狀態"],
    ["🔙 返回主選單"]
]


# ======================
# 主選單
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
    await update.message.reply_text("🤖 AI操盤系統已啟動", reply_markup=reply_markup)


# ======================
# 按鈕控制
# ======================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # 📊 今日策略
    if text == "📊 今日策略":
        await update.message.reply_text("🚀 分析中...")
        run_pipeline()
        await update.message.reply_text("✅ 已完成策略分析")

    # 🔍 單股分析
    elif text == "🔍 單股分析":
        await update.message.reply_text("請輸入股票代碼，例如：2330.TW")

    # 🌍 市場判斷
    elif text == "🌍 市場判斷":
        market = get_market_regime()
        await update.message.reply_text(f"🌍 市場狀態：{market}")

    # ⚙️ 系統狀態 → 進階頁
    elif text == "⚙️ 系統狀態":
        reply_markup = ReplyKeyboardMarkup(advanced_keyboard, resize_keyboard=True)
        await update.message.reply_text("⚙️ 系統設定", reply_markup=reply_markup)

    # 🔙 返回
    elif text == "🔙 返回主選單":
        reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)
        await update.message.reply_text("返回主選單", reply_markup=reply_markup)

    # 📈 回測
    elif text == "📈 回測分析":
        await update.message.reply_text("📈 回測功能開發中")

    # 🤖 AI優化
    elif text == "🤖 AI優化":
        await update.message.reply_text("🤖 AI優化中")

    # 💰 資產
    elif text == "💰 資產狀態":
        await update.message.reply_text("💰 資產統計開發中")

    else:
        await update.message.reply_text("⚠️ 未知指令")


# ======================
# 主程式
# ======================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
