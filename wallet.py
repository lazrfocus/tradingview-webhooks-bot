import os
import subprocess
import asyncio
import ccxt.async_support as ccxt
import api_keys
import generic_functions as func
from prettytable import PrettyTable

myBalance = None

async def get_balance():
    global myBalance

    bybit = ccxt.bybit({
        'apiKey': api_keys.BYBIT_KEY,
        'secret': api_keys.BYBIT_SECRET,
        'enableRateLimit': True,
        # "proxy": "https://cors-anywhere.herokuapp.com/",   ##TODO: create cors vpn
        # "origin": "bitstamp"
    })
    try:
        myBalance = await bybit.fetch_balance()
#        print(myBalance)
    except:
        print('error')
    
    await bybit.close()  # don't forget to close it when you're done

def print_balance():
    global myBalance
    balanceTable = PrettyTable()
#    totalUSD = 0
    if myBalance != None:
        if myBalance['info']['ret_msg'] == 'OK':
#            print(myBalance)
            print('\033[1m','Coin','\033[0m', 'Total','     | ','Free', '      | ', 'USD Value','\x1b[0m')
            #if abs(float(myBalance['USDT']['total'])) > 0.01:
            balanceTable.field_names = ["Coin", "Total", "Free", "USD Value"]
            balanceTable.add_row(['USDT', round(float(myBalance['USDT']['total']),2), round(float(myBalance['USDT']['free']),2), round(float(myBalance['USDT']['total']),2)])
            balanceTable.add_row(['ETH', round(float(myBalance['ETH']['total']),2), round(float(myBalance['ETH']['free']),2), round(float(myBalance['ETH']['total']),2)])

#            totalUSD = totalUSD + float(i['usdValue'])
        else:
            pass
#        balanceTable.add_row(["Total USD", "","", round(totalUSD,2)])
        print(balanceTable)
        
    return True

if __name__ == '__main__':
    
    try:
        while True:
            asyncio.new_event_loop().run_until_complete(get_balance())
            subprocess.call('clear', shell=True)
            func.print_time()
            print_balance()
#            func.print_ping() #bybit doesnt let you print
            #time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        
