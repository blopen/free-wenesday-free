<<<<<<< HEAD
import os

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import pprint
import time
import hashlib
import base64
import hmac



#import ccxt
api_key = 'Ts6FXbGY8Dmis4UW7MHVVuQSrYqsjwVbRUvbpgLpgCclBMVqRjwsxHKrwqxjwAeG'
api_secret_base64 = base64.b64decode('txP8uxwCwZLISbxyYKZCneWgmhIBJh0w1TWmmwViZqDpiin7kPvwtsUUGcYYK0jr')
api_secret = 'txP8uxwCwZLISbxyYKZCneWgmhIBJh0w1TWmmwViZqDpiin7kPvwtsUUGcYYK0jr'
url="https://api.binance.com"
# Variables (API endpoint, nonce and HTTP POST data)
api_path = "/0/private/TradeBalance"
api_nonce = str(int(time.time()*1000))
api_post = "nonce=" + api_nonce + "&asset=xbt"
 
# Cryptographic hash algorithms
#api_sha256 = hashlib.sha256(api_nonce.encode('utf-8') + api_post.encode('utf-8'))
#api_hmac = hmac.new(api_secret, api_path.encode('utf-8') + api_sha256.digest(), hashlib.sha512)
 
# Encode signature into base64 format used in API-Sign value
#api_signature = base64.b64encode(api_hmac.digest())
 
# API authentication signature for use in API-Sign HTTP header
#print(api_signature.decode())
#for production remove testnet=True
client = Client(api_key, api_secret,url)

#depth 
depth = client.get_order_book(symbol='ETHUSDT')
print(depth['asks'][1]) #to buy for
#print(depth['bids'][-1]) #to sell for

#order book
tickers = client.get_orderbook_tickers()
#pprint.pprint(tickers)
print(depth['asks'][1])

#account info
info = client.get_account()
#pprint.pprint(client.get_account())

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
#trades = client.get_my_trades(symbol='ETHUSDT')
=======
import os

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import pprint
import time
import hashlib
import base64
import hmac



#import ccxt
api_key = 'Ts6FXbGY8Dmis4UW7MHVVuQSrYqsjwVbRUvbpgLpgCclBMVqRjwsxHKrwqxjwAeG'
api_secret_base64 = base64.b64decode('txP8uxwCwZLISbxyYKZCneWgmhIBJh0w1TWmmwViZqDpiin7kPvwtsUUGcYYK0jr')
api_secret = 'txP8uxwCwZLISbxyYKZCneWgmhIBJh0w1TWmmwViZqDpiin7kPvwtsUUGcYYK0jr'
url="https://api.binance.com"
# Variables (API endpoint, nonce and HTTP POST data)
api_path = "/0/private/TradeBalance"
api_nonce = str(int(time.time()*1000))
api_post = "nonce=" + api_nonce + "&asset=xbt"
 
# Cryptographic hash algorithms
#api_sha256 = hashlib.sha256(api_nonce.encode('utf-8') + api_post.encode('utf-8'))
#api_hmac = hmac.new(api_secret, api_path.encode('utf-8') + api_sha256.digest(), hashlib.sha512)
 
# Encode signature into base64 format used in API-Sign value
#api_signature = base64.b64encode(api_hmac.digest())
 
# API authentication signature for use in API-Sign HTTP header
#print(api_signature.decode())
#for production remove testnet=True
client = Client(api_key, api_secret,url)

#depth 
depth = client.get_order_book(symbol='ETHUSDT')
print(depth['asks'][1]) #to buy for
#print(depth['bids'][-1]) #to sell for

#order book
tickers = client.get_orderbook_tickers()
#pprint.pprint(tickers)
print(depth['asks'][1])

#account info
info = client.get_account()
#pprint.pprint(client.get_account())

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
#trades = client.get_my_trades(symbol='ETHUSDT')
>>>>>>> bb5139a261576f42443de9c7549cfb80c1f47869
#pprint.pprint(trades)