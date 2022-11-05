'''
Copyright (C) 2017-2022 Bryant Moscon - bmoscon@gmail.com
Please see the LICENSE file for the terms and conditions
associated with this software.
'''
from cryptofeed import FeedHandler
from cryptofeed.defines import ORDER_INFO, TRADES, FILLS
from cryptofeed.exchanges import FTX
import api_keys

api_keys.FTX_KEY
# Examples of some handlers for different updates. These currently don't do much.
# Handlers should conform to the patterns/signatures in callback.py
# Handlers can be normal methods/functions or async. The feedhandler is paused
# while the callbacks are being handled (unless they in turn await other functions or I/O)
# so they should be as lightweight as possible
async def trade(t, receipt_timestamp):
    print(t)


async def fill(data, receipt_timestamp):
    print(data)


async def order(data, receipt_timestamp):
    print(data)

def main():
    
    ftx = FTX(config='config.yaml', subaccount='subaccount')
    #print(ftx.ticker_sync('BTC-USD-PERP'))
    # print(ftx.orders_sync(symbol='BTC-USD-PERP'))
    f = FeedHandler(config="config.yaml")
    # print(ftx.symbols())
    #f.add_feed(FTX(config="config.yaml", subaccount='subaccount', symbols=['BTC-USD', 'BCH-USD', 'USDT-USD'], channels=[TRADES, FILLS, ORDER_INFO], callbacks={TRADES: trade, FILLS: fill, ORDER_INFO: order}))
    #f.add_feed(FTX(config="config.yaml", symbols=['BTC-USD-PERP', 'ADA-USD-PERP', 'ALGO-USD-PERP'], channels=[TRADES, FILLS, ORDER_INFO], callbacks={TRADES: trade, FILLS: fill, ORDER_INFO: order}))
    f.add_feed(FTX(config="config.yaml", symbols=['BTC-USD-PERP', 'ADA-USD-PERP', 'ALGO-USD-PERP','AXS-USD-PERP'], channels=[FILLS, ORDER_INFO], callbacks={TRADES: trade, FILLS: fill, ORDER_INFO: order}))
    # calling f.add_feed more than once will create a parallel thread for each feed
    f.run()


if __name__ == '__main__':
    main()