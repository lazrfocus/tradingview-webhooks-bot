import json
import subprocess
import os
import time
from datetime import datetime
import pytz
from pytz import timezone

positionsJSON = {}
positionsShortJSON = {}
date_format='%m/%d/%Y %H:%M:%S %Z'

##Main Account
#try:
#    positionsJSON = json.loads(subprocess.check_output(['ftx','positions','--sort','pnl','--output','json']))
#except subprocess.CalledProcessError as e:
#    print('error',format.(e.cmd),format(e.returncode),format(e.output))
#    print('read error')

date = datetime.now(tz=pytz.utc)
date = date.astimezone(timezone('US/Pacific'))
print(date.strftime(date_format),'\n')   

try:
    positionsShortJSON = json.loads(subprocess.check_output(['ftx','positions','-a','Short','--sort','pnl','--output','json']))
except subprocess.CalledProcessError as e:
    #print('error',format.(e.cmd),format(e.returncode),format(e.output))
    print('read error')

#for p in positionsJSON:
#    if p['side']=='sell':
#        positionClose = json.loads(subprocess.check_output(['exshort',p['market'],'100%','1']))

for p in positionsShortJSON:
    if p['side']=='sell':
 #       try:
        positionClose = subprocess.check_output(['ftx','trade','-a','Short','--market',p['market'],'--side','buy','--size','100%','--size-hook','position','--type','market'])
        print(positionClose)
#        
        #except:
#            print(positionClose)

