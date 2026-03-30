
# =========================
# 🔥 Performance Stub（暫時版）
# =========================

def evaluate_performance(results):

    if not results:
        return 0

    total = 0
    for r in results:
        total += r.get("ret", 0)

    avg_return = total / len(results)

    print(f"📊 平均報酬: {round(avg_return, 4)}")

    return avg_return
