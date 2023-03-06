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

        crypto_pairs = {
            'BTCUSDT': {'binance': 'BTCUSD', 'coinbase': 'BTC-USD'},
            'ETHUSDT': {'binance': 'ETHUSD', 'coinbase': 'ETH-USD'},
            'DOGEUSDT': {'binance': 'DOGEUSD', 'coinbase': 'DOGE-USD'},
            'XRPUSDT': {'binance': 'XRPUSD', 'coinbase': 'XRP-USD'}
        }
        crypto_rates = []

        for symbol, pairs in crypto_pairs.items():
            ticker_binance = client_binance.get_symbol_ticker(symbol=symbol)
            ticker_coinbase = client_coinbase.get_exchange_rates(currency=pairs['coinbase'])
            bid_price_binance = client_binance.get_order_book(symbol=symbol)['bids'][0][0]
            ask_price_binance = client_binance.get_order_book(symbol=symbol)['asks'][0][0]

            rate = {
                'symbol': symbol,
                'binance_buy': float(ask_price_binance),
                'binance_sell': float(bid_price_binance),
                'coinbase_buy': float(ticker_coinbase['rates']['USD']),
                'coinbase_sell': float(ticker_coinbase['rates']['USD'])
            }

            crypto_rates.append(rate)
            logger.info(f'crypto rates: {crypto_rates}')
        return crypto_rates
    except Exception as e:
        logger.error(f'Error getting crypto rates: {e}')
        return []
