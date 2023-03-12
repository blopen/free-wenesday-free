<<<<<<< HEAD
import os

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
#import ccxt
api_key = 'vzY6b0n5qoUqo5srNn6LMSW2CLb8cXIgRstsKvdksKsZyxPq7A0eB6dcCtlKC9MQ'
secret_key = 'fD2PAd8K93FxesASG7rxKF29pBYKC8P8yIPnz0VOSEg5NElaYuOYRw9zkqxNE3oq'
#b = ccxt.binance({ 'options': { 'adjustForTimeDifference': True }})
##for production deployment remove testnet=True from below line of code
client = Client(api_key, secret_key)
#depth 
depth = client.get_order_book(symbol='ETHUSDT')
print(depth['asks'][1]) #to buy for
print(depth['bids'][-1]) #to sell for

#order book
tickers = client.get_orderbook_tickers()
#pprint.pprint(tickers)
print(depth['asks'][1])

#account info
client = Client(api_key, secret_key)
info = client.get_account()
pprint.pprint(info)

#trading strategy

#1 Get Average price
avg_price = client.get_avg_price(symbol='ETHUSDT')
print(avg_price)
avg_price = avg_price['price']
print(avg_price)
#depth 
depth = client.get_order_book(symbol='ETHUSDT')
pprint.pprint(depth)
ask_price = depth['asks'][1][0]

print(avg_price,ask_price)

if avg_price > ask_price:
  print('add strategy')
  #place trade
  symbol = 'ETHUSDT' # BTCBUSD
  try:  
    order = client.order_market_buy(symbol=symbol,quantity=0.2)
    #pprint.pprint(order)
    if order['status'] == 'FILLED':
      print('success')
      price = order['fills'][0]['price']
      quantity_filled = order['fills'][0]['qty']
      print('price ' + price, ' qty '+ quantity_filled)
  except Exception as e:
    print(e)

#get trades
trades = client.get_my_trades(symbol='ETHUSDT')
pprint.pprint(trades)
=======
import os

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
#import ccxt
api_key = 'vzY6b0n5qoUqo5srNn6LMSW2CLb8cXIgRstsKvdksKsZyxPq7A0eB6dcCtlKC9MQ'
secret_key = 'fD2PAd8K93FxesASG7rxKF29pBYKC8P8yIPnz0VOSEg5NElaYuOYRw9zkqxNE3oq'
#b = ccxt.binance({ 'options': { 'adjustForTimeDifference': True }})
##for production deployment remove testnet=True from below line of code
client = Client(api_key, secret_key)
#depth 
depth = client.get_order_book(symbol='ETHUSDT')
print(depth['asks'][1]) #to buy for
print(depth['bids'][-1]) #to sell for

#order book
tickers = client.get_orderbook_tickers()
#pprint.pprint(tickers)
print(depth['asks'][1])

#account info
client = Client(api_key, secret_key)
info = client.get_account()
pprint.pprint(info)

#trading strategy

#1 Get Average price
avg_price = client.get_avg_price(symbol='ETHUSDT')
print(avg_price)
avg_price = avg_price['price']
print(avg_price)
#depth 
depth = client.get_order_book(symbol='ETHUSDT')
pprint.pprint(depth)
ask_price = depth['asks'][1][0]

print(avg_price,ask_price)

if avg_price > ask_price:
  print('add strategy')
  #place trade
  symbol = 'ETHUSDT' # BTCBUSD
  try:  
    order = client.order_market_buy(symbol=symbol,quantity=0.2)
    #pprint.pprint(order)
    if order['status'] == 'FILLED':
      print('success')
      price = order['fills'][0]['price']
      quantity_filled = order['fills'][0]['qty']
      print('price ' + price, ' qty '+ quantity_filled)
  except Exception as e:
    print(e)

#get trades
trades = client.get_my_trades(symbol='ETHUSDT')
pprint.pprint(trades)
>>>>>>> bb5139a261576f42443de9c7549cfb80c1f47869
