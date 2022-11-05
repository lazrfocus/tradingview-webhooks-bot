'''
Copyright (C) 2017-2022 Bryant Moscon - bmoscon@gmail.com
Please see the LICENSE file for the terms and conditions
associated with this software.
'''
from cryptofeed import FeedHandler
from cryptofeed.defines import ORDER_INFO, TRADES, FILLS
from cryptofeed.exchanges import FTX
from cryptofeed.types import Trade
from cryptofeed.types import OrderInfo
from cryptofeed.types import Fill
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
    print("Fill:", data.side, data.liquidity, data.symbol, data.price, data.amount, data.fee, data.id, data.order_id, data.timestamp)


async def order(data, receipt_timestamp):
    print("Order:",data.status, data.side, data.symbol, data.price, data.remaining, data.id, data.timestamp)
    

def main():
    
    ftx = FTX(config='config.yaml', subaccount='subaccount')
    f = FeedHandler(config="config.yaml")
    f.add_feed(FTX(config="config.yaml", symbols=['DOGE-USD-PERP'], channels=[FILLS, ORDER_INFO], callbacks={FILLS: fill, ORDER_INFO: order}), retries=-1)
    f.add_feed(FTX(config="config.yaml", symbols=['BTC-USD-PERP'], channels=[FILLS, ORDER_INFO], callbacks={FILLS: fill, ORDER_INFO: order}), retries=-1)
    f.add_feed(FTX(config="config.yaml", symbols=['ETH-USD-PERP'], channels=[FILLS, ORDER_INFO], callbacks={FILLS: fill, ORDER_INFO: order}), retries=-1)
    f.add_feed(FTX(config="config.yaml", symbols=['AXS-USD-PERP'], channels=[FILLS, ORDER_INFO], callbacks={FILLS: fill, ORDER_INFO: order}), retries=-1)
    f.add_feed(FTX(config="config.yaml", symbols=['ADA-USD-PERP'], channels=[FILLS, ORDER_INFO], callbacks={FILLS: fill, ORDER_INFO: order}), retries=-1)
    # calling f.add_feed more than once will create a parallel thread for each feed
    f.run()


if __name__ == '__main__':
    main()