from app.core.selector import pick_candidates
from app.core.analysis import analyze_stock
from app.core.decision import make_decision

def run():

    stocks = pick_candidates()
    results = []

    for s in stocks:

        features = analyze_stock(s)
        decision = make_decision(features)

        results.append({
            "symbol": s["symbol"],
            "signal": decision["action"],
            "tp": decision["tp"],
            "sl": decision["sl"]
        })

    return {
        "market": "sideways",
        "strategy": "AI決策",
        "results": results
    }
