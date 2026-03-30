import json
import os

FILE = "portfolio.json"


def load_portfolio():
    if not os.path.exists(FILE):
        return {"cash": 1000000, "positions": []}

    with open(FILE, "r") as f:
        return json.load(f)


def save_portfolio(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


# =====================
# 🟢 買進
# =====================
def open_position(symbol, price, action):

    data = load_portfolio()

    position = {
        "symbol": symbol,
        "entry": price,
        "action": action,
        "size": 0.1  # 10%資金
    }

    data["positions"].append(position)

    save_portfolio(data)


# =====================
# 🔴 出場
# =====================
def close_position(symbol, price):

    data = load_portfolio()

    new_positions = []

    for p in data["positions"]:

        if p["symbol"] != symbol:
            new_positions.append(p)
        else:
            entry = p["entry"]

            if p["action"] == "🟢 做多":
                pnl = (price - entry) / entry
            else:
                pnl = (entry - price) / entry

            data["cash"] *= (1 + pnl * p["size"])

    data["positions"] = new_positions

    save_portfolio(data)


# =====================
# 📊 計算總資產
# =====================
def get_equity(current_prices):

    data = load_portfolio()

    equity = data["cash"]

    for p in data["positions"]:
        symbol = p["symbol"]
        entry = p["entry"]
        size = p["size"]

        price = current_prices.get(symbol, entry)

        if p["action"] == "🟢 做多":
            pnl = (price - entry) / entry
        else:
            pnl = (entry - price) / entry

        equity += data["cash"] * pnl * size

    return round(equity, 2)
