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
    
    #Get Long Positions
    try:
        positionsJSON = json.loads(subprocess.check_output(['ftx','positions','--sort','pnl','--output','json'],stderr=STDOUT,timeout=8))
    except subprocess.CalledProcessError as e:
        print(e.output)
        print("Error: ", e.returncode)
        time.sleep(1)
        continue
    except subprocess.TimeoutExpired as e:
        print("Timeout: ", e)
        time.sleep(1)
        continue
    except Exception as e:
        print("Error: ", e)
        time.sleep(1)
        continue
    
    #Get Short Positions
    try:
        positionsShortJSON = json.loads(subprocess.check_output(['ftx','positions','--sort','-pnl','--output','json'],stderr=STDOUT,timeout=8))
    except subprocess.CalledProcessError as e:
        print(e.output)
        print("Error: ", e.returncode)
        time.sleep(1)
        continue
    except subprocess.TimeoutExpired as e:
        print("Timeout: ", e)
        time.sleep(1)
        continue
    except Exception as e:
        print("Error: ", e)
        time.sleep(1)
        continue
    
    #Print system date for liveness check
    os.system('clear')
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    print(date.strftime(date_format),'\n')   
    
    for p in positionsJSON:
        totalPNL = (totalPNL + p['pnl'])
        percPNL= 100*(p['markPrice'] - p['averageOpenPrice'])/p['averageOpenPrice']

        try:
            if percPNL > percTP:
                output=json.loads(subprocess.check_output(['exlong',p['market'],'--output','json'],stderr=STDOUT,timeout=8))
            elif percPNL < percStop:
                output=json.loads(subprocess.check_output(['exlong',p['market'],'--output','json'],stderr=STDOUT,timeout=8))
            elif percPNL < 0:
                print('\033[1m',p['market'],'\033[0m', ' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;31;40m', round(p['pnl'],2),' | ',round(percPNL,1),'%','\x1b[0m')
            else:
                print('\033[1m',p['market'],'\033[0m',' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;32;40m', round(p['pnl'],2),' | ', round(percPNL,1),'%','\x1b[0m')
            print(output['message'])
        except subprocess.CalledProcessError as e:
            print(e.output)
            print("Error: ", e.returncode)
            time.sleep(1)
            continue
        except subprocess.TimeoutExpired as e:
            print("Timeout: ", e)
            time.sleep(1)
            continue
        except Exception as e:
            print("Error: ", e)
            time.sleep(1)
            continue
        
    print('\nShorts:')

    for p in positionsShortJSON:
        totalPNL = (totalPNL + p['pnl'])
        percPNL=- 100*(p['markPrice'] - p['averageOpenPrice'])/p['averageOpenPrice']
        
        try:
            if percPNL > percTP:
                output=json.loads(subprocess.check_output(['exshort',p['market'],'--output','json'],stderr=STDOUT,timeout=8))
            elif percPNL < percStop:
                output=json.loads(subprocess.check_output(['exshort',p['market'],'--output','json'],stderr=STDOUT,timeout=8))
            elif percPNL < 0:
                print('\033[1m',p['market'],'\033[0m', ' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;31;40m', round(p['pnl'],2),' | ',round(percPNL,1),'%','\x1b[0m')
            else:
                print('\033[1m',p['market'],'\033[0m',' | ', int(p['notionalSize']), ' | ', round(p['markPrice'],3), ' | ', round(p['averageOpenPrice'],3), ' | ', round(p['breakEvenPrice'],3), ' | ', round(p['estimatedLiquidationPrice'],3), ' | ', '\x1b[0;32;40m', round(p['pnl'],2),' | ', round(percPNL,1),'%','\x1b[0m')
            print(output['message'])
        except subprocess.CalledProcessError as e:
            print(e.output)
            print("Error: ", e.returncode)
            time.sleep(1)
            continue
        except subprocess.TimeoutExpired as e:
            print("Timeout: ", e)
            time.sleep(1)
            continue
        except Exception as e:
            print("Error: ", e)
            time.sleep(1)
            continue

    print('\nTotal: $',round(totalPNL,2))

    time.sleep(1)
