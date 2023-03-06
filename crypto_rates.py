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
        crypto_pairs_coinbase = {'BTCUSDT': 'BTC-USD', 'ETHUSDT': 'ETH-USD', 'DOGEUSDT': 'DOGE-USD', 'XRPUSDT': 'XRP-USD'}
        crypto_rates = []

        for binance_pair, coinbase_pair in zip(crypto_pairs_binance.values(), crypto_pairs_coinbase.values()):
            try:
                logger.info(f'Getting rates for {binance_pair} and {coinbase_pair}')
                ticker_binance = client_binance.get_symbol_ticker(symbol=binance_pair)
                ticker_coinbase = client_coinbase.get_exchange_rates(currency=coinbase_pair)

                rate = {
                    'symbol': binance_pair,
                    'binance': {'buy': float(ticker_binance['bidPrice']), 'sell': float(ticker_binance['askPrice'])},
                    'coinbase': {'buy': float(ticker_coinbase['rates']['USD']), 'sell': float(ticker_coinbase['rates']['USD'])},
                }

                crypto_rates.append(rate)
            except Exception as e:
                logger.error(f'Error getting rates for {binance_pair} and {coinbase_pair}: {e}')

        logger.info(f'crypto rates: {crypto_rates}')
        return crypto_rates
    except Exception as e:
        logger.error(f'Error getting crypto rates: {e}')
        return []
