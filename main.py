import time
import asyncio
from bot import (
    get_last_price,
    place_order,
    close_position,
    monitor_profit,
    send_telegram_message,
)

def main():
    symbol = "BTCUSDT"
    qty = 0.001  # Пример количества для торговли
    entry_price = get_last_price(symbol)

    # Открываем позицию
    order_id = place_order(symbol, "Buy", qty)
    if order_id:
        # Создаем постоянный цикл событий
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_telegram_message(f"Открыта позиция: {symbol} по цене {entry_price}"))

        # Начинаем отслеживание прибыли, используя один и тот же цикл событий
        monitor_profit(entry_price, symbol, qty, loop)

if __name__ == "__main__":
    main()
