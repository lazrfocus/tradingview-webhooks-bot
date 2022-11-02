# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from ftx import ThreadedWebsocketManager
import api_keys
import asyncio

from asciichartpy import plot

API = api_keys.FTX_KEY
SECRET = api_keys.FTX_SECRET

symbol = 'DOGE-PERP'
priceArray = []
bidArray = []
askArray = []

def print_chart():
    global priceArray
    global askArray
    global bidArray
    subprocess.call('clear', shell=True)            
    print("\n" + plot([priceArray, askArray, bidArray], {'height': 8, 'format':'{:8.4f}'}),)
    print("\n" + symbol + "= $" + str(priceArray[-1]))  # print last closing price            
    print("\n", round((askArray[-1]-bidArray[-1])/((askArray[-1]+bidArray[-1])/2)*100,4),"%" + " spread")

def on_read(payload):
    global priceArray
    global askArray
    global bidArray
    # print(payload.keys())
    if payload['channel'] == 'ticker':
        if payload['type'] == 'update':
            priceArray.append(payload['data']['last'])
            if len(priceArray)>140:
                priceArray.pop(0)
            askArray.append(payload['data']['ask'])
            if len(askArray)>140:
                askArray.pop(0)
            bidArray.append(payload['data']['bid'])
            if len(bidArray)>140:
                bidArray.pop(0)
            print_chart()    

if __name__ == '__main__':
    
    wsm = ThreadedWebsocketManager(API, SECRET)
    wsm.start()
    name = 'market_connection'
    wsm.start_socket(on_read, socket_name=name)
    wsm.subscribe(name, channel="ticker", op="subscribe", market=symbol)

    # try:
    #     while True:
    #         # asyncio.new_event_loop().run_until_complete(get_ohlc(ftx, 'DOGE-PERP', '1m'))

    #         # print_chart()
    #         # asyncio.run(fetch_ticker('DOGE-PERP'))
    #         exchange = ccxt.ftx()
    #         orderbook = await exchange.
    #         now = exchange.milliseconds()
    #         print(exchange.iso8601(now), symbol, orderbook['asks'][0], orderbook['bids'][0])
    #     # except Exception as e:
    #     #     print(str(e))
    #     #     #raise e  # uncomment to break all loops in case of an error in any one of them
    #     #     break  # you can also break just this one loop if it fails
            
            

    # except KeyboardInterrupt:
    #     print('Interrupted')
    #     os._exit(0)
        



# async def fetch_ticker(symbol):
#     # you can set enableRateLimit = True to enable the built-in rate limiter
#     # this way you request rate will never hit the limit of an exchange
#     # the library will throttle your requests to avoid that
#     global priceArray
#     exchange = ccxt.ftx()
#     while True:
#         # print('--------------------------------------------------------------')
#         # print(exchange.iso8601(exchange.milliseconds()), 'fetching', symbol, 'ticker from', exchange.name)
#         # this can be any call instead of fetch_ticker, really
#         try:
#             ticker = await exchange.fetch_ticker(symbol)
#             # print(exchange.iso8601(exchange.milliseconds()), 'fetched', symbol, 'ticker from', exchange.name)
#             #print(ticker)
#             #print(ticker['info']['last'])
#             priceArray.append(float(ticker['info']['last']))
#             if len(priceArray) > 200:
#                 priceArray.pop(0)
#             # print(priceArray)
#             print_chart()

#         except ccxt.RequestTimeout as e:
#             print('[' + type(e).__name__ + ']')
#             print(str(e)[0:200])
#             # will retry
#         except ccxt.DDoSProtection as e:
#             print('[' + type(e).__name__ + ']')
#             print(str(e.args)[0:200])
#             # will retry
#         except ccxt.ExchangeNotAvailable as e:
#             print('[' + type(e).__name__ + ']')
#             print(str(e.args)[0:200])
#             # will retry
#         except ccxt.ExchangeError as e:
#             print('[' + type(e).__name__ + ']')
#             print(str(e)[0:200])
#             break  # won't retry

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
