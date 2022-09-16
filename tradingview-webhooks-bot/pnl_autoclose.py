import json
import subprocess
from subprocess import STDOUT, check_output
import os
import time
from datetime import datetime
import pytz
from pytz import timezone

positionsJSON = {}
positionsShortJSON = {}
date_format='%m/%d/%Y %H:%M:%S %Z'

percTP = 2
percStop = -1

while 1:
    totalPNL = 0 
    
    try:
        positionsJSON = json.loads(subprocess.check_output(['ftx','positions','--sort','pnl','--output','json'],stderr=STDOUT,timeout=8))
    except subprocess.TimeoutExpired:
    #except subprocess.CalledProcessError as e:
    #    print('read error')
        continue

    try:
        positionsShortJSON = json.loads(subprocess.check_output(['ftx','positions','-a','Short','--sort','pnl','--output','json'],stderr=STDOUT,timeout=8))
    except subprocess.TimeoutExpired:
        continue
    #except:
    #except subprocess.CalledProcessError as e:
    #    print('read error')
        continue

    os.system('clear')

    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    print(date.strftime(date_format),'\n')   
    
    for p in positionsJSON:
        totalPNL = (totalPNL + p['pnl'])
        percPNL= 100*(p['markPrice'] - p['averageOpenPrice'])/p['averageOpenPrice']
        if percPNL > percTP:
            try:
                json.loads(subprocess.check_output(['exlong',p['market'],'--output','json'],stderr=STDOUT,timeout=8))
            except:
                print('read error') 
        elif percPNL < percStop:
            try:
                json.loads(subprocess.check_output(['exlong',p['market'],'--output','json'],stderr=STDOUT,timeout=8))
            except:
                print('read error')
        elif percPNL < 0:
            try:
                print('\033[1m',p['market'],'\033[0m', ' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;31;40m', round(p['pnl'],2),' | ',round(percPNL,1),'%','\x1b[0m')
            except:
                print('error')
        else:
            try:
                print('\033[1m',p['market'],'\033[0m',' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;32;40m', round(p['pnl'],2),' | ', round(percPNL,1),'%','\x1b[0m')
            except:
                print('error')

    print('\nShorts:')

    for p in positionsShortJSON:
        percPNL=- 100*(p['markPrice'] - p['averageOpenPrice'])/p['averageOpenPrice']
        totalPNL = (totalPNL + p['pnl'])
        if percPNL > percTP:
            try:
                json.loads(subprocess.check_output(['exshort',p['market'],'--output','json'],stderr=STDOUT,timeout=8))
            except:
                print('read error') 
        elif percPNL < percStop:
            try:
                json.loads(subprocess.check_output(['exshort',p['market'],'--output','json'],stderr=STDOUT,timeout=8))
            except:
                print('read error')
        elif percPNL < 0:
            try:
                print('\033[1m',p['market'],'\033[0m', ' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;31;40m', round(p['pnl'],2),' | ',round(percPNL,1),'%','\x1b[0m')
            except:
                print('error')
        else:
            try:
                print('\033[1m',p['market'],'\033[0m',' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;32;40m', round(p['pnl'],2),' | ', round(percPNL,1),'%','\x1b[0m')
            except:
                print('error')
#    try:
#        positionsShortJSON = json.loads(subprocess.check_output(['ftx','positions','-a','Short','--sort','pnl','--output','json'],stderr=STDOUT,timeout=8))
#    except:
#        print('read error') 
#    
#    os.system('clear')
#
#    date = datetime.now(tz=pytz.utc)
#    date = date.astimezone(timezone('US/Pacific'))
#    print(date.strftime(date_format),'\n')   
#    
#    for p in positionsJSON:
#        totalPNL = totalPNL + p['pnl']
#        if p['pnl']<0:
#            print('\033[1m',p['market'],'\033[0m',' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;31;40m', round(p['pnl'],3),'\x1b[0m')
#        else:
#            print('\033[1m',p['market'],'\033[0m',' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;32;40m', round(p['pnl'],3),'\x1b[0m')
#
#    print('\nShorts:')
#
#    for p in positionsShortJSON:
#        totalPNL = totalPNL + p['pnl']
#        if p['pnl']<0:
#            print('\033[1m',p['market'],'\033[0m', ' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;31;40m', round(p['pnl'],3),'\x1b[0m')
#        else:
#            print('\033[1m',p['market'],'\033[0m',' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;32;40m', round(p['pnl'],3),'\x1b[0m')
#
    print('\nTotal: $',round(totalPNL,2))

    time.sleep(1)
