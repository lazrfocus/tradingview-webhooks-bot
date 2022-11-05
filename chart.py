# -*- coding: utf-8 -*-
import subprocess
from ftx import ThreadedWebsocketManager
import api_keys
import subprocess
from asciichartpy import plot
import generic_functions as func
#from termgraph import CandleStickGraph

API = api_keys.FTX_KEY
SECRET = api_keys.FTX_SECRET

ticker = 'DOGE-PERP'
priceArray = []

def print_chart():
    global priceArray
    func.clear_sceen()
    print(plot(priceArray, {'height': 15, 'format':'{:8.4f}'}))


def on_read(payload):
    global priceArray

    if payload['channel'] == 'ticker':
        if payload['type'] == 'update':
            if len(priceArray) == 0:
                priceArray.append(payload['data']['last'])
                print_chart()
            elif priceArray[-1] != payload['data']['last']:
                priceArray.append(payload['data']['last'])
                print_chart()
            if len(priceArray)>140:
                priceArray.pop(0)

def subscribe_ticker(symbol):
    wsm = ThreadedWebsocketManager(API, SECRET)
    wsm.start()
    name = 'market_connection'
    wsm.start_socket(on_read, socket_name=name)
    wsm.subscribe(name, channel="ticker", op="subscribe", market=symbol)

if __name__ == '__main__':
    subprocess.call('clear', shell=True)            
    
    try:
        subscribe_ticker(ticker)
    

    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)