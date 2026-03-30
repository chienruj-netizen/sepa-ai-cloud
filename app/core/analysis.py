def analyze_stock(stock):

    price = stock["price"]

    # 模擬型態（之後會升級AI）
    if price > 500:
        pattern = "主升段"
    elif price < 120:
        pattern = "起跌點"
    else:
        pattern = "盤整"

    return {
        "pattern": pattern,
        "price": price
    }
