import os
import time
from crypto_rates import get_crypto_rates
from send_message import send_whatsapp_message, send_telegram_message

WHATSAPP_USERS = os.environ.get('WHATSAPP_USERS').split(',')
TELEGRAM_CHAT_IDS = os.environ.get('TELEGRAM_CHAT_IDS').split(',')

def send_crypto_rates():
    crypto_rates = get_crypto_rates()

    message = 'Crypto Rates:\n\n'
    for rate in crypto_rates:
        message += f"{rate['symbol']}:\nBinance: {rate['binance']}\nCoinbase: {rate['coinbase']}\n\n"

    for user in WHATSAPP_USERS:
        send_whatsapp_message(user, message)

    for chat_id in TELEGRAM_CHAT_IDS:
        send_telegram_message(chat_id, message)

def lambda_handler(event, context):
    send_crypto_rates()
