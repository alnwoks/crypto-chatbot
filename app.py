import requests
import json
import time

TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
WHATSAPP_BOT_TOKEN = 'YOUR_WHATSAPP_BOT_TOKEN'

# Cryptocurrency exchange APIs
CRYPTO_API_URLS = [
    'https://api.example.com/crypto_rates_1',
    'https://api.example.com/crypto_rates_2',
    'https://api.example.com/crypto_rates_3'
]

# Cryptocurrencies to track
CRYPTO_LIST = ['BTC', 'ETH', 'USDT', 'DOGE']

# Default message template
DEFAULT_MESSAGE_TEMPLATE = "The latest buy rate of {crypto} on {exchange} is {buy_rate} and the latest sell rate is {sell_rate}. Response time: {response_time} seconds"

# Function to handle messages from Telegram
def telegram_handler(event, context):
    incoming_message = json.loads(event['body'])
    chat_id = incoming_message['message']['chat']['id']
    text = incoming_message['message']['text']

    if '/crypto' in text:
        # Get the cryptocurrency from the message
        crypto = text.split()[1].upper()

        # Get the latest rates for the specified cryptocurrency from all cryptocurrency exchange APIs
        rates = []
        for url in CRYPTO_API_URLS:
            exchange_name = url.split("/")[-1]
            exchange_rates = get_crypto_rates(crypto, url)
            rates.append({"exchange": exchange_name, "buy_rate": exchange_rates['buy'], "sell_rate": exchange_rates['sell'], "response_time": exchange_rates['response_time']})

        # Format the message with the latest rates from all cryptocurrency exchange APIs
        message = ""
        for rate in rates:
            message += DEFAULT_MESSAGE_TEMPLATE.format(crypto=crypto, exchange=rate['exchange'], buy_rate=rate['buy_rate'], sell_rate=rate['sell_rate'], response_time=rate['response_time']) + "\n"

        # Send the response message back to the user via the Telegram bot
        send_telegram_message(chat_id, message)

# Function to handle messages from WhatsApp
def whatsapp_handler(event, context):
    incoming_message = json.loads(event['body'])
    chat_id = incoming_message['messages'][0]['chatId']
    text = incoming_message['messages'][0]['body']

    if '/crypto' in text:
        # Get the cryptocurrency from the message
        crypto = text.split()[1].upper()

        # Get the latest rates for the specified cryptocurrency from all cryptocurrency exchange APIs
        rates = []
        for url in CRYPTO_API_URLS:
            exchange_name = url.split("/")[-1]
            exchange_rates = get_crypto_rates(crypto, url)
            rates.append({"exchange": exchange_name, "buy_rate": exchange_rates['buy'], "sell_rate": exchange_rates['sell'], "response_time": exchange_rates['response_time']})

        # Format the message with the latest rates from all cryptocurrency exchange APIs
        message = ""
        for rate in rates:
            message += DEFAULT_MESSAGE_TEMPLATE.format(crypto=crypto, exchange=rate['exchange'], buy_rate=rate['buy_rate'], sell_rate=rate['sell_rate'], response_time=rate['response_time']) + "\n"

        # Send the response message back to the user via the WhatsApp bot
        send_whatsapp_message(chat_id, message)

# Function to get the latest rates for a cryptocurrency from a cryptocurrency exchange API
def get_crypto_rates(crypto, url):
    # Call the API of a cryptocurrency exchange to get the latest rates for the specified cryptocurrency
    start_time = time.time()
    response = requests.get(url)
    response_time = time.time()
