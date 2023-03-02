import os
import logging
from telegram.ext import Updater, CommandHandler
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

# Initialize the Telegram bot using the API token stored in the environment variable
TELEGRAM_BOT_TOKEN = os.environ.get('YOUR_TELEGRAM_BOT_TOKEN', '')

updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

def start(update, context):
    """Handler function for the /start command."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Use the /getrate command to get the current buy and sell rates for a cryptocurrency on supported exchanges.")

def getrate(update, context):
    """Handler function for the /getrate command."""
    # Parse the cryptocurrency and exchange arguments
    try:
        crypto = context.args[0].upper()
        exchange = context.args[1].title()
    except IndexError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid command format. Please use the format /getrate <cryptocurrency symbol> <exchange name>.")
        return

    # Check if the cryptocurrency symbol is valid
    if crypto not in CRYPTO_SYMBOLS:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Unsupported cryptocurrency symbol: {crypto}")
        return

    # Check if the exchange name is valid
    if exchange not in EXCHANGES:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Unsupported exchange name: {exchange}")
        return

    # Get the buy and sell rates for the cryptocurrency on the exchange
    try:
        response = get_crypto_rates(crypto, exchange)
    except Exception as e:
        error_message = str(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error getting rates from {exchange}: {error_message}")
        return

    # Format the response message using the default message template
    # response_message = MESSAGE_TEMPLATE.format(
    #     currency=crypto,
    #     exchange=response['exchange_name'],
    #     buy_rate=response['buy_rate'],
    #     sell_rate=response['sell_rate'],
    #     response_time=response['response_time']
    # )

    # # Send the response message back to the user via the Telegram bot
    # context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)

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
                return

    # Send the latest crypto rates to the user via WhatsApp
    if len(crypto_rates) > 0:
        message = "\n\n".join(crypto_rates)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def main():
    # Register the command handlers with the Telegram bot
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('getrate', getrate))

    # Start the Telegram bot
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()