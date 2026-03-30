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

# 🔥 新增
from app.core.backtest_engine import run_backtest
from app.core.performance import analyze_performance
from app.core.optimizer import optimize
from app.core.ai_optimizer import save_best
from app.core.portfolio import get_equity

TOKEN = os.getenv("TELEGRAM_TOKEN")

# =====================
# 👉 主選單（升級版）
# =====================
keyboard = [
    ["📊 今日 AI 選股"],
    ["🔍 單股分析"],
    ["⚙️ 系統狀態"],
    ["📈 回測分析", "🤖 AI優化"],
    ["💰 資產狀態"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# =====================
# 🚀 /start
# =====================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 AI交易系統 已啟動\n請選擇功能👇",
        reply_markup=reply_markup
    )


# =====================
# 📊 今日選股
# =====================
async def today_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = run()
        results = data.get("results", [])

        msg = f"🧠 AI市場分析\n市場：{data.get('market')}\n策略：{data.get('strategy')}\n\n"

        if not results:
            msg += "⚠️ 今日無機會"
        else:
            for r in results:
                msg += (
                    f"{r['symbol']}｜{r['signal']}\n"
                    f"分數:{r['score']}｜趨勢:{r['trend']}\n"
                    f"TP:{r['tp']} SL:{r['sl']}\n\n"
                )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"❌ 系統錯誤：{e}")


# =====================
# 🔍 單股分析
# =====================
async def stock_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_stock"] = True
    await update.message.reply_text("請輸入股票代碼，例如：2330")


async def analyze_and_reply(update, symbol):

    try:
        features = analyze_stock({"symbol": symbol})

        if not features:
            await update.message.reply_text("❌ 無法取得資料")
            return

        trend = detect_trend(features)
        score = features["score"]

        decision = make_decision(features, trend, score)

        msg = (
            f"📊 {symbol}\n\n"
            f"💰 價格：{features['price']}\n"
            f"📈 型態：{features['pattern']}\n"
            f"📊 MA20：{features['ma20']}\n"
            f"⚡ RSI：{features['rsi']}\n\n"
            f"🧠 AI：{decision['action']}\n"
            f"🎯 TP:{decision['tp']} SL:{decision['sl']}\n"
            f"📊 RR:{decision['rr']}\n"
        )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"❌ 分析失敗：{e}")


# =====================
# 📈 回測
# =====================
async def backtest_cmd(update, context):

    try:
        df = run_backtest("2330.TW")
        perf = analyze_performance(df)

        msg = (
            "📈 回測結果\n\n"
            f"勝率：{perf['win_rate']}\n"
            f"平均報酬：{perf['avg_return']}\n"
            f"總報酬：{perf['total_return']}\n"
            f"交易數：{perf['trades']}"
        )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"❌ 回測失敗：{e}")


# =====================
# 🤖 AI優化
# =====================
async def optimize_cmd(update, context):

    try:
        best, _ = optimize()
        save_best(best)

        msg = (
            "🤖 AI優化完成\n\n"
            f"threshold：{best['threshold']}\n"
            f"vol_ratio：{best['vol_ratio']}"
        )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"❌ 優化失敗：{e}")


# =====================
# 💰 資產
# =====================
async def portfolio_cmd(update, context):

    try:
        prices = {}  # 可升級成即時價格
        equity = get_equity(prices)

        await update.message.reply_text(f"💰 當前資產：{equity}")

    except Exception as e:
        await update.message.reply_text(f"❌ 資產錯誤：{e}")


# =====================
# ⚙️ 系統狀態
# =====================
async def status_cmd(update, context):
    msg = (
        "⚙️ 系統狀態\n"
        "✅ AI決策\n"
        "✅ 回測系統\n"
        "✅ 自動優化\n"
        "✅ 模擬持倉"
    )
    await update.message.reply_text(msg)


# =====================
# 🧠 輸入處理
# =====================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    if text.isdigit():
        symbol = f"{text}.TW"
        await analyze_and_reply(update, symbol)
        return

    if context.user_data.get("waiting_stock"):
        context.user_data["waiting_stock"] = False
        symbol = f"{text}.TW"
        await analyze_and_reply(update, symbol)
        return

    if text == "📊 今日 AI 選股":
        await today_cmd(update, context)

    elif text == "📈 回測分析":
        await backtest_cmd(update, context)

    elif text == "🤖 AI優化":
        await optimize_cmd(update, context)

    elif text == "💰 資產狀態":
        await portfolio_cmd(update, context)

    elif text == "⚙️ 系統狀態":
        await status_cmd(update, context)

    else:
        await update.message.reply_text("請使用下方選單👇", reply_markup=reply_markup)


# =====================
# 🚀 主程式
# =====================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
