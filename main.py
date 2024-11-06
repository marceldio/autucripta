from bot import get_last_price, place_order, monitor_profit, send_telegram_message

def main():
    symbol = "BTCUSDT"
    qty = 0.001  # Пример количества для торговли
    entry_price = get_last_price(symbol)

    # Открываем позицию
    order_id = place_order(symbol, "Buy", qty)
    if order_id:
        send_telegram_message(f"Открыта позиция: {symbol} по цене {entry_price}")
        monitor_profit(entry_price, symbol, qty)

if __name__ == "__main__":
    main()
