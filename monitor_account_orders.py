import subprocess
from ftx import ThreadedWebsocketManager
import api_keys
import subprocess
import generic_functions as func
import os

API = api_keys.FTX_KEY
SECRET = api_keys.FTX_SECRET

symbol = 'BTC-PERP'

def on_fill(payload):
    # print(payload)
    
    try:
        if payload['channel'] == 'fills':
            if payload['type'] == 'update':
                print("Fill: ", payload['data']['market'], payload['data']['side'], 'Price: ', round(float(payload['data']['price']),4), 'QTY: ', round(float(payload['data']['size']),4), 'Fee: $', round(float(payload['data']['fee']),4),  payload['data']['liquidity'], '       ', payload['data']['time'])
    except:
        pass
    
    # return rollingliquidations

def on_order(payload):
    #print(payload)
    if payload['channel'] == 'orders':
        if payload['type'] == 'update':
            if payload['data']['status'] == 'closed':
                print("Closed Order: ", payload['data']['market'], payload['data']['side'], 'Price: ', round(float(payload['data']['price']),4), 'QTY: ', round(float(payload['data']['size']),4), 'id: ', payload['data']['id'], '     ', payload['data']['createdAt'])
            else:
                print("New Order: ", payload['data']['market'], payload['data']['side'], 'Price: ', round(float(payload['data']['price']),4), 'QTY: ', round(float(payload['data']['size']),4), 'id: ', payload['data']['id'], '     ', payload['data']['createdAt'])

def subscribe_fills():
    wsm = ThreadedWebsocketManager(API, SECRET)
    wsm.start()
    socket_fills="fills_socket"
    socket_orders="orders_socket"
    wsm.start_socket(on_fill, socket_name=socket_fills)
    wsm.login(socket_name=socket_fills)
    wsm.subscribe(socket_fills, channel="fills", op="subscribe")
    wsm.start_socket(on_order, socket_name=socket_orders)
    wsm.login(socket_name=socket_orders)
    wsm.subscribe(socket_orders, channel="orders", op="subscribe")
if __name__ == '__main__':
    subprocess.call('clear', shell=True)            
    
    try:
        subscribe_fills()
    
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        