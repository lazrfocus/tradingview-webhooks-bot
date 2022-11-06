'''
Copyright (C) 2017-2022 Bryant Moscon - bmoscon@gmail.com
Please see the LICENSE file for the terms and conditions
associated with this software.
'''
from cryptofeed import FeedHandler
from cryptofeed.defines import ORDER_INFO, TRADES, FILLS
from cryptofeed.exchanges import FTX
from cryptofeed.types import Trade
from cryptofeed.types import OrderInfo
from cryptofeed.types import Fill
import sqlite3

conn = sqlite3.connect('trades.db')

#Colors
colorRed = "\033[0;31;40m" #RED
colorGreen = "\033[0;32;40m" # GREEN
colorBold = "\033[1m"
colorReset = "\033[0m" # Reset

#async def trade(t, receipt_timestamp):
#    print(t)

async def fill(data, receipt_timestamp):
    insertDB_fill(conn, data)
    printDB_totalfees(conn)
    printDB_totalfills(conn)

async def order(data, receipt_timestamp):
    print(data)
    print("Order:",data.status, data.side, data.symbol, '@ $',data.price, 'QTY:', data.remaining, 'id:', data.id, '     ', data.timestamp)
    insertDB_order(conn, data)
    
def createDB(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE fills
                 (symbol text, side text, price real, amount real, fee real, liquidity text, id text, order_id text, timestamp text)''')
    c.execute('''CREATE TABLE orders
                 (symbol text, side text, status text, price real, amount real, id text, timestamp text)''')
    conn.commit()
    #conn.close()
    
def insertDB_fill(conn, data):
    c = conn.cursor()
    c.execute("INSERT INTO fills VALUES (?,?,?,?,?,?,?,?,?)", (data.symbol, data.side, float(data.price), float(data.amount), float(data.fee), data.liquidity, str(data.id), str(data.order_id), str(data.timestamp)))
    conn.commit()
    #conn.close()

def insertDB_order(conn, data):
    c = conn.cursor()
    if data.status == 'submitting':
        c.execute("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", (data.symbol, data.side, data.status, float(data.price), float(data.remaining), str(data.id), str(data.timestamp)))
    elif data.status == 'closed':
        c.execute("DELETE FROM orders WHERE id = ?", (str(data.id),))
    conn.commit()
    #conn.close()

def printDB_totalfees(conn):
    c = conn.cursor()
    c.execute("SELECT SUM(fee) FROM fills")
    totalfees = c.fetchone()[0]
    print(colorBold, 'total fees: $', round(totalfees,2), colorReset)

def printDB_totalfills(conn):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM fills")
    totalfills = c.fetchone()[0]
    print(colorBold, 'total fills: ', totalfills, colorReset)    
    
def delete_all_orders(conn):
    sql = 'DELETE FROM orders'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def fetch_open_orders():
    #TODO: fetch open orders from rest api
    return

def main():
    #create db file once then comment it out
    #createDB(conn)
    #clear orders for development
    delete_all_orders(conn)
    #fetch all open orders from rest api
    
    
    ftx = FTX(config='config.yaml', subaccount='subaccount')
    f = FeedHandler(config="config.yaml")
    
    #symbols only matters for trades channel
    # calling f.add_feed more than once will create a parallel thread for each feed
    f.add_feed(FTX(config="config.yaml", symbols=['BTC-USD-PERP'], channels=[FILLS], callbacks={FILLS: fill}), retries=-1)
    f.add_feed(FTX(config="config.yaml", symbols=['BTC-USD-PERP'], channels=[ORDER_INFO], callbacks={ORDER_INFO: order}), retries=-1)
    
    f.run()
    
if __name__ == '__main__':
    main()