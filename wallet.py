from ftx import Client
import os
import time
from datetime import datetime
import pytz
from pytz import timezone
API = "Z4SFREtdLmPpPC_AuzN2uNZwcZv1lRp8gtBZaUOo"
SECRET = "vIi-58XacD282GjZRB43usYrNLRib5ML8K_-mA41"

client = Client(API, SECRET)
#info = client.get_markets()
usdTotal = 0
ethTotal = 0
usdFree = 0
ethFree = 0
usdTotalLong = 0
ethTotalLong = 0
usdFreeLong = 0
ethFreeLong = 0
usdTotalShort = 0
ethTotalShort = 0
usdFreeShort = 0
ethFreeShort = 0

date_format='%m/%d/%Y %H:%M:%S %Z'

while 1:
    os.system('clear')
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    print(date.strftime(date_format))
    print(' Main: $',round(usdFreeLong,2),'($',round(usdTotalLong,2), ') |',round(ethFreeLong,5),'(',round(ethTotalLong,5),')')
    print('Short: $',round(usdFreeShort,2),'($',round(usdTotalShort,2), ') |',round(ethFreeShort,5),'(',round(ethTotalShort,5),')')
    print('--------------------------------------------------------------')
    print('Total: $',round(usdFree,2),'($',round(usdTotal,2), ') |',round(ethFree,5),'/(',round(ethTotal,5),')')


    usdTotalLong = 0
    ethTotalLong = 0
    usdFreeLong = 0
    ethFreeLong = 0
    usdTotalShort = 0
    ethTotalShort = 0
    usdFreeShort = 0
    ethFreeShort = 0
    
    try:
        info = client.get_all_balances()
        for i in info['result']['main']:
            if i['coin']=='USD':
                usdTotalLong = i['total']
                usdFreeLong = i['free']
            elif i['coin']=='ETH':
                ethTotalLong = i['total']
                ethFreeLong = i['free']
        for i in info['result']['Short']:
            if i['coin']=='USD':
                usdTotalShort = i['total']
                usdFreeShort = i['free']
            elif i['coin']=='ETH':
                ethTotalShort = i['total']
                ethFreeShort = i['free']
               #     print(i['coin'],round(i['total'],2),round(i['free'],2))
        ethTotal=ethTotalLong+ethTotalShort
        ethFree=ethFreeLong+ethFreeShort
        usdTotal=usdTotalLong+usdTotalShort
        usdFree=usdFreeLong+usdFreeShort
    except:
       print('error')

    time.sleep(1)
    os.system('clear')


