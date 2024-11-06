from pybit.unified_trading import HTTP
from telegram import Bot
from config import BYBIT_API_KEY, BYBIT_API_SECRET, TELEGRAM_TOKEN, CHAT_ID

# Инициализация клиента Bybit
bybit_client = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET, testnet=True)  # testnet=True для тестирования

# Инициализация клиента Telegram
telegram_bot = Bot(token=TELEGRAM_TOKEN)

# Тестовое сообщение для проверки подключения
def send_test_message():
    try:
        # Отправляем тестовое сообщение в Telegram
        telegram_bot.send_message(chat_id=CHAT_ID, text="Бот успешно подключен к Telegram!")
        print("Соединение с Telegram успешно!")
    except Exception as e:
        print(f"Ошибка подключения к Telegram: {e}")

# Получение последней цены BTCUSDT для теста соединения с Bybit API
def get_last_price(symbol="BTCUSDT"):
    try:
        ticker = bybit_client.get_tickers(category='linear', symbol=symbol)
        last_price = ticker['result']['list'][0]['lastPrice']
        print(f"Последняя цена для {symbol}: {last_price}")
        return last_price
    except Exception as e:
        print(f"Ошибка подключения к Bybit: {e}")

# Запуск тестов
if __name__ == "__main__":
    send_test_message()
    get_last_price()
