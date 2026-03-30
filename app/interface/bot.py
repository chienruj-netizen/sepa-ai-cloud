import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from app.main import run
from app.core.analysis import analyze_stock
from app.core.decision import make_decision

TOKEN = os.getenv("TELEGRAM_TOKEN")

# 👉 主選單（升級版）
keyboard = [
    ["📊 今日 AI 選股"],
    ["🔍 單股分析"],
    ["⚙️ 系統狀態"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# =====================
# 🚀 /start
# =====================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 SEPA Cloud AI Engine 已啟動\n請選擇功能👇",
        reply_markup=reply_markup
    )


# =====================
# 📊 今日選股
# =====================
async def today_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = run()

    results = data.get("results", [])
    results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)

    msg = f"🧠 AI市場分析\n市場：{data.get('market')}\n策略：{data.get('strategy')}\n\n"

    if not results:
        msg += "⚠️ 今日無機會（或資料不足）"
    else:
        for item in results:
            msg += (
                f"{item.get('symbol')}｜{item.get('signal')}\n"
                f"📊 分數:{item.get('score', 0)}\n"
                f"🎯 TP:{item.get('tp')} SL:{item.get('sl')}\n\n"
            )

    await update.message.reply_text(msg)


# =====================
# 🔍 單股分析
# =====================
async def stock_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_stock"] = True
    await update.message.reply_text("請輸入股票代碼，例如：2330")


# =====================
# ⚙️ 系統狀態
# =====================
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "⚙️ 系統狀態\n"
        "✅ 雲端運行\n"
        "✅ AI決策引擎\n"
        "✅ 即時資料（FinMind）\n"
        "✅ 新聞分析（NewsAPI）"
    )
    await update.message.reply_text(msg)


# =====================
# 🧠 處理輸入（🔥關鍵升級）
# =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    print("DEBUG:", text, context.user_data)

    # === 單股分析模式 ===
    if context.user_data.get("waiting_stock"):

        context.user_data["waiting_stock"] = False

        symbol = f"{text}.TW"

        try:
            features = analyze_stock({"symbol": symbol})

            if features is None:
                await update.message.reply_text("❌ 無法取得該股票資料")
                return

            decision = make_decision(features)

            msg = (
                f"📊 {symbol}\n\n"
                f"💰 現價：{features.get('price')}\n"
                f"📈 型態：{features.get('pattern')}\n"
                f"📊 MA20：{features.get('ma20')}｜MA60：{features.get('ma60')}\n"
                f"⚡ RSI：{features.get('rsi')}｜MACD：{features.get('macd')}\n\n"
                f"🧠 AI決策：{decision.get('action')}\n"
                f"🎯 TP：{decision.get('tp')}\n"
                f"🛑 SL：{decision.get('sl')}\n"
                f"📊 分數：{decision.get('score')}\n\n"
                f"📖 AI分析：\n{decision.get('reason')}"
            )

            await update.message.reply_text(msg)
            return

        except Exception as e:
            await update.message.reply_text(f"❌ 分析失敗：{e}")
            return

    # === 其他輸入（🔥修正這裡）===
    # 👉 不再顯示「請使用選單操作」
    # 👉 改成引導回選單
    await update.message.reply_text("👇 請點擊下方功能選單", reply_markup=reply_markup)


# =====================
# 🧠 主程式
# =====================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("today", today_cmd))

    # ✅ 按鈕（精準匹配）
    app.add_handler(MessageHandler(filters.Regex("^🔍 單股分析$"), stock_prompt))
    app.add_handler(MessageHandler(filters.Regex("^📊 今日 AI 選股$"), today_cmd))
    app.add_handler(MessageHandler(filters.Regex("^⚙️ 系統狀態$"), status_cmd))

    # ✅ 所有輸入（最後）
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
