import os
import logging
import certifi
from binance.client import Client as BinanceClient
from coinbase.wallet.client import Client as CoinbaseClient

BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.environ.get('BINANCE_SECRET_KEY')
COINBASE_API_KEY = os.environ.get('COINBASE_API_KEY')
COINBASE_API_SECRET = os.environ.get('COINBASE_API_SECRET')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_crypto_rates():
    try:
        # Initialize the Binance client using the API key and secret stored in environment variables
        client_binance = BinanceClient(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY, tld='us', requests_params={'verify': certifi.where()})

        # Initialize the Coinbase client using the API key and secret stored in environment variables
        client_coinbase = CoinbaseClient(api_key=COINBASE_API_KEY, api_secret=COINBASE_API_SECRET)

        binance_symbols = {'BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'XRPUSDT'}
        coinbase_symbols = {'BTC-USD', 'ETH-USD', 'DOGE-USD', 'XRP-USD'}
        crypto_rates = []

        for symbol in binance_symbols:
            ticker_binance = client_binance.get_symbol_ticker(symbol=symbol)

            if 'BTC' in symbol:
                symbol_coinbase = 'BTC-USD'
            elif 'ETH' in symbol:
                symbol_coinbase = 'ETH-USD'
            elif 'DOGE' in symbol:
                symbol_coinbase = 'DOGE-USD'
            elif 'XRP' in symbol:
                symbol_coinbase = 'XRP-USD'

            ticker_coinbase = client_coinbase.get_exchange_rates(currency=symbol_coinbase)

            rate = {
                'symbol': symbol,
                'binance': float(ticker_binance['price']),
                'coinbase': float(ticker_coinbase['rates']['USD']),
            }

            crypto_rates.append(rate)

        return crypto_rates
    except Exception as e:
        logger.error(f'Error getting crypto rates: {e}')
        return []
