import subprocess
from ftx import ThreadedWebsocketManager
import api_keys
import subprocess
import generic_functions as func
from decimal import Decimal
import time
import os

import requests
from order_book import OrderBook

API = api_keys.FTX_KEY
SECRET = api_keys.FTX_SECRET

symbol = 'DOGE-PERP'

# orderbook = {}
def test_orderbook_init():
    global ob
    ob = OrderBook(max_depth=10)
    #ob.bids = {{val: val for val in range(20)}}
    #ob.asks = {val: val for val in range(10, 30)}
    ob.bids = {}
    ob.asks = {}
    # assert len(ob) == 20

def on_OBupdate(payload):
    global ob
    if payload['channel'] == 'orderbook':
        if payload['type'] == 'update':
            for i in payload['data']['bids']:
                if i[1] == 0:
                    # print(i[0],"bid removed")
                    try:
                        del ob.bids[Decimal(i[0])]
                    except:
                        pass
                else:
                    # print(i[0],"bid added")
                    ob.bids[Decimal(i[0])] = Decimal(i[1])


            for i in payload['data']['asks']:
                if i[1] == 0:
                    # print(i[0],"ask removed")
                    try:
                        del ob.asks[Decimal(i[0])]
                    except:
                        pass
                else:
                    # print(i[0],"ask added")
                    ob.asks[Decimal(i[0])] = Decimal(i[1])

def getTopOrders(ob):
    # convert orderbook to dict
    topbid = None
    topask = None
    def convert(x):
        if isinstance(x, Decimal):
            return float(x)
        if isinstance(x, dict):
            return {k: float(v) for k, v in x.items()}
    ob_dict = ob.to_dict(to_type=convert)
    try:
        if topbid != float(list(ob_dict['bid'].keys())[0]):
            topbid=float(list(ob_dict['bid'].keys())[0])
            # print("First Bid   ", topbid)
        if topask != float(list(ob_dict['ask'].keys())[0]):
            topask=float(list(ob_dict['ask'].keys())[0])
            # print("First Ask   ", topask)

    except:
        pass

    return ob_dict, topbid, topask

def subscribe_book(symbol):
    wsm = ThreadedWebsocketManager(API, SECRET)
    wsm.start()
    name = 'market_connection'
    wsm.start_socket(on_OBupdate, socket_name=name)
    wsm.subscribe(name, channel="orderbook", op="subscribe", market=symbol)

if __name__ == '__main__':
    subprocess.call('clear', shell=True)            
    
    try:
        test_orderbook_init() 
        subscribe_book(symbol)

        while True:
            fullob, topbid, topask = getTopOrders(ob)
            print("First Bid   ", topbid)
            print("First Ask   ", topask)
            time.sleep(1)

        
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        