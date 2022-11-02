import subprocess
from ftx import ThreadedWebsocketManager
import api_keys
import subprocess
import generic_functions as func

API = api_keys.FTX_KEY
SECRET = api_keys.FTX_SECRET

symbol = 'DOGE-PERP'

orderbook = {}

def on_OBupdate(payload):
    # print(payload)
    # print(payload['channel'])
    # setactive=0
    if payload['channel'] == 'orderbook':
        if payload['type'] == 'update':
            for i in payload['data']['bids']:
                if i[1] == 0:
                    print(i[0],"bid removed")
                else:
                    print(i[0],"bid added")
                    orderbook[str(i[0])]=float(orderbook[i[0]])+float(i[1])
            for i in payload['data']['asks']:
                if i[1] == 0:
                    print(i[0],"ask removed")
                else:
                    print(i[0],"ask added")

    #             # print(bool(i['liquidation']))
    #             if bool(i['liquidation']):
    #                 print(i['time'], "     |  ", i['size'], "   ", i['price'])
    #                 rollingliquidations = float(i['size'])+rollingliquidations
    #                 setactive=1
    #             else:
    #                 if setactive:
    #                     print("Liquidations since start: ", round(rollingliquidations),2)
    #                     setactive=0

def subscribe_book(symbol):
    wsm = ThreadedWebsocketManager(API, SECRET)
    wsm.start()
    name = 'market_connection'
    wsm.start_socket(on_OBupdate, socket_name=name)
    wsm.subscribe(name, channel="orderbook", op="subscribe", market=symbol)

if __name__ == '__main__':
    subprocess.call('clear', shell=True)            
    
    try:
        subscribe_book(symbol)
        
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        