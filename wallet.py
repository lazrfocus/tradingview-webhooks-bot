import os
import subprocess
import asyncio
import ccxt.async_support as ccxt
import api_keys
import generic_functions as func

myBalance = None

async def get_balance():
    global myBalance

    ftx = ccxt.ftx({
        'apiKey': api_keys.FTX_KEY,
        'secret': api_keys.FTX_SECRET,
        'enableRateLimit': True,
        # "proxy": "https://cors-anywhere.herokuapp.com/",   ##TODO: create cors vpn
        # "origin": "bitstamp"
    })
    try:
        myBalance = await ftx.fetch_balance()
    except:
        print('error')
    
    await ftx.close()  # don't forget to close it when you're done

def print_balance():
    global myBalance

    if myBalance != None:
        print('\033[1m','Coin','\033[0m', 'Total',' | ','Free', ' | ', 'USD Value','\x1b[0m')
        for i in myBalance['info']['result']:
            if abs(float(i['total'])) > 0.01:
                print('\033[1m',i['coin'],'\033[0m', round(float(i['total']),2),' | ',round(float(i['free']),2), ' | ', round(float(i['usdValue']),2),'\x1b[0m')
        else:
            pass
    
    return True

if __name__ == '__main__':
    
    try:
        while True:
            asyncio.new_event_loop().run_until_complete(get_balance())
            subprocess.call('clear', shell=True)
            func.print_time()
            print_balance()
            func.print_ping()
            #time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        