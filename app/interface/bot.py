import os
from telegram import ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from app.main import run_trade, run_observe
from app.core.performance_tracker import get_performance
from app.core.optimizer import suggest_params
from app.core.portfolio import summary
from app.core.single_stock import analyze

TOKEN = os.getenv("TELEGRAM_TOKEN")

if TOKEN:
    TOKEN = TOKEN.strip()

if not TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN 未設定")


# ===== 按鈕 =====
def get_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["📊 今日推薦"],
            ["🚀 今日爆發股"],
            ["🔍 單股分析"],
            ["📈 績效報告"],
            ["🤖 AI優化"],
            ["⚙️ 系統狀態"]
        ],
        resize_keyboard=True
    )


# ===== start =====
async def start(update, context):
    await update.message.reply_text("🤖 AI交易系統已啟動", reply_markup=get_keyboard())


# ===== 文字標準化（關鍵🔥）=====
def normalize(text):
    return text.strip().replace("\n", "").replace("\r", "")


# ===== 主邏輯 =====
async def handle_message(update, context):

    raw_text = update.message.text
    text = normalize(raw_text)

    print(f"📩 收到: [{raw_text}] → [{text}]")  # 🔥 debug

    try:

        if "今日推薦" in text:
            result = run_observe()

        elif "今日爆發" in text:
            result = run_trade()

        elif "績效" in text:
            result = get_performance()

        elif "AI優化" in text:
            result = suggest_params()

        elif "系統狀態" in text:
            result = system_status()

        elif "單股分析" in text:
            await update.message.reply_text("請輸入股票代碼，例如：2330.TW")
            return

        elif text.endswith(".TW"):
            data = analyze(text)

            result = f"""
📊 {data['symbol']}
價格：{round(data['price'],2)}
勝率：{round(data['prob'],3)}
趨勢：{data['trend']}

🧠 AI分析：
{data['reason']}
"""

        else:
            result = f"⚠️ 無法識別指令: {text}"

        await update.message.reply_text(result, reply_markup=get_keyboard())

    except Exception as e:
        print("❌ BOT ERROR:", e)
        await update.message.reply_text(f"⚠️ 系統錯誤: {e}", reply_markup=get_keyboard())


# ===== 系統狀態 =====
def system_status():

    status = []

    if os.path.exists("data/model_v3.pkl"):
        status.append("模型：🟢")
    else:
        status.append("模型：🔴")

    try:
        s = summary({})
        status.append(f"資金：{s['cash']}")
        status.append(f"持倉：{s['positions']}")
    except:
        status.append("資金：❌")

    if os.getenv("OPENAI_API_KEY"):
        status.append("OpenAI：🟢")
    else:
        status.append("OpenAI：🔴")

    return "\n".join(status)


# ===== 啟動 =====
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot 啟動中...")
    app.run_polling()


if __name__ == "__main__":
    main()
