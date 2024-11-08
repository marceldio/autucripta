from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_API_SECRET

# Инициализация клиента Bybit для тестовой среды
bybit_client = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET, testnet=True)

def get_wallet_balance():
    try:
        # Запрос информации о балансе с указанием accountType
        response = bybit_client.get_wallet_balance(accountType="UNIFIED")
        if response['retCode'] == 0:
            balances = response['result']['list']
            for account in balances:
                print(f"Тип аккаунта: {account['accountType']}")
                for coin in account['coin']:
                    print(f"Монета: {coin['coin']}")
                    print(f"Доступный баланс: {coin['availableToWithdraw']}")
                    print(f"Общий баланс: {coin['walletBalance']}")
                    print("-" * 30)
        else:
            print(f"Ошибка: {response['retMsg']}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    get_wallet_balance()
