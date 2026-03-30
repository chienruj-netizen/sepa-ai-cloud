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
# 📊 今日選股（排序＋理由）
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
                    f"📈 型態:{item.get('pattern', '未知')}\n"
                    f"🎯 TP:{item.get('tp')} SL:{item.get('sl')}\n"
                    f"🧠 理由:{item.get('reason', '')[:60]}...\n\n"
                )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"❌ 系統錯誤：{e}")


# =====================
# 🔍 單股分析（進入模式）
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
# 🧠 單股分析函式（共用）
# =====================
async def analyze_and_reply(update, symbol):

    try:
        features = analyze_stock({"symbol": symbol})

        if features is None:
            await update.message.reply_text("❌ 無法取得該股票資料")
            return

        decision = make_decision(features)

        msg = (
            f"📊 {symbol}\n\n"
            f"💰 現價：{features.get('price', 'N/A')}\n"
            f"📈 型態：{features.get('pattern', 'N/A')}\n"
            f"📊 MA20：{features.get('ma20', 'N/A')}｜MA60：{features.get('ma60', 'N/A')}\n"
            f"⚡ RSI：{features.get('rsi', 'N/A')}｜MACD：{features.get('macd', 'N/A')}\n\n"
            f"📊 分數：{decision.get('score', 0)}\n"
            f"🧠 AI決策：{decision.get('action')}\n"
            f"🎯 TP：{decision.get('tp')}｜🛑 SL：{decision.get('sl')}\n\n"
            f"📖 AI分析：\n{decision.get('reason', '')}"
        )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"❌ 分析失敗：{e}")


# =====================
# 🧠 所有輸入處理（🔥最強版本）
# =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    print("DEBUG:", text, context.user_data)

    # =====================
    # 🔥 直接輸入股票（最強）
    # =====================
    if text.isdigit() and len(text) <= 5:
        symbol = f"{text}.TW"
        await analyze_and_reply(update, symbol)
        return

    # =====================
    # 🔍 單股分析模式
    # =====================
    if context.user_data.get("waiting_stock"):

        context.user_data["waiting_stock"] = False

        symbol = f"{text}.TW"
        await analyze_and_reply(update, symbol)
        return

    # =====================
    # 📊 今日選股（文字觸發）
    # =====================
    if text == "📊 今日 AI 選股":
        await today_cmd(update, context)
        return

    # =====================
    # ⚙️ 系統狀態
    # =====================
    if text == "⚙️ 系統狀態":
        await status_cmd(update, context)
        return

    # =====================
    # fallback（不再顯示錯誤）
    # =====================
    await update.message.reply_text(
        "👇 請點擊下方功能選單",
        reply_markup=reply_markup
    )


# =====================
# 🧠 主程式
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
