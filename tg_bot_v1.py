import requests
import time
import asyncio
import telegram
import nest_asyncio
from telegram.ext import Application

# nest_asyncio kullanımı
nest_asyncio.apply()

# Bot token'ınızı ve chat id'nizi buraya ekleyin
API_TOKEN = "7263924313:AAEPgNTjfnq2MOwNaSxi6kI7jE0OSoSt4wI"
CHAT_ID = '1097680675'

# Botu oluşturma
bot = telegram.Bot(token=API_TOKEN)

async def send_telegram_message(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

def check_transactions(wallet_address):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [wallet_address, {"limit": 1}]
    }
    response = requests.post("https://api.mainnet-beta.solana.com", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["result"]
    return []

async def main():
    wallet_address = "2ifqKPBhTgapdDJFZKUJikPwTdeQTbypxBNaEsCtpWVa"
    last_transaction = None

    while True:
        transactions = check_transactions(wallet_address)
        if transactions:
            latest_transaction = transactions[0]["signature"]
            if latest_transaction != last_transaction:
                last_transaction = latest_transaction
                message = f"Yeni bir işlem gerçekleşti. İşlem İmzası: {latest_transaction}"
                await send_telegram_message(message)
        await asyncio.sleep(20)  # Her 20 saniyede bir kontrol

if __name__ == "__main__":
    asyncio.run(main())

