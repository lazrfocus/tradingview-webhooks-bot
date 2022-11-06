import subprocess
import ccxt
import asyncio
#import ccxt.async_support as ccxt
import api_keys
import subprocess
import generic_functions as func
import os
import time

ftx = ccxt.ftx({
    'apiKey': api_keys.FTX_KEY,
    'secret': api_keys.FTX_SECRET,
    'enableRateLimit': True,
})

ftx.load_markets()
balanceUSDfree = None
balanceETHfree = None
balanceETHfreeInUSD = None
balanceTotalFree = None
obLastBid = None
obLastAsk = None

def get_balance():
    global balanceUSDfree, balanceETHfree, balanceETHfreeInUSD, balanceTotalFree, ftx
    
    try:
        balanceETHfree = ftx.fetch_partial_balance('ETH')['free']
    except:
        pass
    try:
        balanceUSDfree = ftx.fetch_partial_balance('USD')['free']
    except:
        pass
    try:
        ETHfreelastbidprice= ftx.fetch_ticker("ETH/USD")['bid']
    except:
        pass
    
    balanceETHfreeInUSD=balanceETHfree*ETHfreelastbidprice
    balanceTotalFree=balanceUSDfree+balanceETHfreeInUSD
    print('USDfreebalance: ', balanceUSDfree)
    print('ETHfreebalance: ', balanceETHfree)
    print('totalfreeBalance: ', balanceTotalFree)

def get_last_bid(ticker):
    global obLastBid
    
    try:
        obLastBid = ftx.fetch_ticker(ticker)['bid']
    except:
        pass

def place_limit_order(ticker, side, percentSize, price, reduceOnly, ioc, postOnly):
    global balanceTotalFree, obLastBid
    
    print('Placing order')
    
    size=round((balanceTotalFree*percentSize)/obLastBid, 4)
    print("QTY:", size,"   Lev. Cost: $", round(size*obLastBid,2), "   Cost: $",(size*obLastBid)/20)
    try:
        ftx.create_limit_order(ticker, side, size, price, {'reduceOnly': reduceOnly, 'ioc': ioc, 'postOnly': postOnly})
    except:
        print('Order failed')
        
def place_market_order(ticker, side, percentSize, reduceOnly, ioc, postOnly):
    print('Placing order')
    
def place_stop_order(ticker, side, percentSize, price, stopPrice, reduceOnly, ioc, postOnly):
    print('Placing order')
    ftx.fetch
    ftx.create_stop_limit_order(ticker, side, size, price, stopPrice, {'reduceOnly': reduceOnly, 'ioc': ioc, 'postOnly': postOnly})
    
if __name__ == '__main__':
    func.clear_sceen()
    try:
        while True:
            func.print_time()
            get_balance() ## adds a lot of latency
            get_last_bid("BTC-PERP") ##adds more latency
            place_limit_order("BTC-PERP", "buy", 0.1, 15000, False, False, False)
            #time.sleep(3)
        #ftx.create_limit_order("BTC-PERP", "buy", 0.001, 15000, {'reduceOnly': False, 'ioc': False, 'postOnly': False})
    
    
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        