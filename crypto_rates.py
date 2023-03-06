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

        crypto_pairs_binance = {'BTCUSDT': 'BTCUSD', 'ETHUSDT': 'ETHUSD', 'DOGEUSDT': 'DOGEUSD', 'XRPUSDT': 'XRPUSD'}
        crypto_pairs_coinbase = {'BTCUSD': 'BTC-USD', 'ETHUSD': 'ETH-USD', 'DOGEUSD': 'DOGE-USD', 'XRPUSD': 'XRP-USD'}
        crypto_rates = []

        for binance_pair, coinbase_pair in zip(crypto_pairs_binance.keys(), crypto_pairs_coinbase.keys()):
            logger.info(f'Fetching rate for binance pair: {binance_pair}, coinbase pair: {coinbase_pair}')
            ticker_binance = client_binance.get_symbol_ticker(symbol=binance_pair)
            ticker_coinbase = client_coinbase.get_exchange_rates(currency=coinbase_pair)

            rate = {
                'symbol': binance_pair,
                'binance': {
                    'buy': client_binance.get_ticker(symbol=binance_pair)['bidPrice'],
                    'sell': client_binance.get_ticker(symbol=binance_pair)['askPrice']
                },
                'coinbase': {
                    'buy': ticker_coinbase['buy'],
                    'sell': ticker_coinbase['sell']
                }
            }

            crypto_rates.append(rate)
        logger.info(f'crypto rates: {crypto_rates}')
        return crypto_rates
    except Exception as e:
        logger.error(f'Error getting crypto rates: {e}')
        return []
