from app.core.q_learning import update_q

CONFIG = {
    "tp": 0.05,
    "sl": -0.03,
    "threshold": 0.7,
    "top_k": 2
}


def optimize_model(results, market):

    if not results:
        print("⚠️ 無資料")
        return CONFIG

    avg = sum([r["ret"] for r in results]) / len(results)

    print(f"📊 平均報酬: {round(avg,4)}")

    # 🔥 狀態加入市場
    state = f"{market}_tp:{CONFIG['tp']}_sl:{CONFIG['sl']}_th:{CONFIG['threshold']}"
    score = update_q(state, avg)

    print(f"🧠 Q值更新: {round(score,4)}")

    # 🔥 牛市策略
    if market == "bull":

        if avg > 0:
            CONFIG["tp"] = min(CONFIG["tp"] + 0.01, 0.1)
            CONFIG["threshold"] = min(CONFIG["threshold"] + 0.02, 0.9)
            print("📈 牛市 → 強攻")

        else:
            CONFIG["sl"] = max(CONFIG["sl"] - 0.01, -0.1)

    # 🔥 熊市策略
    elif market == "bear":

        CONFIG["top_k"] = 1
        CONFIG["threshold"] = 0.75
        print("🐻 熊市 → 保守 or 放空")

    # 🔥 震盪策略
    elif market == "sideways":

        CONFIG["top_k"] = 1
        CONFIG["threshold"] = 0.8
        print("🌀 震盪 → 少做")

    print(f"⚙️ 新參數: {CONFIG}")

    return CONFIG
