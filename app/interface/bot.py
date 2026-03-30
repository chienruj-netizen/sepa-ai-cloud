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

from app.main import run
from app.core.analysis import analyze_stock
from app.core.decision import make_decision
from app.core.radar import detect_trend
from app.core.gpt_explainer import gpt_explain   # 🔥 GPT解讀

from app.core.backtest_engine import run_backtest
from app.core.performance import analyze_performance
from app.core.optimizer import optimize
from app.core.ai_optimizer import save_best
from app.core.portfolio import load_portfolio, get_equity

TOKEN = os.getenv("TELEGRAM_TOKEN")


# =====================
# 🎯 主面板
# =====================
def build_dashboard():

    keyboard = [
        [
            InlineKeyboardButton("📊 今日選股", callback_data="today"),
            InlineKeyboardButton("🔍 單股分析", callback_data="analyze")
        ],
        [
            InlineKeyboardButton("📈 回測", callback_data="backtest"),
            InlineKeyboardButton("🤖 AI優化", callback_data="optimize")
        ],
        [
            InlineKeyboardButton("📦 持倉", callback_data="portfolio"),
            InlineKeyboardButton("⚙️ 系統", callback_data="status")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =====================
# 📊 主畫面
# =====================
async def dashboard(update, context):

    data = run()
    portfolio = load_portfolio()
    equity = get_equity({})

    msg = (
        "📊 AI交易控制台\n\n"
        f"🧠 市場：{data.get('market')}\n"
        f"📈 策略：{data.get('strategy')}\n\n"
        f"💰 資產：{equity}\n"
        f"📦 持倉數：{len(portfolio['positions'])}\n\n"
        "────────────\n"
        "選擇操作👇"
    )

    await update.message.reply_text(msg, reply_markup=build_dashboard())


# =====================
# 🔘 按鈕控制
# =====================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()
    action = query.data

    # =====================
    # 📊 今日選股 + GPT
    # =====================
    if action == "today":

        data = run()
        results = data.get("results", [])

        msg = "📊 今日AI選股\n\n"

        if not results:
            msg += "⚠️ 今日無機會"
        else:
            for r in results:

                symbol = r["symbol"]

                features = analyze_stock({"symbol": symbol})
                trend = detect_trend(features)
                decision = make_decision(features, trend, features["score"])

                gpt_text = gpt_explain(features, decision, trend)

                msg += (
                    f"{symbol}｜{decision['action']}\n"
                    f"TP:{decision['tp']} SL:{decision['sl']}\n"
                    f"{gpt_text}\n\n"
                )

    # =====================
    # 🔍 單股分析
    # =====================
    elif action == "analyze":

        context.user_data["waiting_input"] = True
        msg = "請輸入股票代碼，例如：2330"

    # =====================
    # 📈 回測
    # =====================
    elif action == "backtest":

        df = run_backtest("2330.TW")
        perf = analyze_performance(df)

        msg = (
            "📈 回測結果\n\n"
            f"勝率：{perf['win_rate']}\n"
            f"平均報酬：{perf['avg_return']}\n"
            f"總報酬：{perf['total_return']}\n"
        )

    # =====================
    # 🤖 AI優化
    # =====================
    elif action == "optimize":

        best, _ = optimize()
        save_best(best)

        msg = (
            "🤖 AI優化完成\n\n"
            f"threshold：{best['threshold']}\n"
            f"vol_ratio：{best['vol_ratio']}"
        )

    # =====================
    # 📦 持倉
    # =====================
    elif action == "portfolio":

        data = load_portfolio()

        msg = "📦 持倉\n\n"

        if not data["positions"]:
            msg += "目前無持倉"
        else:
            for p in data["positions"]:
                msg += f"{p['symbol']}｜{p['action']}｜{p['entry']}\n"

    # =====================
    # ⚙️ 系統
    # =====================
    elif action == "status":

        msg = (
            "⚙️ 系統狀態\n"
            "✅ GPT決策\n"
            "✅ 回測系統\n"
            "✅ 自動優化\n"
            "✅ 模擬持倉"
        )

    else:
        msg = "⚠️ 未知操作"

    await query.edit_message_text(msg, reply_markup=build_dashboard())


# =====================
# 🔍 接收輸入（單股）
# =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("waiting_input"):

        context.user_data["waiting_input"] = False

        symbol = f"{update.message.text}.TW"

        try:
            features = analyze_stock({"symbol": symbol})
            trend = detect_trend(features)
            decision = make_decision(features, trend, features["score"])

            gpt_text = gpt_explain(features, decision, trend)

            msg = (
                f"📊 {symbol}\n\n"
                f"💰 價格：{features['price']}\n"
                f"📈 型態：{features['pattern']}\n\n"
                f"🧠 AI：{decision['action']}\n"
                f"🎯 TP:{decision['tp']} SL:{decision['sl']}\n\n"
                f"{gpt_text}"
            )

        except Exception as e:
            msg = f"❌ 分析失敗：{e}"

        await update.message.reply_text(msg, reply_markup=build_dashboard())


# =====================
# 🚀 主程式
# =====================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", dashboard))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 Trading Panel Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
