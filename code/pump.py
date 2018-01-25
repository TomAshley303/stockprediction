# Import
import os
import sys
import time
import argparse
import ccxt

parser = argparse.ArgumentParser()
parser.add_argument("--quantity", type=float, help="Buy/Sell Quantity", default=6.0)
parser.add_argument("--symbol", type=str, help="Market Symbol (Ex: IOTABTC)", default='IOTABTC')
parser.add_argument("--minprofit", type=float, help="Target Profit", default=1.3)
parser.add_argument("--maxprofit", type=float, help="Target Profit", default=1.5)
parser.add_argument("--orderid", type=int, help="Target Order Id", default=0)
parser.add_argument("--testmode", type=bool, help="Test Mode True/False", default=False)
parser.add_argument("--pump", type=bool, help="Pump n Dump True/False", default=False)
parser.add_argument("--monitor", type=bool, help="Monitor Price True/False", default=False)
parser.add_argument("--watch", type=bool, help="Watch Price True/False", default=False)
parser.add_argument("--exchange", type=str, help="Selected Exchange", default='binance')
parser.add_argument("--wait_time", type=int, help="Wait Time (seconds)", default=3)
parser.add_argument("--increasing", type=float, help="Buy Price +Increasing (0.00000001)", default=0.00000001)
parser.add_argument("--decreasing", type=float, help="Sell Price -Decreasing (0.00000001)", default=0.00000001)
parser.add_argument("--price", type=float, help="Sell Price -Decreasing (0.00000001)")

option = parser.parse_args()

WAIT_TIME = option.wait_time
QUANTITY = option.quantity
MINPROFIT = option.minprofit
MAXPROFIT = option.maxprofit
TEST_MODE = option.testmode
EXCHANGE = option.exchange
LAST_ORDER_PRICE = 0.0
CONFIG = {
    'gdax': {
        'api_key': "5fa76ac6e0524c592f01667e6d3f453a",
        'secret': "NCWyljw5MM7N8tWdxrVQ4jg3ivuik1IzWpHOaP1OctgnmJb9xlxaWn1WzQinhZhTCobrZbrm1VZCknoS3hgE7w==",
        'password': '8x5dftkskkt'
    },
    "binance": {
        'api_key': "bLt8i8ah7z5OIhPcjW9XNISudKLWcQ4PxdWSLfK57r1Z1iEz8h4I8kwFSMgwLJR3",
        'secret': "mtKjfWoSP88Y8isnYFHvpgm2TLvOXl0lOdOHiSfnvvvc3hfa4nlsBk9HQ5auD4f6"
    },
    "hitbtc": {
        'api_key': "d332ac0c7ca9efb4798a389719d64eaf",
        'secret': "daa9b1d96b520b39cedbaefb1cbca34a"
    },
    "cryptopia": {
        "api_key": "4303ea93de0c4c64af6abf2e35e72fd7",
        "secret": "QuWSpBhV+xE352/6mSVImzaV1APCu2fP2LYOyPhBFVk="
    },
}


def get_exchange(exchange):
    config = CONFIG[exchange]
    if exchange == "gdax":
        return ccxt.gdax({
            "api_key": config['api_key'],
            "secret": config['secret'],
            "password": config['password']
        })
    if exchange == "binance":
        return ccxt.binance({
            "api_key": config['api_key'],
            "secret": config['secret']
        })
    if exchange == "hitbtc":
        return ccxt.hitbtc({
            "api_key": config['api_key'],
            "secret": config['secret']
        })
    if exchange == "cryptopia":
        return ccxt.cryptopia({
            "api_key": config['api_key'],
            "secret": config['secret']
        })


def watch_action(symbol, exchange):
    print("Auto Trading for %s. Enter your symbol. Ex: %s" % symbol, EXCHANGE)
    while True:
        time.sleep(1)
        tick = exchange.fetch_ticker(symbol)
        print("Time: %s , Symbol: %s, Last Ask: %.8f, Last Bid: %.8f, High: %.8f, Low: %.8f" % (
            str(tick["datetime"]), symbol, tick['ask'], tick['bid'], tick['high'], tick['low']))


def cancel_and_rebuy(exchange, order_id, symbol, quantity, buy_price):
    exchange.cancel_order(order_id, symbol  )
    while True:
        time.sleep(2)
        status = exchange.fetch_order_status(order_id)["status"]
        if status == "CANCELED":
            return exchange.create_limit_buy_order(symbol, quantity, buy_price)

def simple_trade_btc(symbol, quantity, exchange, buy_price=None, order_id=None):
    print("Simple Trade for Exchange: %s and Currency: %s \n" % (EXCHANGE, symbol))
    last_tick = exchange.fetch_ticker(symbol)
    # if buy_price is None:
    buy_price = last_tick['bid']
    LAST_ORDER_PRICE = buy_price
    buy_price = round(buy_price - (buy_price * 0.02), 5)
    buy_order = exchange.create_limit_buy_order(symbol, quantity, buy_price)
    print("Create Buy Order for %s at: \n" % symbol)
    print("Buy Price: %.5f \n" % buy_price * 0.01)
    while True:
        time.sleep(3)
        # print("Time: %s , Symbol: %s, Last Ask: %.8f, Last Bid: %.8f, High: %.8f, Low: %.8f" % (
        #     str(last_tick["datetime"]), symbol, last_tick['ask'], last_tick['bid'], last_tick['high'], last_tick['low']))
        buy_order_status = exchange.fetch_order_status(buy_order["id"])
        print("Exchange: %s and Currency: %s. Buy Order Status: %s \n" % (EXCHANGE, symbol, buy_order_status))
        if buy_order_status != "closed":
            last_tick = exchange.fetch_ticker(symbol)
            if last_tick['bid'] > buy_price:
                buy_price = last_tick['bid']
                buy_order = cancel_and_rebuy(exchange, symbol, buy_order['id'], quantity, buy_price)
        else:
            break
    # orders = exchange.fetch_closed_ozrders()
    sell_price = buy_price * MAXPROFIT

    sell_price = round(sell_price, 5)
    sell_order = exchange.create_limit_sell_order(symbol, quantity, sell_price)
    print("Create Sell Order for %s at: \n" % symbol)
    print("Sell Price: %.5f \n Original Buy Price: %.5f \n Profit Made (BTC): %.5f \n" %
          (sell_price, buy_price, sell_price - buy_price))
    while True:
        time.sleep(3)
        sell_order_status = exchange.fetch_order_status(sell_order["id"])
        print("Exchange: %s Currency: %s. Sell Order Status: %s \n" % (EXCHANGE, symbol, sell_order_status))
        if sell_order_status == "closed:":
            print("Sell Price: %.5f \n Original Buy Price: %.5f \n Profit Made (BTC): %.5f \n" %
                  (sell_price, buy_price, sell_price - buy_price))
            break
    print("Order Complete \n")


def main():
    symbol = option.symbol
    exchange = get_exchange(option.exchange)

    print("Auto Trading for %s, looking at Coin: %s " % (EXCHANGE, symbol))

    print("trader.py --quantity %s --symbol %s --profit %s --wait_time %s --orderid %s \n" % (
        option.quantity, symbol, option.maxprofit, option.wait_time, option.orderid))

    print('%%%s profit scanning for %s \n' % (MAXPROFIT, symbol))

    if TEST_MODE:
        print("Test mode active")

    while True:
        start_time = time.time()
        simple_trade_btc(symbol, QUANTITY, exchange, option.price)
        end_time = time.time()
        if end_time - start_time < WAIT_TIME:
            time.sleep(WAIT_TIME - (end_time - start_time))


if __name__ == "__main__":
    main()