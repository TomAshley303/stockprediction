import pandas
import ccxt
import time

binance = ccxt.binance({
    'apiKey': 'bLt8i8ah7z5OIhPcjW9XNISudKLWcQ4PxdWSLfK57r1Z1iEz8h4I8kwFSMgwLJR3',
    'secret': 'mtKjfWoSP88Y8isnYFHvpgm2TLvOXl0lOdOHiSfnvvvc3hfa4nlsBk9HQ5auD4f6'
})

markets = binance.load_markets()

delay = 2 # seconds

while 1 == 1:
    print(binance.fetch_trades('TRX/BTC'))

# if binance.hasFetchOHLCV:
#     for symbol in binance.markets:
#         time.sleep(binance.rateLimit / 1000)  # time.sleep wants seconds
#         print(symbol, binance.fetch_ohlcv(symbol, '1d'))  # one day


