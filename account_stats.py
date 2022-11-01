import os
import subprocess
import asyncio
import ccxt.async_support as ccxt
import api_keys
import generic_functions as func
import wallet
import pnl

if __name__ == '__main__':
    
    try:
        while True:
            asyncio.new_event_loop().run_until_complete(pnl.get_positions())
            asyncio.new_event_loop().run_until_complete(wallet.get_balance())
            subprocess.call('clear', shell=True)
            func.print_time()
            wallet.print_balance()
            print('--------------------------------')
            pnl.print_positions()
            func.print_ping()
            
    except KeyboardInterrupt:
        print('Interrupted')
        os._exit(0)
        