"""
Tradingview-webhooks-bot is a python bot that works with tradingview's webhook alerts!
This bot is not affiliated with tradingview and was created by @robswc

You can follow development on github at: github.com/robswc/tradingview-webhook-bot

I'll include as much documentation here and on the repo's wiki!  I
expect to update this as much as possible to add features as they become available!
Until then, if you run into any bugs let me know!
"""

from actions import send_order, parse_webhook
from auth import get_token
from flask import Flask, request, abort

import time
import os
import subprocess
import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

from datetime import datetime
import pytz
from pytz import timezone
date_format='%H:%M:%S'
# Create Flask object called app.
app = Flask(__name__)


# Create root to easily let us know its on/working.
@app.route('/')
def root():
    return 'online'

def gettime():
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    date = date.strftime(date_format)
    return date

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Parse the string data from tradingview into a python dict
        data = parse_webhook(request.get_data(as_text=True))
	# Chec that the key is correct
        ticker=data['id']
        ticker=ticker[:-4]
        ticker=ticker+"-PERP"
        side=data['trade']
        if side=='long':
            side='b'
            time=gettime() 
            print('\a',time,'\033[33m' + 'Rcvd: long',ticker, data['percent']+'%','\033[39m')
            try:
                output = subprocess.check_output(['ftx','trade','--market',ticker,'--side',side,'--type','market', '--size', data['percent']+'%','--split',data['qty']],stderr=subprocess.STDOUT)
                time=gettime() 
                print('\033[32m',time,'Long', ticker,data['percent']+'%','\033[39m')
            except subprocess.CalledProcessError as e:
                time=gettime() 
                print('\033[31m',time,'Long', ticker,data['percent']+'%','\033[39m','error {} {} {} '.format(e.cmd,e.returncode,e.output))
            return '', 200
        elif side=='exlong':
            side='s'
            hook='position'           
            time=gettime() 
            print('\a','\033[33m',time,'Rcvd: exit long',ticker, data['percent']+'%','\033[39m')
            try:
                output=subprocess.check_output(['ftx','trade','--market',ticker,'--side',side,'--type','market', '--size', data['percent']+'%','--split',data['qty'],'--size-hook',hook,'--reduce-only'],stderr=subprocess.STDOUT)
                time=gettime() 
                print('\033[32m',time,'Exit Long', ticker,data['percent']+'%','\033[39m')
            except subprocess.CalledProcessError as e:
                time=gettime() 
                print('\033[31m',time,'Exit Long', ticker,data['percent']+'%','\033[39m','error {} {} {} '.format(e.cmd,e.returncode,e.output))
            return '', 200
        if side=='short':
            side='s'
            hook='default'
            time=gettime() 
            print('\a','\033[33m',time, 'Rcvd: short',ticker, data['percent']+'%','\033[39m')
            try:
                output=subprocess.check_output(['ftx','trade','-a','Short','--market',ticker,'--side',side,'--type','market', '--size', data['percent']+'%','--split',data['qty']],stderr=subprocess.STDOUT)
                time=gettime() 
                print('\033[32m',time,'Short',ticker,data['percent']+'%','\033[39m')
            except subprocess.CalledProcessError as e:
                time=gettime() 
                print('\033[31m',time,'Short',ticker,data['percent']+'%','\033[39m','error {} {} {} '.format(e.cmd,e.returncode,e.output))
            return '', 200
        elif side=='exshort':
            side='b'
            hook='position'           
            time=gettime() 
            print('\a','\033[33m',time,'Rcvd: exit short',ticker,data['percent']+'%','\033[39m')
            try:
                output=subprocess.check_output(['ftx','trade','-a','Short','--market',ticker,'--side',side,'--type','market', '--size', data['percent']+'%','--split',data['qty'],'--size-hook',hook,'--reduce-only'],stderr=subprocess.STDOUT)
                time=gettime() 
                print('\033[32m',time,'Exit Short', data['percent']+'%',ticker,'\033[39m')
            except subprocess.CalledProcessError as e:
                time=gettime() 
                print('\033[31m',time,'Exit Short',data['percent']+'%',ticker,'\033[39m','error {} {} {} '.format(e.cmd,e.returncode,e.output)) 
            return '', 200
        #subprocess.run(['ftx','trade','--market',ticker,'--side',side,'--type','market', '--size', data['percent']+'%','--split',data['qty'],'--size-hook',hook])
        return '', 200
    else:
        abort(400)


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000) #change port if needed here
