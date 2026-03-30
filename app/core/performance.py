
def evaluate_performance(results):

    if not results:
        print("⚠️ 無交易")
        return 0

    returns = [r["ret"] for r in results]

    wins = [r for r in returns if r > 0]
    losses = [r for r in returns if r <= 0]

    win_rate = len(wins) / len(returns)

    avg_win = sum(wins)/len(wins) if wins else 0
    avg_loss = sum(losses)/len(losses) if losses else 0

    ev = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)

    print("\n📊 ===== 評估 =====")
    print(f"交易數: {len(returns)}")
    print(f"勝率: {round(win_rate,2)}")
    print(f"EV: {round(ev,4)}")

    return ev
