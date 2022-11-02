import subprocess
from ftx import ThreadedWebsocketManager
import api_keys
import subprocess
import generic_functions as func

API = api_keys.FTX_KEY
SECRET = api_keys.FTX_SECRET

symbol = 'DOGE-PERP'

rollingliquidations = 0

def on_trade(payload):
    global rollingliquidations
    # print(payload['channel'])
    setactive=0
    if payload['channel'] == 'trades':
        if payload['type'] == 'update':
            for i in payload['data']:
                # print(i)
                # print(bool(i['liquidation']))
                if bool(i['liquidation']):
                    print(i['time'], "     |  ", i['size'], "   ", i['price'])
                    rollingliquidations = float(i['size'])+rollingliquidations
                    setactive=1
                else:
                    if setactive:
                        print("Liquidations since start: ", round(rollingliquidations),2)
                        setactive=0

def subscribe_trades(symbol):
    wsm = ThreadedWebsocketManager(API, SECRET)
    wsm.start()
    name = 'market_connection'
    wsm.start_socket(on_trade, socket_name=name)
    wsm.subscribe(name, channel="trades", op="subscribe", market=symbol)

if __name__ == '__main__':
    subprocess.call('clear', shell=True)            
    
    try:
        subscribe_trades(symbol)
    
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        