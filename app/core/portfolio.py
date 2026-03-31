import json
import os
from app.core.trade_logger import log_trade

FILE = "portfolio.json"

def load_portfolio():
    if not os.path.exists(FILE):
        return {"cash": 5000000, "positions": []}

    return json.load(open(FILE))

def save_portfolio(data):
    json.dump(data, open(FILE,"w"), indent=2)

def open_position(symbol, price, action):

    data = load_portfolio()

    size = 300000

    if data["cash"] < size:
        return

    for p in data["positions"]:
        if p["symbol"] == symbol:
            return

    data["cash"] -= size

    data["positions"].append({
        "symbol": symbol,
        "entry": price,
        "action": action,
        "size": size
    })

    save_portfolio(data)

def check_positions(prices):

    data = load_portfolio()
    new_positions = []

    for p in data["positions"]:

        symbol = p["symbol"]
        entry = p["entry"]
        size = p["size"]

        price = prices.get(symbol)

        if price is None:
            new_positions.append(p)
            continue

        tp = entry * 1.05
        sl = entry * 0.97

        if price >= tp or price <= sl:

            pnl = (price - entry) / entry

            data["cash"] += size * (1 + pnl)

            log_trade(symbol, entry, price, pnl)

        else:
            new_positions.append(p)

    data["positions"] = new_positions
    save_portfolio(data)

def summary(prices):

    data = load_portfolio()

    cash = data["cash"]
    unrealized = 0

    for p in data["positions"]:
        price = prices.get(p["symbol"], p["entry"])
        pnl = (price - p["entry"]) / p["entry"]
        unrealized += p["size"] * pnl

    return {
        "cash": round(cash,2),
        "equity": round(cash + unrealized,2),
        "positions": len(data["positions"])
    }
