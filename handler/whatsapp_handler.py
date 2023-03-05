import os
import logging
from wa_automate_socket_client import SocketClient as  WhatsappClient
# from openwa import WhatsappClient
from get_crypto_rates import get_crypto_rates

logging.basicConfig(level=logging.DEBUG)

# Define the default message template
MESSAGE_TEMPLATE = "Current buy rate for {currency} on {exchange}: {buy_rate}\nCurrent sell rate for {currency} on {exchange}: {sell_rate}\nResponse time: {response_time:.3f} seconds"

# Define the supported cryptocurrencies and their symbols
CRYPTO_SYMBOLS = {
    'BTC': 'BTC',
    'ETH': 'ETH',
    'USDT': 'USDT',
    'DOGE': 'DOGE',
}

# Define the supported exchanges
EXCHANGES = [
    'Binance',
    'Coinbase',
    'Kraken',
    'Huobi',
    'Bitfinex',
    'Bitstamp'
]

# Initialize the WhatsApp client using the session file stored in the environment variable
WA_SESSION_FILE = os.environ.get('WA_SESSION_FILE', '')

client = WhatsappClient(
    client_id=os.environ.get('WA_CLIENT_ID', ''),
    client_secret=os.environ.get('WA_CLIENT_SECRET', ''),
    session_path=WA_SESSION_FILE,
    logger=logging.getLogger(__name__)
)

def send_message(chat_id, message):
    """Sends a message to a WhatsApp chat."""
    client.send_message(chat_id, message)

def get_all_rates():
    """Gets the current buy and sell rates for all supported cryptocurrencies on all supported exchanges."""
    crypto_rates = []
    for crypto in CRYPTO_SYMBOLS.values():
        for exchange in EXCHANGES:
            try:
                response = get_crypto_rates(crypto, exchange)
                response_message = MESSAGE_TEMPLATE.format(
                    currency=crypto,
                    exchange=response['exchange_name'],
                    buy_rate=response['buy_rate'],
                    sell_rate=response['sell_rate'],
                    response_time=response['response_time']
                )
                crypto_rates.append(response_message)
            except Exception as e:
                error_message = str(e)
                logging.error(f"Error getting rates from {exchange}: {error_message}")
    return "\n\n".join(crypto_rates)

def on_message_received(message):
    """Handler function for incoming WhatsApp messages."""
    chat_id = message.chat.id
    text = message.text

    if text == '/start':
        response = "Hello! Use the /getallrates command to get the current buy and sell rates for all supported cryptocurrencies on all supported exchanges."
        send_message(chat_id, response)
    elif text == '/getallrates':
        response = get_all_rates()
        send_message(chat_id, response)
    else:
        response = "Invalid command. Please use /start or /getallrates."
        send_message(chat_id, response)

def main():
    """Main function for running the WhatsApp bot."""
    # Connect to the WhatsApp server
    client.connect()

    # Register the message handler with the WhatsApp client
    client.register_message_handler(on_message_received)

    # Wait for incoming messages
    client.wait_for_messages()

if __name__ == '__main__':
    main()
