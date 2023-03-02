import os
import time
import logging
import requests
from binance.client import Client
from binance.exceptions import BinanceAPIException

logging.basicConfig(level=logging.DEBUG)

# Define the supported cryptocurrencies and their symbols
CRYPTO_SYMBOLS = {
    'BTC': 'BTC',
    'ETH': 'ETH',
    'USDT': 'USDT',
    'DOGE': 'DOGE',
}

# Define the exchanges and their API endpoints
EXCHANGES = {
    'Binance': {'api': 'binance', 'url': 'https://api.binance.com/api/v3/ticker/bookTicker?symbol={symbol}'},
    'Coinbase': {'api': 'coinbase', 'url': 'https://api.coinbase.com/v2/prices/{symbol}-USD/spot'},
    'Kraken': {'api': 'kraken', 'url': 'https://api.kraken.com/0/public/Ticker?pair={symbol}USD'},
    'Huobi': {'api': 'huobi', 'url': 'https://api.huobi.pro/market/detail/merged?symbol={symbol}'},
    'Bitfinex': {'api': 'bitfinex', 'url': 'https://api-pub.bitfinex.com/v2/ticker/{symbol}'},
    'Bitstamp': {'api': 'bitstamp', 'url': 'https://www.bitstamp.net/api/v2/ticker/{symbol}/'},
}

# Initialize the Binance client using the API key and secret stored in environment variables
client = Client(api_key=os.environ.get('BINANCE_API_KEY', ''), api_secret=os.environ.get('BINANCE_API_SECRET', ''))

def get_crypto_rates(crypto, exchange):
    start_time = time.time()
    if exchange == 'Binance':
        symbol = CRYPTO_SYMBOLS[crypto] + 'USDT'
        try:
            ticker = client.get_ticker(symbol=symbol)
            buy_rate = ticker['bidPrice']
            sell_rate = ticker['askPrice']
            end_time = time.time()
            response_time = end_time - start_time
            message = {
                'currency': crypto.upper(),
                'exchange_name': exchange,
                'buy_rate': buy_rate,
                'sell_rate': sell_rate,
                'response_time': response_time
            }
            logging.debug(f"Response message: {message}")
            return message
        except BinanceAPIException as e:
            error_message = e.message
            logging.debug(f"Error message: {error_message}")
            raise e
    elif exchange == 'Coinbase':
        symbol = CRYPTO_SYMBOLS[crypto] + '-USD'
        try:
            response = requests.get(EXCHANGES[exchange]['url'].format(symbol=symbol))
            response_time = time.time() - start_time
            data = response.json()
            buy_rate = data['data']['amount']
            sell_rate = data['data']['amount']
            message = {
                'currency': crypto.upper(),
                'exchange_name': exchange,
                'buy_rate': buy_rate,
                'sell_rate': sell_rate,
                'response_time': response_time
            }
            logging.debug(f"Response message: {message}")
            return message
        except Exception as e:
            error_message = str(e)
            logging.debug(f"Error message: {error_message}")
            raise e
    elif exchange == 'Kraken':
        symbol = CRYPTO_SYMBOLS[crypto] + 'USD'
        try:
            response = requests.get(EXCHANGES[exchange]['url'].format(symbol=symbol))
            response_time = time.time() - start_time
            data = response.json()['result'][symbol]
            buy_rate = data['b'][0]
            sell_rate = data['a'][0]
            message = {
                'currency': crypto.upper(),
                'exchange_name': exchange,
                'buy_rate': buy_rate,
                'sell_rate': sell_rate,
                'response_time': response_time
            }
            logging.debug(f"Response message: {message}")
            return message
        except Exception as e:
            error_message = str(e)
            logging.debug(f"Error message: {error_message}")
            raise e
    elif exchange == 'Huobi':
        symbol = CRYPTO_SYMBOLS[crypto] + 'usdt'
        try:
            response = requests.get(EXCHANGES[exchange]['url'].format(symbol=symbol)).json()
            buy_rate = response['tick']['bid'][0]
            sell_rate = response['tick']['ask'][0]
            end_time = time.time()
            response_time = end_time - start_time
            message = {
                'currency': crypto.upper(),
                'exchange_name': exchange,
                'buy_rate': buy_rate,
                'sell_rate': sell_rate,
                'response_time': response_time
            }
            logging.debug(f"Response message: {message}")
            return message
        except Exception as e:
            error_message = str(e)
            logging.debug(f"Error message: {error_message}")
            raise e
    elif exchange == 'Bitfinex':
        symbol = CRYPTO_SYMBOLS[crypto] + 'USD'
        try:
            response = requests.get(EXCHANGES[exchange]['url'].format(symbol=symbol)).json()
            buy_rate = response['bid']
            sell_rate = response['ask']
            end_time = time.time()
            response_time = end_time - start_time
            message = {
                'currency': crypto.upper(),
                'exchange_name': exchange,
                'buy_rate': buy_rate,
                'sell_rate': sell_rate,
                'response_time': response_time
            }
            logging.debug(f"Response message: {message}")
            return message
        except Exception as e:
            error_message = str(e)
            logging.debug(f"Error message: {error_message}")
            raise e
    elif exchange == 'Bitstamp':
        symbol = CRYPTO_SYMBOLS[crypto].lower() + 'usd'
        try:
            response = requests.get(EXCHANGES[exchange]['url'].format(symbol=symbol)).json()
            buy_rate = response['bid']
            sell_rate = response['ask']
            end_time = time.time()
            response_time = end_time - start_time
            message = {
                'currency': crypto.upper(),
                'exchange_name': exchange,
                'buy_rate': buy_rate,
                'sell_rate': sell_rate,
                'response_time': response_time
            }
            logging.debug(f"Response message: {message}")
            return message
        except Exception as e:
            error_message = str(e)
            logging.debug(f"Error message: {error_message}")
            raise e
    else:
        raise ValueError(f"Unsupported exchange: {exchange}")
