import os
import logging
from binance.client import Client as BinanceClient
from coinbase.wallet.client import Client as CoinbaseClient
import certifi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.environ.get('BINANCE_SECRET_KEY')
COINBASE_API_KEY = os.environ.get('COINBASE_API_KEY')
COINBASE_API_SECRET = os.environ.get('COINBASE_API_SECRET')

def get_crypto_rates():
    # Initialize the Binance client using the API key and secret stored in environment variables
    client_binance = BinanceClient(api_key=os.environ.get('BINANCE_API_KEY', ''), api_secret=os.environ.get('BINANCE_SECRET_KEY', ''), tld='us', requests_params={'verify': certifi.where()})

    # Initialize the Coinbase client using the API key and secret stored in environment variables
    client_coinbase = CoinbaseClient(api_key=os.environ.get('COINBASE_API_KEY', ''), api_secret=os.environ.get('COINBASE_API_SECRET', ''))

    crypto_pairs = ['BTC-USD', 'ETH-USD', 'DOGE-USD', 'XRP-USD']
    crypto_rates = []

    for pair in crypto_pairs:
        try:
            ticker_binance = client_binance.get_symbol_ticker(symbol=pair)
            ticker_coinbase = client_coinbase.get_exchange_rates(currency=pair)

            rate = {
                'symbol': pair,
                'binance': float(ticker_binance['price']),
                'coinbase': float(ticker_coinbase['rates']['USD']),
            }

            crypto_rates.append(rate)
        except Exception as e:
            logger.error(f"Failed to get rates for {pair}: {e}")

    return crypto_rates
