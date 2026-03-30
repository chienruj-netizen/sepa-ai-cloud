from app.core.ml_predictor import predict_stock
from app.core.sepa_filter import apply_sepa_filter
from app.core.tw_stock_list import get_tw_stocks
from app.core.ai_optimizer import CONFIG


def pick_candidates():

    symbols = get_tw_stocks()

    results = []

    for s in symbols[:200]:

        try:
            ai = predict_stock(s)
            sepa = apply_sepa_filter(s)

            if not ai:
                continue

            score = ai["prob"]

            # 🔥 動態門檻
            if score > CONFIG["threshold"] and sepa["breakout"] and not sepa["reversal"]:
                results.append({
                    "symbol": s,
                    "prob": score,
                    "side": "LONG"
                })

            elif score < (1 - CONFIG["threshold"]) and sepa["reversal"]:
                results.append({
                    "symbol": s,
                    "prob": score,
                    "side": "SHORT"
                })

        except:
            continue

    results = sorted(results, key=lambda x: abs(x["prob"] - 0.5), reverse=True)

    return results[:CONFIG["top_k"]]
