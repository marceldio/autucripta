import requests
import time
import hmac
import hashlib
import json
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Ваши данные API из .env
api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")
base_url = "https://api-testnet.bybit.com"
recv_window = "5000"
httpClient = requests.Session()

# Функция для генерации подписи
def genSignature(payload):
    param_str = str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(api_secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
    signature = hash.hexdigest()
    return signature

# Функция для запроса баланса
def get_balance():
    global time_stamp
    endpoint = "/v5/account/wallet-balance"
    url = base_url + endpoint

    # Получаем текущий timestamp
    time_stamp = str(int(time.time() * 1000))
    params = 'accountType=UNIFIED'  # тип аккаунта
    signature = genSignature(params)

    headers = {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-SIGN-TYPE": "2",
        "X-BAPI-TIMESTAMP": time_stamp,
        "X-BAPI-RECV-WINDOW": recv_window,
        "Content-Type": "application/json",
    }

    # Отправляем запрос с передачей параметров как строки запроса
    response = httpClient.request("GET", url + "?" + params, headers=headers)
    print("Response Text:", response.text)
    print("Response Headers:", response.headers)

# Запуск запроса баланса
get_balance()
