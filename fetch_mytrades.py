## This script will fetch all your trades from FTX and save them to a csv file

import csv #pip3 install csv
import ccxt #pip3 install ccxt
import api_keys ##create a file in this directory called api_keys.py and add your api keys
##api_keys.py should look like this:
##FTX_KEY = 'yourkey'
##FTX_SECRET = 'yoursecret'

exchange = ccxt.ftx({
    'apiKey': api_keys.FTX_KEY,
    'secret': api_keys.FTX_SECRET,
    # "headers": {
    #     "FTX-SUBACCOUNT": "Short" #uncomment to use subaccount, otherwise fetches from main account
    # }

})

f = open('mytrades.csv', 'w')
writer = csv.writer(f)

markets = exchange.load_markets ()

all_results = {}
symbol = None
since = None
limit = 4900
end_time = exchange.milliseconds()

while True:
    print('-' * 80)
    params = {
        'end_time': int(end_time / 1000),
    }
    results = exchange.fetch_my_trades(symbol, since, limit, params)
    if len(results):
        first = results[0]
        last = results[len(results) - 1]
        end_time = first['timestamp']
        print('Fetched', len(results), 'trades from', first['datetime'], 'till', last['datetime'])
        fetched_new_results = False
        for result in results:
            if result['id'] not in all_results:
                fetched_new_results = True
                all_results[result['id']] = result
        if not fetched_new_results:
            print('Done')
            break
    else:
        print('Done')
        break


all_results = list(all_results.values())
all_results = exchange.sort_by(all_results, 'timestamp')

print('Fetched', len(all_results), 'trades')
writer.writerow(["#", "Market", "Size", "Price", "Fee", "Side", "Type", "Liquidity", "ID", "Order ID","Time"])
for i in range(0, len(all_results)):
    result = all_results[i]
    writer.writerow([i, result['info']['market'], result['info']['size'], result['info']['price'], result['info']['fee'], result['info']['side'], result['info']['type'], result['info']['liquidity'], result['info']['id'],result['info']['orderId'],result['info']['time']])
    
f.close()
print('Saved', len(all_results), 'trades to mytrades.csv')
print('-' * 80)
