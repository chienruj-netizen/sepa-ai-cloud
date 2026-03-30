from app.core.backtest import calculate_win_rate


def get_strategy_mode():

    win_rate = calculate_win_rate()

    if win_rate < 0.45:
        return {
            "mode": "defense",
            "threshold": 70
        }

    elif win_rate > 0.6:
        return {
            "mode": "attack",
            "threshold": 50
        }

    else:
        return {
            "mode": "normal",
            "threshold": 60
        }
