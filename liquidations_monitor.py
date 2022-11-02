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

symbol = 'DOGE-PERP'

def on_rx_trade(payload):
    # print(payload['channel'])
    if payload['channel'] == 'trades':
        if payload['type'] == 'update':
            for i in payload['data']:
                # print(i)
                # print(bool(i['liquidation']))
                if bool(i['liquidation']):
                    print(i['time'], "     |  ", i['size'], "   ", i['time'])
                    # print("LIQUIDATION", payload['data']['side'], payload['data']['size'], payload['data']['price'], payload['data']['time'],'\n')
                # else:
                #     pass

def subscribe_trades(symbol):
    wsm = ThreadedWebsocketManager(API, SECRET)
    wsm.start()
    name = 'market_connection'
    wsm.start_socket(on_rx_trade, socket_name=name)
    wsm.subscribe(name, channel="trades", op="subscribe", market=symbol)

if __name__ == '__main__':
    subprocess.call('clear', shell=True)            
    
    try:
        subscribe_trades(symbol)
    
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        