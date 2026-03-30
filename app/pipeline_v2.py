from app.core.selector import pick_candidates
from app.core.decision import make_decision
from app.core.strategy_report import build_trade_plan


def run_pipeline():

    candidates = pick_candidates()

    trades = []

    for c in candidates:
        d = make_decision(c, "bull", c["prob"])

        if d["action"] == "HOLD":
            continue

        trade = build_trade_plan(c, d)
        trades.append(trade)

    return trades
