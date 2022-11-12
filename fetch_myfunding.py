## This script will fetch all your funding payouts/payments from FTX and save them to a csv file

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
    #    "FTX-SUBACCOUNT": "Short" #uncomment to use subaccount, otherwise fetches from main account
    #}

})

all_results = {}
start_time = exchange.parse8601('2020-11-01T00:00:00Z')  # timestamp in milliseconds
end_time = exchange.milliseconds()

print('-' * 80)
request = {
'start_time': int(start_time / 1000),  # unix timestamp in seconds, optional
'end_time': int(end_time / 1000),  # unix timestamp in seconds, optional
# 'future': 'BTC-PERP',  # optional, otherwise return all futures
}

filename='myfunding.csv'
f = open(filename, 'w')
writer = csv.writer(f)

while True:
    
    response = exchange.private_get_funding_payments(request)
    results = exchange.safe_value(response, 'result', [])

    if len(results):
        first = results[0]
        last = results[len(results) - 1]
        end_time = first['time']
        print('Fetched', len(results), 'funding from', first['time'], 'till', last['time'])
        fetched_new_results = False
        for result in results:
            if result['id'] not in all_results:
                fetched_new_results = True
                all_results[result['id']] = result
                # print(result)
        new_end = exchange.parse8601(results[len(results)-1]['time'])

        request = {
            'start_time': int(start_time / 1000),  # unix timestamp in seconds, optional
            'end_time': int(new_end)/1000,  # unix timestamp in seconds, optional
        }
        if not fetched_new_results:
            print('Done')
            break
    else:
        print('Done')
        break

all_results = list(all_results.values())
all_results = exchange.sort_by(all_results, 'time')
print('Fetched', len(all_results), 'funding')

writer.writerow(["#","Market", "Payment", "Time", "Rate", "ID"])
for i in range(0, len(all_results)):
    result = all_results[i]
    writer.writerow([i, result['future'], result['payment'], result['time'], result['rate'], result['id']])

f.close()
print('Saved', len(all_results), 'funding to', filename)
print('-' * 80)
