import time
from pybit.unified_trading import HTTP
from telegram import Bot
from config import BYBIT_API_KEY, BYBIT_API_SECRET, TELEGRAM_TOKEN, CHAT_ID

# Инициализация клиента Bybit
bybit_client = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET, testnet=True)  # testnet=True для тестирования

# Инициализация клиента Telegram
telegram_bot = Bot(token=TELEGRAM_TOKEN)

# Функция для отправки сообщения в Telegram
def send_telegram_message(message):
    try:
        telegram_bot.send_message(chat_id=CHAT_ID, text=message)
        print("Сообщение отправлено в Telegram.")
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")

# Тестовое сообщение для проверки подключения к Telegram
def send_test_message():
    try:
        telegram_bot.send_message(chat_id=CHAT_ID, text="Бот успешно подключен к Telegram!")
        print("Соединение с Telegram успешно!")
    except Exception as e:
        print(f"Ошибка подключения к Telegram: {e}")

# Получение последней цены для символа (по умолчанию BTCUSDT) для теста соединения с Bybit API
def get_last_price(symbol="BTCUSDT"):
    try:
        ticker = bybit_client.get_tickers(category='linear', symbol=symbol)
        last_price = float(ticker['result']['list'][0]['lastPrice'])
        print(f"Последняя цена для {symbol}: {last_price}")
        return last_price
    except Exception as e:
        print(f"Ошибка подключения к Bybit: {e}")
        return None

# Функция для размещения рыночного ордера
def place_order(symbol, side, qty):
    try:
        order = bybit_client.place_order(
            category='linear',
            symbol=symbol,
            side=side,
            orderType='Market',
            qty=qty,
            timeInForce='GoodTillCancel',
            reduceOnly=False,
            closeOnTrigger=False
        )
        print(f"Открыт ордер {side} для {symbol} на {qty} единиц.")
        return order['result']['orderId']
    except Exception as e:
        print(f"Ошибка при размещении ордера: {e}")
        return None

# Функция для закрытия позиции
def close_position(symbol, side, qty):
    try:
        order = bybit_client.place_order(
            category='linear',
            symbol=symbol,
            side=side,
            orderType='Market',
            qty=qty,
            timeInForce='GoodTillCancel',
            reduceOnly=True,
            closeOnTrigger=False
        )
        print(f"Закрыт ордер {side} для {symbol} на {qty} единиц.")
        return order['result']['orderId']
    except Exception as e:
        print(f"Ошибка при закрытии ордера: {e}")
        return None

# Функция для отслеживания прибыли и закрытия позиции при достижении целевой прибыли
def monitor_profit(entry_price, symbol, qty, target_profit_percent=0.1):
    while True:
        current_price = get_last_price(symbol)
        if current_price is None:
            time.sleep(60)
            continue
        profit_percent = ((current_price - entry_price) / entry_price) * 100

        if profit_percent >= target_profit_percent:
            close_position(symbol, "Sell", qty)
            send_telegram_message(f"Позиция закрыта: {symbol} по цене {current_price} с прибылью {profit_percent:.2f}%")
            break

        time.sleep(60)  # Проверяем каждые 60 секунд

# Запуск тестов и основной функции
if __name__ == "__main__":
    send_test_message()
    get_last_price()
