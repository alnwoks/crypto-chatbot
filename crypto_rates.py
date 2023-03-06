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

        # Define the symbol mappings for each exchange
        binance_symbol_map = {'BTCUSDT': 'BTCUSD', 'ETHUSDT': 'ETHUSD', 'DOGEUSDT': 'DOGEUSD', 'XRPUSDT': 'XRPUSD'}
        coinbase_symbol_map = {'BTCUSDT': 'BTC-USD', 'ETHUSDT': 'ETH-USD', 'DOGEUSDT': 'DOGE-USD', 'XRPUSDT': 'XRP-USD'}

        crypto_rates = []

        for pair in binance_symbol_map.keys():
            binance_symbol = binance_symbol_map[pair]
            coinbase_symbol = coinbase_symbol_map[pair]

            ticker_binance = client_binance.get_symbol_ticker(symbol=pair)
            ticker_coinbase = client_coinbase.get_spot_price(currency_pair=coinbase_symbol)

            rate = {
                'symbol': pair,
                'binance': float(ticker_binance['price']),
                'coinbase': float(ticker_coinbase.amount),
            }

            crypto_rates.append(rate)
            logger.info(f'crypto rates: {crypto_rates}')

        return crypto_rates
    except Exception as e:
        logger.error(f'Error getting crypto rates: {e}')
        return []
