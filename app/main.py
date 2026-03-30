from app.core.selector import pick_candidates
from app.core.analysis import analyze_stock
from app.core.decision import make_decision

def run():

    stocks = pick_candidates()
    results = []

    for s in stocks:

        try:
            features = analyze_stock(s)

            if features is None:
                continue

            decision = make_decision(features)

            results.append({
                "symbol": s.get("symbol", "UNKNOWN"),
                "signal": decision.get("action", "⚪"),
                "tp": decision.get("tp", 0),
                "sl": decision.get("sl", 0)
            })

        except Exception as e:
            print(f"❌ Error processing {s}: {e}")
            continue

    return {
        "market": "sideways",
        "strategy": "AI決策",
        "results": results
    }
