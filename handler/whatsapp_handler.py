import os
import logging
from twilio.rest import Client
from get_crypto_rates import get_crypto_rates

logging.basicConfig(level=logging.DEBUG)

# Define the default
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

# Initialize the Twilio client using the account SID and auth token stored in the environment variables
TWILIO_ACCOUNT_SID = os.environ.get('YOUR_TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('YOUR_TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('YOUR_TWILIO_PHONE_NUMBER', '')
CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_message_whatsapp(message):
    """Sends a WhatsApp message containing the specified message text."""
    message = CLIENT.messages.create(
        from_='whatsapp:' + TWILIO_PHONE_NUMBER,
        to='whatsapp:' + os.environ.get('YOUR_WHATSAPP_NUMBER', ''),
        body=message
    )
    logging.debug(f"WhatsApp message SID: {message.sid}")

def main(event, context):
    """Main function that sends the latest crypto rates to the user via WhatsApp."""
    # Get the buy and sell rates for each supported cryptocurrency and exchange
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

    # Send the latest crypto rates to the user via WhatsApp
    if len(crypto_rates) > 0:
        message = "\n\n".join(crypto_rates)
        send_message_whatsapp(message)

if __name__ == '__main__':
    main()
