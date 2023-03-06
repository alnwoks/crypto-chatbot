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

        for binance_pair, coinbase_pair in zip(crypto_pairs_binance.keys(), crypto_pairs_coinbase.keys()):
            ticker_binance = client_binance.get_symbol_ticker(symbol=binance_pair)
            ticker_coinbase = client_coinbase.get_exchange_rates(currency=coinbase_pair)

            buy_rate_binance = client_binance.get_orderbook_ticker(symbol=binance_pair)['askPrice']
            sell_rate_binance = client_binance.get_orderbook_ticker(symbol=binance_pair)['bidPrice']

            buy_rate_coinbase = client_coinbase.get_buy_price(currency_pair=coinbase_pair)['amount']
            sell_rate_coinbase = client_coinbase.get_sell_price(currency_pair=coinbase_pair)['amount']

            rate = {
                'symbol': binance_pair,
                'binance': {
                    'buy': float(buy_rate_binance),
                    'sell': float(sell_rate_binance),
                },
                'coinbase': {
                    'buy': float(buy_rate_coinbase),
                    'sell': float(sell_rate_coinbase),
                },
            }

            crypto_rates.append(rate)
        logger.info(f'crypto rates: {crypto_rates}')
        return crypto_rates
    except Exception as e:
        logger.error(f'Error getting crypto rates: {e}')
        return []
