from app.core.selector import pick_candidates
from app.core.analysis import analyze_stock
from app.core.decision import make_decision

def run():

    stocks = pick_candidates()

    results = []

    for s in stocks:

        symbol = s["symbol"]
        df = s["df"]

        features = analyze_stock(df)

        if features is None:
            continue

        decision = make_decision(features)

        results.append({
            "symbol": symbol,
            "signal": decision["action"],
            "tp": decision["tp"],
            "sl": decision["sl"]
        })

    return {
        "market": "sideways",
        "strategy": "AI決策",
        "results": results
    }
