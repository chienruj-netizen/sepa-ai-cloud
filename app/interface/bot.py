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
from app.core.radar import detect_trend

TOKEN = os.getenv("TELEGRAM_TOKEN")

# =====================
# 👉 主選單
# =====================
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
    try:
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
                    f"📈 趨勢:{item.get('trend')}\n"
                    f"🎯 TP:{item.get('tp')} SL:{item.get('sl')}\n\n"
                )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"❌ 系統錯誤：{e}")


# =====================
# 🔍 單股分析（入口）
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
        "✅ 新聞分析（NewsAPI）\n"
        "✅ 主升段雷達\n"
        "✅ 爆量偵測\n"
        "✅ 法人資金流"
    )
    await update.message.reply_text(msg)


# =====================
# 🧠 單股分析（核心）
# =====================
async def analyze_and_reply(update, symbol):

    try:
        features = analyze_stock({"symbol": symbol})

        if not features:
            await update.message.reply_text("❌ 無法取得資料")
            return

        # 🔥 核心修正（一定要有）
        trend = detect_trend(features)
        score = features["score"]

        decision = make_decision(features, trend, score)

        msg = (
            f"📊 {symbol}\n\n"
            f"💰 現價：{features.get('price')}\n"
            f"📈 型態：{features.get('pattern')}\n"
            f"📊 MA20：{features.get('ma20')}｜MA60：{features.get('ma60')}\n"
            f"⚡ RSI：{features.get('rsi')}｜MACD：{features.get('macd')}\n\n"
            f"📊 分數：{decision.get('score')}\n"
            f"🧠 AI決策：{decision.get('action')}\n"
            f"🎯 TP：{decision.get('tp')}｜🛑 SL：{decision.get('sl')}\n\n"
            f"📖 AI分析：\n{decision.get('reason', '')}"
        )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"❌ 分析失敗：{e}")


# =====================
# 🧠 輸入處理
# =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    print("DEBUG:", text, context.user_data)

    # 🔥 直接輸入股票
    if text.isdigit() and len(text) <= 5:
        symbol = f"{text}.TW"
        await analyze_and_reply(update, symbol)
        return

    # 🔍 單股模式
    if context.user_data.get("waiting_stock"):
        context.user_data["waiting_stock"] = False
        symbol = f"{text}.TW"
        await analyze_and_reply(update, symbol)
        return

    # 📊 今日選股
    if text == "📊 今日 AI 選股":
        await today_cmd(update, context)
        return

    # ⚙️ 系統狀態
    if text == "⚙️ 系統狀態":
        await status_cmd(update, context)
        return

    # fallback
    await update.message.reply_text(
        "👇 請點擊下方功能選單",
        reply_markup=reply_markup
    )


# =====================
# 🚀 主程式
# =====================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("today", today_cmd))

    app.add_handler(MessageHandler(filters.Regex("^🔍 單股分析$"), stock_prompt))
    app.add_handler(MessageHandler(filters.Regex("^📊 今日 AI 選股$"), today_cmd))
    app.add_handler(MessageHandler(filters.Regex("^⚙️ 系統狀態$"), status_cmd))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
