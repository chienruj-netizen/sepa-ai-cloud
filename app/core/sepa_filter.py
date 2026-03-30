
from app.core.radar import detect_breakout
from app.core.reversal import detect_reversal


def apply_sepa_filter(symbol):

    breakout = detect_breakout(symbol)
    reversal = detect_reversal(symbol)

    return {
        "symbol": symbol,
        "breakout": breakout,
        "reversal": reversal
    }
