import os
import subprocess
import asyncio
import ccxt.async_support as ccxt
import api_keys
import generic_functions as func

myPositions = None

async def get_positions():
    global myPositions

    ftx = ccxt.ftx({
        'apiKey': api_keys.FTX_KEY,
        'secret': api_keys.FTX_SECRET,
        'enableRateLimit': True,
        # "proxy": "https://cors-anywhere.herokuapp.com/",   ##TODO: create cors vpn
        # "origin": "bitstamp"
    })
    
    try:
        myPositions = await ftx.fetch_positions()
    except:
        print('error')
    
    await ftx.close()  # don't forget to close it when you're done

def print_positions():
    global myPositions
    
    for i in myPositions:
        if i['info']['recentPnl'] != None:
            if (i['info']['side']) == 'buy':
                if float((i['info']['recentPnl'])) >=0: 
                    print('\033[1m',i['info']['side'], i['info']['future'],'\033[0m',' | ', str(i['info']['size']), ' | ', '\x1b[0;32;40m', round(float((i['info']['recentPnl'])),2),'\x1b[0m')
                else:
                    print('\033[1m',i['info']['side'], i['info']['future'],'\033[0m',' | ', str(i['info']['size']), ' | ', '\x1b[0;31;40m', round(float((i['info']['recentPnl'])),2),'\x1b[0m')
            elif (i['info']['side']) == 'sell':
                print(i['info']['side'] + ' ' + i['info']['future'] + ' ' + str(i['info']['size']), round(float((i['info']['recentPnl'])),2))
            else:
                pass
        else:
            pass
    
    return True

if __name__ == '__main__':
    
    try:
        while True:
            asyncio.new_event_loop().run_until_complete(get_positions())
            subprocess.call('clear', shell=True)
            func.print_time()
            print_positions()
            func.print_ping()

            #time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        