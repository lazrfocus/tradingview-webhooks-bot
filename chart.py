# -*- coding: utf-8 -*-

import os
import sys

from asciichartpy import plot

# -----------------------------------------------------------------------------

this_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(os.path.dirname(this_folder))
sys.path.append(root_folder + '/python')
sys.path.append(this_folder)

# -----------------------------------------------------------------------------

import ccxt  # noqa: E402

# -----------------------------------------------------------------------------

ftx = ccxt.ftx()
#coinbasepro = ccxt.coinbasepro()

symbol = 'DOGE-PERP'

# each ohlcv candle is a list of [ timestamp, open, high, low, close, volume ]
index = 4  # use close price from each ohlcv candle


def print_chart(exchange, symbol, timeframe):

    print("\n" + exchange.name + ' ' + symbol + ' ' + timeframe + ' chart:')

    # get a list of ohlcv candles
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

    # get the ohlCv (closing price, index == 4)
    series = [x[index] for x in ohlcv]

    # print the chart
    print("\n" + plot(series[-120:], {'height': 20, 'format':'{:8.4f}'}))

    last = ohlcv[len(ohlcv) - 1][index]  # last closing price
    return last


last = print_chart(ftx, 'DOGE-PERP', '1m')
print("\n" + symbol + "= $" + str(last) + "\n")  # print last closing price

#last = print_chart(coinbasepro, 'BTC/USD', '1h')
#print("\n" + coinbasepro.name + " ₿ = $" + str(last) + "\n")  # print last closing price