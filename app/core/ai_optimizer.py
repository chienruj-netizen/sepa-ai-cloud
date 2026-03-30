
def optimize_model(results):

    print("🧠 AI 優化中...")

    if not results:
        print("⚠️ 無回測資料")
        return

    # 🔥 強制轉 float
    avg = sum([float(r.get("ret", 0)) for r in results]) / len(results)

    print(f"📊 平均報酬（優化用）: {round(avg,4)}")

    if avg > 0:
        print("📈 策略表現良好")
    else:
        print("⚠️ 策略需優化")
        

def load_best():
    return None
