import os
import subprocess
import asyncio
import ccxt.async_support as ccxt
import api_keys
import generic_functions as func
from prettytable import PrettyTable
import colorama as ca

myPositions = None
ca.init(autoreset=False)

# #Color
colorRed = "\033[0;31;40m" #RED
colorGreen = "\033[0;32;40m" # GREEN
colorBold = "\033[1m"
colorReset = "\033[0m" # Reset

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
    
    await ftx.close()  # don't forget to close it when you're don
def print_positions():
    global myPositions
    pnlTable = PrettyTable()
    pnlTable.field_names = ["Position", "Ticker", "QTY", "Cost", "USD Value", "Entry", "Mark", "Liquidation", "PnL"]
    
    #print("Position  ", "Ticker  ", "     QTY  ", "     Cost  ", "USD Value  ", "Entry ", "Liquidation ", "PnL")
    for i in myPositions:
        if i['info']['recentPnl'] != None:
            # print(i)
            if (i['info']['side']) == 'buy':
                #if float((i['info']['recentPnl'])) >=0: 
                    #print(colorBold,"Long | ", i['info']['future'],colorReset,' | ', str(i['info']['size']), ' | ', round(float((i['info']['collateralUsed'])),1), ' | ', round(float((i['info']['cost'])),1), ' | ', round(float((i['info']['entryPrice'])),4), ' | ', round(float((i['info']['estimatedLiquidationPrice'])),4), ' | ', colorGreen, round(float((i['info']['recentPnl'])),2), colorReset)
                pnlTable.add_row(["Long", i['info']['future'], str(i['info']['size']), round(float((i['info']['collateralUsed'])),1), round(float((i['info']['cost'])),1), round(float((i['info']['entryPrice'])),4), round(float((i['info']['markPrice'])),4), round(float((i['estimatedLiquidationPrice'])),4), round(float((i['info']['recentPnl'])),2)])                #else:
                #    print(colorBold,"Long | ", i['info']['future'],colorReset,' | ', str(i['info']['size']), ' | ', round(float((i['info']['collateralUsed'])),1), ' | ', round(float((i['info']['cost'])),1), ' | ', round(float((i['info']['entryPrice'])),4), ' | ', round(float((i['info']['estimatedLiquidationPrice'])),4), ' | ', colorRed, round(float((i['info']['recentPnl'])),2), colorReset)
            elif (i['info']['side']) == 'sell':
                pnlTable.add_row(["Short", i['info']['future'], str(i['info']['size']), round(float((i['info']['collateralUsed'])),1), round(float((i['info']['cost'])),1), round(float((i['info']['entryPrice'])),4), round(float((i['info']['markPrice'])),4), round(float((i['estimatedLiquidationPrice'])),4), round(float((i['info']['recentPnl'])),2)])
                #if float((i['info']['recentPnl'])) >=0: 
                #    print(colorBold,"Short | ", i['info']['future'],colorReset,' | ', str(i['info']['size']), ' | ', round(float((i['info']['collateralUsed'])),1), ' | ', round(float((i['info']['cost'])),1), ' | ', round(float((i['info']['entryPrice'])),4), ' | ', round(float((i['info']['estimatedLiquidationPrice'])),4), ' | ', colorGreen, round(float((i['info']['recentPnl'])),2), colorReset)
                #else:
                #    print(colorBold,"Short | ", i['info']['future'],colorReset,' | ', str(i['info']['size']), ' | ', round(float((i['info']['collateralUsed'])),1), ' | ', round(float((i['info']['cost'])),1), ' | ', round(float((i['info']['entryPrice'])),4), ' | ', round(float((i['info']['estimatedLiquidationPrice'])),4), ' | ', colorRed, round(float((i['info']['recentPnl'])),2), colorReset)
            else:
                pass
        else:
            pass
    print(pnlTable)
    
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