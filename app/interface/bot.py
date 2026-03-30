import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from app.controller import analyze_single, get_today_picks

TOKEN = os.getenv("TELEGRAM_TOKEN")


# =====================
# UI
# =====================
def build_dashboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 今日爆發", callback_data="today"),
            InlineKeyboardButton("🔍 單股分析", callback_data="analyze")
        ],
        [
            InlineKeyboardButton("🚀 主升段", callback_data="long"),
            InlineKeyboardButton("💣 起跌段", callback_data="short")
        ]
    ])


# =====================
# 安全 edit
# =====================
async def safe_edit(query, text):
    try:
        await query.edit_message_text(text, reply_markup=build_dashboard())
    except Exception as e:
        if "Message is not modified" not in str(e):
            print("TG ERROR:", e)


# =====================
# 主畫面
# =====================
async def dashboard(update, context):
    await update.message.reply_text(
        "🚀 AI交易系統（V6：ML + GPT）",
        reply_markup=build_dashboard()
    )


# =====================
# 按鈕
# =====================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()
    action = query.data

    # 📊 今日爆發
    if action == "today":

        picks = get_today_picks()

        msg = "📊 今日爆發股（AI預測）\n\n"

        for p in picks:
            msg += (
                f"{p['symbol']}\n"
                f"📈 預測報酬：{round(p['score']*100,2)}%\n"
                f"📊 趨勢：{p['trend']}\n"
                f"🎯 動作：{p['action']}\n\n"
            )

    # 🔍 單股
    elif action == "analyze":
        context.user_data["waiting"] = True
        msg = "請輸入股票代碼，例如 2330"

    # 🚀 主升段
    elif action == "long":

        picks = get_today_picks()
        strong = [p for p in picks if p["trend"] == "bull"]

        msg = "🚀 主升段（AI）\n\n"

        for p in strong:
            msg += f"{p['symbol']}｜{round(p['score']*100,1)}%\n"

    # 💣 起跌段
    elif action == "short":

        picks = get_today_picks()
        weak = [p for p in picks if p["trend"] == "bear"]

        msg = "💣 起跌段（AI）\n\n"

        for p in weak:
            msg += f"{p['symbol']}｜{round(p['score']*100,1)}%\n"

    else:
        msg = "⚠️ 未知操作"

    await safe_edit(query, msg)


# =====================
# 單股（🔥GPT）
# =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("waiting"):

        context.user_data["waiting"] = False

        symbol = f"{update.message.text}.TW"

        result = analyze_single(symbol)

        f = result["features"]
        d = result["decision"]
        gpt = result.get("gpt", "")

        msg = (
            f"📊 {symbol}\n\n"
            f"💰 價格：{f['price']}\n"
            f"📈 型態：{f.get('pattern','-')}\n\n"
            f"📊 AI預測報酬：{round(result['score']*100,2)}%\n"
            f"🧠 決策：{d['action']}\n"
            f"🎯 TP:{d['tp']} SL:{d['sl']}\n\n"
        )

        if gpt:
            msg += f"🤖 GPT分析\n{gpt}"

        await update.message.reply_text(msg)


# =====================
# 啟動
# =====================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", dashboard))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 AI交易系統 V6 啟動")
    app.run_polling()


if __name__ == "__main__":
    main()
