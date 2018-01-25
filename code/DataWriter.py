# Import
import os
import time
import argparse
import ccxt
import csv
import boto
import boto.s3
from boto.s3.key import Key

parser = argparse.ArgumentParser()
parser.add_argument("--exchange", type=str, help="Selected Exchange", default='binance')
parser.add_argument("--symbol", type=str, help="Selected Exchange", default='binance')
option = parser.parse_args()

WAIT_TIME = 1

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
    if exchange == "bittrex":
        return ccxt.cryptopia({
            "api_key": config['api_key'],
            "secret": config['secret']
        })


def process_tick(tick):
    symbol = option.symbol.replace('/', '-')
    directory = os.getcwd().replace('code', 'data')
    filename = str("%s\home-market-data\%s\%s.csv" % (directory, option.exchange, symbol))
    with open(filename, 'w') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"',  quoting=csv.QUOTE_ALL)
        names = list(tick)
        names.pop(names.index("info"))
        datawriter.writerow(names)
        values = list()
        for item in names:
            info = None
            if item == "info":
                break
                # for sub_item in tick[item]:
                #     item = str("info_%s" % sub_item)
            values.append(tick[item])
        datawriter.writerow(values)
    return 0


def action(exchange, symbol):
    tick = process_tick(exchange.fetch_ticker(symbol))
    symbol = option.symbol.replace('/', '-')
    directory = os.getcwd().replace('code', 'data')
    filename = str("%s\home-market-data\%s\%s.csv" % (directory, option.exchange, symbol))
    with open(filename, 'w') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        names = list(tick)
        names.pop(names.index("info"))
        datawriter.writerow(names)
        values = list()
        for item in names:
            info = None
            if item == "info":
                break
                # for sub_item in tick[item]:
                #     item = str("info_%s" % sub_item)
            values.append(tick[item])
        datawriter.writerow(values)
    return 0

def write_to_csv(csvfile, tick):
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
    names = list(tick)
    names.pop(names.index("info"))
    datawriter.writerow(names)
    values = list()
    for item in names:
        info = None
        if item == "info":
            break
            # for sub_item in tick[item]:
            #     item = str("info_%s" % sub_item)
        values.append(tick[item])
    datawriter.writerow(values)


def main():
    symbol = option.symbol
    exchange = get_exchange(option.exchange)
    symbol = option.symbol.replace('/', '-')
    directory = os.getcwd().replace('code', 'data')
    filename = str("%s\home-market-data\%s\%s.csv" % (directory, option.exchange, symbol))
    with open(filename, 'w') as csvfile:
        while True:
            tick = exchange.fetch_ticker(option.symbol)
            write_to_csv(csvfile, tick)


if __name__ == "__main__":
    main()