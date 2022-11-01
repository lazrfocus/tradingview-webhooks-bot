#from ftx import Client
import os
import subprocess
import time
from datetime import datetime
import pytz
import pytz
from pytz import timezone
import asyncio
import ccxt.async_support as ccxt
import re

date_format='%m/%d/%Y %H:%M:%S %Z'
def print_time():
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    print(date.strftime(date_format))

def print_ping():
    ping_response = subprocess.Popen(["ping", "-c1", "ftx.com"], stdout=subprocess.PIPE).stdout.read()
    print(re.search(r'time=(\d+)',ping_response.decode(), re.MULTILINE).group(1) +' ms')

async def print_positions():
    ftx = ccxt.ftx({
        'apiKey': '' ,        
        'secret': '',
        'enableRateLimit': True,
        # "proxy": "https://cors-anywhere.herokuapp.com/",   ##TODO: create cors vpn
        # "origin": "bitstamp"
    })
    try:
        myPositions = await ftx.fetch_positions()
    except:
        print('error')
    
    # print(myPositions)
    await ftx.close()  # don't forget to close it when you're done
    subprocess.call('clear', shell=True)
    print_time()
    for i in myPositions:
        if i['info']['recentPnl'] != None:
            if (i['info']['side']) == 'buy':
                print(i['info']['side'] + ' ' + i['info']['future'] + ' ' + str(i['info']['size']), round(float((i['info']['recentPnl'])),2))
            elif (i['info']['side']) == 'sell':
                print(i['info']['side'] + ' ' + i['info']['future'] + ' ' + str(i['info']['size']), round(float((i['info']['recentPnl'])),2))
            else:
                pass
        else:
            pass
#    try:
#        print_ping()
#    except:
#        print('ping error')

    return True

if __name__ == '__main__':
    
    try:
        while True:
            asyncio.new_event_loop().run_until_complete(print_positions())

            time.sleep(1)
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        
    #

# while 1:
#     date = datetime.now(tz=pytz.utc)
#     date = date.astimezone(timezone('US/Pacific'))
#     print(date.strftime(date_format))
#     print('--------------------------------------------------------------')
#     print('Unrealized PNL: ',unrealizedPNL)
#     print('Collateral Used: ',collateralUsed)
#     print('Total PNL: ',unrealizedPNL+realizedPNL)
#     print('Lifetime Realized PNL: ',realizedPNL)
#     print('--------------------------------------------------------------')
    
#     realizedPNL = 0
#     unrealizedPNL = 0
#     collateralUsed = 0
    
#     try:
#         info = client.get_positions()
#         for i in info['result']:
#             #print(i)
#             realizedPNL=realizedPNL+float(i['realizedPnl'])
#             #print(float(i['size']))
#             if float(i['size'])>0:
#                 print('Long: ',i['future'],' ',i['size'],' ',i['cost'],' ',i['collateralUsed'],' ',i['openSize'],' ',i['entryPrice'],' ',i['unrealizedPnl'],' ',i['realizedPnl'],' ',i['estimatedLiquidationPrice'])
#                 unrealizedPNL = unrealizedPNL + float(i['unrealizedPnl'])
#                 collateralUsed = collateralUsed + float(i['collateralUsed'])
#             elif float(i['size'])<0:
#                 print('Short: ',i['future'],' ',i['size'],' ',i['cost'],' ',i['collateralUsed'],' ',i['openSize'],' ',i['entryPrice'],' ',i['unrealizedPnl'],' ',i['realizedPnl'],' ',i['estimatedLiquidationPrice'])
#                 unrealizedPNL = unrealizedPNL + float(i['unrealizedPnl'])
#                 collateralUsed = collateralUsed + float(i['collateralUsed'])

#     except:
#         print('Error')
    
#     time.sleep(1)

#     subprocess.call('clear', shell=True)



