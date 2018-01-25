# -*- coding: UTF-8 -*-
# @yasinkuyu

import os
import sys
import time
# from .config import *
import argparse
import ccxt


parser = argparse.ArgumentParser()
parser.add_argument("--quantity", type=int, help="Buy/Sell Quantity", default=6)
parser.add_argument("--symbol", type=str, help="Market Symbol (Ex: IOTABTC)", default='IOTABTC')
parser.add_argument("--profit", type=float, help="Target Profit", default=1.3)
parser.add_argument("--orderid", type=int, help="Target Order Id", default=0)
parser.add_argument("--testmode", type=bool, help="Test Mode True/False", default=False)
parser.add_argument("--pump", type=bool, help="Pump n Dump True/False", default=False)
parser.add_argument("--monitor", type=bool, help="Monitor Price True/False", default=False)
parser.add_argument("--exchange", type=str, help="Selected Exchange", default=False)
parser.add_argument("--wait_time", type=int, help="Wait Time (seconds)", default=3)
parser.add_argument("--increasing", type=float, help="Buy Price +Increasing (0.00000001)", default=0.00000001)
parser.add_argument("--decreasing", type=float, help="Sell Price -Decreasing (0.00000001)", default=0.00000001)

option = parser.parse_args()

TEST_MODE = option.testmode

PROFIT = option.profit
ORDER_ID = option.orderid
QUANTITY = option.quantity
WAIT_TIME = option.wait_time  # seconds
TARGET_PRICE = 0
TARGET_PROFITABLE_PRICE = None
LAST_PROFIT_PCT_HIT = 0

# client = BinanceAPI(Config.api_key, Config.api_secret)


def write(data):
    file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ORDER'), 'w')
    file.write(data)

#
# def buy_limit(symbol, quantity, buyPrice):
#     global TEST_MODE
#
#     if TEST_MODE:
#         return "100000"
#
#     ret = client.buy_limit(symbol, quantity, buyPrice)
#     if 'msg' in ret:
#         errexit(ret['msg'])
#
#     orderId = ret['orderId']
#
#     write("{}\n".format([symbol, orderId, quantity, buyPrice]))
#
#     print("******************")
#     print('Order Id: %d' % orderId)
#
#     return orderId


# def sell_limit(symbol, quantity, orderId):
#     global TEST_MODE
#     global ORDER_ID
#     global TARGET_PRICE
#     global TARGET_PROFITABLE_PRICE
#
#     ret = client.get_open_orders(symbol)
#     if 'msg' in ret:
#         errexit(ret['msg'])
#
#     print("Orders")
#
#     for order in ret:
#         price = float(order['price'])
#         origQty = float(order['origQty'])
#         executedQty = float(order['executedQty'])
#
#         if order['orderId'] == orderId:
#             print("Order: %d: %lf\t%lf\t%lf" % (order['orderId'], price, origQty, executedQty))
#
#             TARGET_PROFITABLE_PRICE = None
#             ORDER_ID = 0
#
#             if not TEST_MODE:
#                 ret = client.sell_limit(symbol, quantity, TARGET_PRICE)
#                 print('Sales were made at %s price.' % (TARGET_PRICE))
#                 print('---------------------------------------------')
#
#                 if 'msg' in ret:
#                     errexit(ret['msg'])
#
#                 print(ret)
#             else:
#                 print("Order Id: %s. The test order is complete. Price %s" % (orderId, TARGET_PRICE))

#
# def sell(symbol, quantity, target_price):
#     ret = client.sell_limit(symbol, quantity, target_price)
#     print('Sales were made at %s price.' % (target_price))
#     print('---------------------------------------------')
#
#     if 'msg' in ret:
#         errexit(ret['msg'])


# def cancel_order(symbol, orderId):
#     global TEST_MODE
#
#     if orderId is not None:
#
#         if not TEST_MODE:
#             ret = client.cancel(symbol, orderId)
#             if 'msg' in ret:
#                 errexit(ret['msg'])
#
#         print('Order has been canceled.')


# def check_order(symbol, orderId):
#     ret = client.query_order(symbol, orderId)
#     if 'msg' in ret:
#         errexit(ret['msg'])
#
#     # Canceled Filled Partial Fill
#     if ret['status'] != "CANCELED":
#         # if ret['status'] != "NEW":
#         print("%s Order completed. Try sell..." % (orderId))
#         return True
#     print("%s Order is open..." % (orderId))
#     return False

#
# def get_ticker(symbol):
#     ret = client.get_ticker(symbol)
#     return float(ret["lastPrice"])
#

def errexit(msg):
    print("Error: " + msg)
    exit(1)

#
# def action(symbol):
#     global ORDER_ID
#     global QUANTITY
#     global TARGET_PRICE
#     global TARGET_PROFITABLE_PRICE
#
#     file = open("ORDER", "r")
#     # print file.read()
#
#     lastPrice = get_ticker(symbol)
#
#     ret = client.get_orderbooks(symbol, 5)
#     lastBid = float(ret['bids'][0][0])  # last buy price
#     lastAsk = float(ret['asks'][0][0])  # last sell price
#
#     btcPrice = get_ticker("BTCUSDT")
#     buyPrice = lastBid + option.increasing  # target buy price
#     sellPrice = lastAsk - option.decreasing  # target sell price
#
#     profitablePrice = buyPrice + (buyPrice * PROFIT / 100)  # spread
#     currentProfit = buyPrice + (buyPrice * PROFIT / 100)  # spread
#
#     earnTotal = sellPrice - buyPrice
#
#     TARGET_PRICE = sellPrice
#
#     if ORDER_ID is 0:
#
#         print('price:%.8f buyp:%.8f sellp:%.8f-bid:%.8f ask:%.8f BTC:$%.1f profit price:%.8f' % (
#         lastPrice, buyPrice, sellPrice, lastBid, lastAsk, btcPrice, profitablePrice))
#
#         # Did profit get caught
#         if lastAsk >= profitablePrice:
#
#             TARGET_PROFITABLE_PRICE = profitablePrice
#
#             ORDER_ID = buy_limit(symbol, QUANTITY, buyPrice)
#
#             print("Percentage of %s profit. Order created from %.8f. Profit: %.8f BTC" % (PROFIT, sellPrice, earnTotal))
#             print("#####################")
#
#         else:
#
#             TARGET_PROFITABLE_PRICE = None
#
#     else:
#
#         # If the order is complete, try to sell it.
#         if check_order(symbol, ORDER_ID):
#
#             # Did profit get caught
#             if lastAsk >= TARGET_PROFITABLE_PRICE:
#
#                 print("Target sell price: %.8f " % TARGET_PROFITABLE_PRICE)
#
#                 sell_limit(symbol, QUANTITY, ORDER_ID)
#
#             # if the profit is lost, cancel order
#             else:
#
#                 print("%s Cancel order" % (ORDER_ID))
#
#                 cancel_order(symbol, ORDER_ID)
#
#                 # Reset order
#                 ORDER_ID = None
#                 # empty ORDER file
#                 write(" ")


def pump_action(symbol, target_profit_increase, exchange):
    # if exchange == "binance":
    #     market = ccxt.binance({
    #         'api_key': Config.binance_api_key,
    #         'secret': Config.binance_api_secret
    #     })
    # if exchange == "cryptopia":
    #     market = ccxt.cryptopia({
    #         'api_key': Config.cryptopia_api_key,
    #         'secret': Config.cryptopia_secret
    #     })
    # if exchange == "hitbtc":
    #     market = ccxt.hitbtc({
    #         'api_key': Config.hitbtc_api_key,
    #         'secret': Config.hitbtc_secret
    #     })
    market = ""
    current_buy_price = exchange.fetch_ticker(symbol)["bid"]
    target_profit_price = current_buy_price + (current_buy_price * target_profit_increase) / 100
    cost = market.create_limit_buy_order(symbol, [["amount", option.quantity], ["buy", current_buy_price*2]])['cost']
    while True:
        start_time = time.time()
        # check_profit(symbol, current_buy_price, target_profit_price)
        end_time = time.time()
        if end_time - start_time < WAIT_TIME:
            time.sleep(WAIT_TIME - (end_time - start_time))
#
#
# def monitor_pump(symbol, buy_price, target_profit_price):
#
#     min_profit_met = False
#     ret = client.get_orderbooks(symbol, 5)
#     last_ask = float(ret['asks'][0][0])  # last sell price
#     price_change = last_ask - buy_price
#     total_percent_change = (price_change / buy_price) * 100
#     current_profit_price = last_ask + (last_ask * total_percent_change / 100)  # spread
#     current_profit_percent = buy_price * total_percent_change
#     print("Buy Price: %.8f , Last Ask: %.8f, Price Change: %.8f" % (buy_price, last_ask, price_change))
#     if total_percent_change >= option.profit - 5:
#         sell(symbol, option.quantity, last_ask)
#     if total_percent_change >= 25:
#         min_profit_met = True
#     if min_profit_met:
#         if total_percent_change <= 20:
#             sell(symbol, option.quantity, last_ask)
#     else:
#         if total_percent_change <= -1:
#             sell(symbol, option.quantity, last_ask)
#
# def check_profit(symbol, buy_price):
#     global LAST_PROFIT_PCT_HIT
#     ret = client.get_orderbooks(symbol, 1)
#     last_ask = float(ret['asks'][0][0])  # last sell price
#     price_change = last_ask - buy_price
#     total_percent_change = (price_change / buy_price) * 100
#     interval_percent_change = total_percent_change // 50
#     if total_percent_change >= option.profit:
#         sell(symbol, option.quantity, last_ask)
#     else:
#         for x in range(0, 30, 1):
#             if interval_percent_change == x:
#                 LAST_PROFIT_PCT_HIT = x
#             else:
#                 if LAST_PROFIT_PCT_HIT < (x - 3):
#                     sell(symbol, option.quantity, last_ask)
#

def buy_and_set_sell(symbol, market, amount):
    last_tick = market.fetch_ticker(market, symbol)
    last_bid = last_tick['bid']
    last_ask = last_tick['ask']
    order = market.create_limit_buy_order(market, ({
        'symbol': symbol,
        'price': last_bid*2,
        'amount': amount
    }))

    sell_price = 0.0;
    while True:
        order_sold = False
        order_status = market.fetch_order_status(order['id'])
        if order_status == "FILLED":
            last_ask = market.fetch_ticker(market, symbol)['ask']
            sell_order = market.create_limit_sell_order(market, {
                'symbol': symbol,
                'price': last_ask * 8,
                'amount': amount
            })
            sell_price = sell_order['price']
            break
    # while True:
    #     last_ask = market.fetch_ticker(market, symbol)['ask']
    #     sell_order_status = market.fetch_order_status(order[sell_order['id']])
    #     if sell_order['status'] != 'FILLED' & last_ask < sell_price:


def monitor_price(symbol, exchange):
    if exchange == "binance":
        market = ccxt.binance({
            'api_key': 'bLt8i8ah7z5OIhPcjW9XNISudKLWcQ4PxdWSLfK57r1Z1iEz8h4I8kwFSMgwLJR3',
            'secret': 'mtKjfWoSP88Y8isnYFHvpgm2TLvOXl0lOdOHiSfnvvvc3hfa4nlsBk9HQ5auD4f6'
        })
    if exchange == "cryptopia":
        market = ccxt.cryptopia({
            'api_key': '4303ea93de0c4c64af6abf2e35e72fd7',
            'secret': 'QuWSpBhV+xE352/6mSVImzaV1APCu2fP2LYOyPhBFVk='
        })
    if exchange == "hitbtc":
        market = ccxt.hitbtc({
            'api_key': 'd332ac0c7ca9efb4798a389719d64eaf',
            'secret': "daa9b1d96b520b39cedbaefb1cbca34a"
        })
    while True:
        tick = market.fetch_ticker(symbol)
        print("Time: %s , Symbol: %s, Last Ask: %.8f, Last Bid: %.8f, High: %.8f, Low: %.8f" % (str(tick["datetime"]), symbol, tick['ask'], tick['bid'], tick['high'], tick['low']))


def main():
    symbol = option.symbol

    print(" Enter your symbol. Ex: %s" % symbol)

    name = input()

    if name != "":
        symbol = name
    if option.monitor:
        monitor_price(option.symbol, option.exchange)
    if option.pump:
        buy_and_set_sell(option.symbol, option.exchange, option.amount)
        # pump_action(option.symbol, option.profit)

    print("trader.py --quantity %s --symbol %s --profit %s --wait_time %s --orderid %s \n" % (
    option.quantity, symbol, option.profit, option.wait_time, option.orderid))

    print('%%%s profit scanning for %s \n' % (PROFIT, symbol))

    if TEST_MODE:
        print("Test mode active")

    while True:

        startTime = time.time()
        # action(symbol)
        endTime = time.time()

        if endTime - startTime < WAIT_TIME:
            time.sleep(WAIT_TIME - (endTime - startTime))


if __name__ == "__main__":
    main()