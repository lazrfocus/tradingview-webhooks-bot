import ccxt, time, random
ftx_keys = {
    'apiKey': 'test',
    'secret': 'test',
    'headers': {
        'ftx-subaccount' : 'test'
        }
}
ftx = ccxt.ftx(ftx_keys)

def refresh_order(order):
    updated_orders = ftx.fetch_orders()
    for updated_order in updated_orders:
        if updated_order["id"] == order["id"]:
            return updated_order
    print("Failed to find order {}".format(order["id"]))
    return None

ticker = "BTC-PERP"
#print(ex.fetch_markets())
#for i in ftx.fetch_markets():
#    print(i)    
tickers = ftx.fetch_tickers()
for symbol, ticker in tickers.items():
    print(
            symbol,
            ticker['datetime'],
            'ask: ' + str(ticker['ask']),
            'bid: ' + str(ticker['bid'])
    )
market = [mk for mk in ex.fetch_markets() if mk["symbol"] == ticker][0]
min_size = market["limits"]["amount"]["min"]

amount = 0.01
amount_traded = 0

# Initialise empty order and prices, preparing for loop
order = None
bid, ask = 0, 1e10

while amount - amount_traded > min_size:
    move = False
    ticker_data = ex.fetch_ticker(ticker)
    new_bid, new_ask = ticker_data['bid'], ticker_data['ask']

    if bid != new_bid:
        bid = new_bid

        # If an order exists then cancel it
        if order is not None:
            # cancel order
            try:
                ex.cancel_order(order["id"])
            except Exception as e:
                print(e)

            # refresh order details and track how much we got filled
            order = refresh_order(order)
            amount_traded += float(order["info"]["filledSize"])

            # Exit now if we're done!
            if amount - amount_traded < min_size:
                break

        # place order
        order = ex.create_limit_buy_order(ticker, amount, new_bid, {"postOnly": True})
        print("Buy {} {} at {}".format(amount, ticker, new_bid))
        time.sleep(random.random())

    # Even if the price has not moved, check how much we have filled.
    if order is not None:
        order = refresh_order(order)
        amount_traded += float(order["info"]["filledSize"])
    time.sleep(0.1)

print("Finished buying {} of {}".format(amount, ticker))
