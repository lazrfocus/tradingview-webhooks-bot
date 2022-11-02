# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import asyncio
import numpy as np

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

ohlcv = None
series = None

priceArray = []

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402

def print_chart():
    # print the chart
    # global ohlcv
    # global series
    global priceArray
    
    subprocess.call('clear', shell=True)            
    # print(plot(series, { 'height': 10 }))
    print("\n" + plot(priceArray[-200:], {'height': 40, 'format':'{:8.4f}'}))

    # last = ohlcv[len(ohlcv) - 1][index]  # last closing price
    print("\n" + symbol + "= $" + str(priceArray[-1]) + "\n")  # print last closing price            
    # return last

async def main(symbol):
    # you can set enableRateLimit = True to enable the built-in rate limiter
    # this way you request rate will never hit the limit of an exchange
    # the library will throttle your requests to avoid that
    global priceArray
    exchange = ccxt.ftx()
    while True:
        # print('--------------------------------------------------------------')
        # print(exchange.iso8601(exchange.milliseconds()), 'fetching', symbol, 'ticker from', exchange.name)
        # this can be any call instead of fetch_ticker, really
        try:
            ticker = await exchange.fetch_ticker(symbol)
            # print(exchange.iso8601(exchange.milliseconds()), 'fetched', symbol, 'ticker from', exchange.name)
            #print(ticker)
            #print(ticker['info']['last'])
            priceArray.append(float(ticker['info']['last']))
            if len(priceArray) > 200:
                priceArray.pop(0)
            # print(priceArray)
            print_chart()

        except ccxt.RequestTimeout as e:
            print('[' + type(e).__name__ + ']')
            print(str(e)[0:200])
            # will retry
        except ccxt.DDoSProtection as e:
            print('[' + type(e).__name__ + ']')
            print(str(e.args)[0:200])
            # will retry
        except ccxt.ExchangeNotAvailable as e:
            print('[' + type(e).__name__ + ']')
            print(str(e.args)[0:200])
            # will retry
        except ccxt.ExchangeError as e:
            print('[' + type(e).__name__ + ']')
            print(str(e)[0:200])
            break  # won't retry

# async def get_ohlc(exchange, symbol, timeframe):
#     global ohlcv
#     global series

#     # print("\n" + exchange.name + ' ' + symbol + ' ' + timeframe + ' chart:')

#     # get a list of ohlcv candles
#     try:
#         ohlcv = await exchange.fetch_ohlcv(symbol, timeframe)
#     except:
#         print('error')
    
#     await ftx.close()  # don't forget to close it when you're done
#     # get the ohlCv (closing price, index == 4)
#     series = [x[index] for x in ohlcv]

if __name__ == '__main__':
    
    try:
        while True:
            # asyncio.new_event_loop().run_until_complete(get_ohlc(ftx, 'DOGE-PERP', '1m'))

            # print_chart()
            asyncio.run(main('DOGE-PERP'))
            
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        

