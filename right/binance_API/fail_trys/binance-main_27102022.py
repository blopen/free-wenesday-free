<<<<<<< HEAD
from distutils.log import info
from locale import currency
import os
import string
import sys

from binance.client import Client
from binance.enums import *
import pprint
import time
import random
import webbrowser as wb
#import vlc

##Repo und optzizen**********
exchangeName = "binance"

API_KEY = 'IdOB74VGLBdyafLEJEaDbKr0ucE4oWROC94qLjYRFDdIRxusEjZryBRaNSOBs4a7'
SECRET_KEY = 'bTpX1dsKhOgWudEXft9ihOOCU2id7eG6QFe2P22nujrDaklck9Ze9nClxVMi5x7f'
RECV_WINDOW=60000
url='https://api.binance.com'
thecurrency=['LTCBUSD','BTCBUSD','ETHUSDT']
ranum=random.randint(0,2)
cur= thecurrency[0]#'LTCBUSD'#'BTCBUSD'ETHUSDT
class Binance:
    def __init__(self, public_key = '', secret_key = '', sync = False):
        self.time_offset = 0
        self.streamObject = Client(public_key, secret_key)
        #self.streamObject.API_URL = url  # for testnet
        if sync:
            self.time_offset = self._get_time_offset()
            print( "Offset: %s ms" % (self.time_offset) )

    def _get_time_offset(self):
        res = self.streamObject.get_server_time()
        return res['serverTime'] - int(time.time() * 1000)

    def my_balance(self):
        print(self.streamObject.get_account(recvWindow=RECV_WINDOW))
              
    def my_trades_lct(self):
        #symbol='BTCBUSD'
        #quantity=0.0002
        #trade = self.streamObject.get_my_trades(symbol='BTCBUSD')
        print(self.streamObject.get_my_trades(symbol='LTCBUSD'))
    def my_trades_btc(self):
    #symbol='BTCBUSD'
    #quantity=0.0002
    #trade = self.streamObject.get_my_trades(symbol='BTCBUSD')
        print(self.streamObject.get_my_trades(symbol='BTCBUSD'))
    def my_trades_eth(self):
    #symbol='BTCBUSD'
    #quantity=0.0002
    #trade = self.streamObject.get_my_trades(symbol='BTCBUSD')
        print(self.streamObject.get_my_trades(symbol='ETHUSDT'))
    def synced(self, fn_name, **args):
        args['timestamp'] = int(time.time() * 1000 + self.time_offset)
        return getattr(self.streamObject, fn_name)(**args)
      
    def synced_order(self, fn_name, **args):
        resp = self.streamObject.get_server_time()
        resp['serverTime'] - int(time.time() * 1000 + self.time_offset)
        return getattr(self.streamObject, fn_name)(**args)
binance = Binance(API_KEY, SECRET_KEY)
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
curList = []
i=0
prGreen("Mein Name ist Weday")
time.sleep(3)
prCyan(binance._get_time_offset())
print("Suchi nach deals isch gstartet :D")
for curentcur in thecurrency:
    print("Es wird berchent Strategie für: "+curentcur)
    depth = binance.streamObject.get_order_book(symbol=curentcur)
    tickers = binance.streamObject.get_orderbook_tickers()
    infos = binance.my_balance()
    avg_price = binance.streamObject.get_avg_price(symbol=curentcur)
    avg_price = avg_price['price']
    depth = binance.streamObject.get_order_book(symbol=curentcur)
    ask_price = depth['asks'][1][0]
    a = float(avg_price)
    b = float(ask_price)
    curList.append(a - b)
    print(avg_price,ask_price)
    
bestCur=curList.index(min(curList))   
print(curList)
prCyan(binance._get_time_offset())

depth = binance.streamObject.get_order_book(symbol=thecurrency[bestCur])
print(depth['asks'][1]) #to buy for
print(depth['bids'][-1]) #to sell for

#order book
tickers = binance.streamObject.get_orderbook_tickers()
pprint.pprint(tickers)
print(depth['asks'][1])

#account info
infos = binance.my_balance()
pprint.pprint(infos)

#trading strategy
#1 Get Average price
avg_price = binance.streamObject.get_avg_price(symbol=thecurrency[bestCur])
print(avg_price)
avg_price = avg_price['price']
print(avg_price)
#depth 
depth = binance.streamObject.get_order_book(symbol=thecurrency[bestCur])
pprint.pprint(depth)
ask_price = depth['asks'][1][0]

print(avg_price,ask_price)

print(infos)

if avg_price > ask_price:
  prRed('add strategy für '+thecurrency[bestCur])
  #place trade
  prCyan(binance._get_time_offset())
  check_symbol = thecurrency[bestCur] #'LTCBUSD' # BTCBUSD  ETHUSDT
  #symbol = curt #'LTCBUSD' # BTCBUSD  ETHUSDT
  try:
    #order = binance.my_trades_btc()
    #market_order = binance.streamObject.order_market_sell(symbol='BTCBUSD', quantity=0.004)
    #pprint.pprint(market_order)
    #pprint.pprint(order)
    
    
    #order = binance.synced_order('get_my_trades','BTCBUSD',0.0002)
    if check_symbol=="LTCBUSD":
            order = binance.my_trades_lct()
            market_order = binance.streamObject.order_limit_buy(symbol=thecurrency[bestCur], quantity=0.2, price=ask_price)
    elif check_symbol=='BTCBUSD':
            order = binance.my_trades_btc()
            market_order = binance.streamObject.order_limit_buy(symbol=thecurrency[bestCur], quantity=0.0005, price=ask_price)
    elif check_symbol=='ETHUSDT':
            order = binance.my_trades_eth()
            market_order = binance.streamObject.order_limit_buy(symbol=thecurrency[bestCur], quantity=0.004, price=ask_price)  
    
        
    prRed('add try für '+check_symbol)
    prCyan(binance._get_time_offset())
    
       
    pprint.pprint(market_order)
    pprint.pprint(order)
    if market_order['status'] == 'FILLED':
      time.sleep(3)
      prGreen('success :D')
      #wb.open('https://www.youtube.com/watch?v=btPJPFnesV4')
      #playsound.playsound('/home/nelson/wenstday/back/StilleMomente.mp3')
      #p = vlc.MediaPlayer("/home/nelson/wenstday/back/StilleMomente.mp3")
      #p.play()
      price = order['fills'][0]['price']
      quantity_filled = order['fills'][0]['qty']
      prCyan(binance._get_time_offset())
      prGreen('price ' + price, ' qty '+ quantity_filled)
      
    else:
        #get trades
        pprint.pprint(market_order)
        print('FAILS')
        print(binance._get_time_offset())
  except Exception as e:
    print(e)



print(binance._get_time_offset())
ranum=random.randint(0,2)
curt= thecurrency[ranum]#'LTCBUSD'#'BTCBUSD'ETHUSDT
    #get trades
if curt=="LTCBUSD":
    order = binance.my_trades_lct()
    market_order = binance.streamObject.order_market_sell(symbol=thecurrency[bestCur], quantity=0.4)#crush by insuflienc
if curt=='ETHUSDT':
    order = binance.my_trades_eth()
    market_order = binance.streamObject.order_market_sell(symbol=thecurrency[bestCur], quantity=0.05)#crush by insuflienc
    order = binance.my_trades_btc()
    market_order = binance.streamObject.order_market_sell(symbol=thecurrency[bestCur], quantity=0.0005)
print("Suchi nach trades bendet")
=======
from distutils.log import info
from locale import currency
import os
import string
import sys

from binance.client import Client
from binance.enums import *
import pprint
import time
import random
import webbrowser as wb
#import vlc

##Repo und optzizen**********
exchangeName = "binance"

API_KEY = 'IdOB74VGLBdyafLEJEaDbKr0ucE4oWROC94qLjYRFDdIRxusEjZryBRaNSOBs4a7'
SECRET_KEY = 'bTpX1dsKhOgWudEXft9ihOOCU2id7eG6QFe2P22nujrDaklck9Ze9nClxVMi5x7f'
RECV_WINDOW=60000
url='https://api.binance.com'
thecurrency=['LTCBUSD','BTCBUSD','ETHUSDT']
ranum=random.randint(0,2)
cur= thecurrency[0]#'LTCBUSD'#'BTCBUSD'ETHUSDT
class Binance:
    def __init__(self, public_key = '', secret_key = '', sync = False):
        self.time_offset = 0
        self.streamObject = Client(public_key, secret_key)
        #self.streamObject.API_URL = url  # for testnet
        if sync:
            self.time_offset = self._get_time_offset()
            print( "Offset: %s ms" % (self.time_offset) )

    def _get_time_offset(self):
        res = self.streamObject.get_server_time()
        return res['serverTime'] - int(time.time() * 1000)

    def my_balance(self):
        print(self.streamObject.get_account(recvWindow=RECV_WINDOW))
              
    def my_trades_lct(self):
        #symbol='BTCBUSD'
        #quantity=0.0002
        #trade = self.streamObject.get_my_trades(symbol='BTCBUSD')
        print(self.streamObject.get_my_trades(symbol='LTCBUSD'))
    def my_trades_btc(self):
    #symbol='BTCBUSD'
    #quantity=0.0002
    #trade = self.streamObject.get_my_trades(symbol='BTCBUSD')
        print(self.streamObject.get_my_trades(symbol='BTCBUSD'))
    def my_trades_eth(self):
    #symbol='BTCBUSD'
    #quantity=0.0002
    #trade = self.streamObject.get_my_trades(symbol='BTCBUSD')
        print(self.streamObject.get_my_trades(symbol='ETHUSDT'))
    def synced(self, fn_name, **args):
        args['timestamp'] = int(time.time() * 1000 + self.time_offset)
        return getattr(self.streamObject, fn_name)(**args)
      
    def synced_order(self, fn_name, **args):
        resp = self.streamObject.get_server_time()
        resp['serverTime'] - int(time.time() * 1000 + self.time_offset)
        return getattr(self.streamObject, fn_name)(**args)
binance = Binance(API_KEY, SECRET_KEY)
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
curList = []
i=0
prGreen("Mein Name ist Weday")
time.sleep(3)
prCyan(binance._get_time_offset())
print("Suchi nach deals isch gstartet :D")
for curentcur in thecurrency:
    print("Es wird berchent Strategie für: "+curentcur)
    depth = binance.streamObject.get_order_book(symbol=curentcur)
    tickers = binance.streamObject.get_orderbook_tickers()
    infos = binance.my_balance()
    avg_price = binance.streamObject.get_avg_price(symbol=curentcur)
    avg_price = avg_price['price']
    depth = binance.streamObject.get_order_book(symbol=curentcur)
    ask_price = depth['asks'][1][0]
    a = float(avg_price)
    b = float(ask_price)
    curList.append(a - b)
    print(avg_price,ask_price)
    
bestCur=curList.index(min(curList))   
print(curList)
prCyan(binance._get_time_offset())

depth = binance.streamObject.get_order_book(symbol=thecurrency[bestCur])
print(depth['asks'][1]) #to buy for
print(depth['bids'][-1]) #to sell for

#order book
tickers = binance.streamObject.get_orderbook_tickers()
pprint.pprint(tickers)
print(depth['asks'][1])

#account info
infos = binance.my_balance()
pprint.pprint(infos)

#trading strategy
#1 Get Average price
avg_price = binance.streamObject.get_avg_price(symbol=thecurrency[bestCur])
print(avg_price)
avg_price = avg_price['price']
print(avg_price)
#depth 
depth = binance.streamObject.get_order_book(symbol=thecurrency[bestCur])
pprint.pprint(depth)
ask_price = depth['asks'][1][0]

print(avg_price,ask_price)

print(infos)

if avg_price > ask_price:
  prRed('add strategy für '+thecurrency[bestCur])
  #place trade
  prCyan(binance._get_time_offset())
  check_symbol = thecurrency[bestCur] #'LTCBUSD' # BTCBUSD  ETHUSDT
  #symbol = curt #'LTCBUSD' # BTCBUSD  ETHUSDT
  try:
    #order = binance.my_trades_btc()
    #market_order = binance.streamObject.order_market_sell(symbol='BTCBUSD', quantity=0.004)
    #pprint.pprint(market_order)
    #pprint.pprint(order)
    
    
    #order = binance.synced_order('get_my_trades','BTCBUSD',0.0002)
    if check_symbol=="LTCBUSD":
            order = binance.my_trades_lct()
            market_order = binance.streamObject.order_limit_buy(symbol=thecurrency[bestCur], quantity=0.2, price=ask_price)
    elif check_symbol=='BTCBUSD':
            order = binance.my_trades_btc()
            market_order = binance.streamObject.order_limit_buy(symbol=thecurrency[bestCur], quantity=0.0005, price=ask_price)
    elif check_symbol=='ETHUSDT':
            order = binance.my_trades_eth()
            market_order = binance.streamObject.order_limit_buy(symbol=thecurrency[bestCur], quantity=0.004, price=ask_price)  
    
        
    prRed('add try für '+check_symbol)
    prCyan(binance._get_time_offset())
    
       
    pprint.pprint(market_order)
    pprint.pprint(order)
    if market_order['status'] == 'FILLED':
      time.sleep(3)
      prGreen('success :D')
      #wb.open('https://www.youtube.com/watch?v=btPJPFnesV4')
      #playsound.playsound('/home/nelson/wenstday/back/StilleMomente.mp3')
      #p = vlc.MediaPlayer("/home/nelson/wenstday/back/StilleMomente.mp3")
      #p.play()
      price = order['fills'][0]['price']
      quantity_filled = order['fills'][0]['qty']
      prCyan(binance._get_time_offset())
      prGreen('price ' + price, ' qty '+ quantity_filled)
      
    else:
        #get trades
        pprint.pprint(market_order)
        print('FAILS')
        print(binance._get_time_offset())
  except Exception as e:
    print(e)



print(binance._get_time_offset())
ranum=random.randint(0,2)
curt= thecurrency[ranum]#'LTCBUSD'#'BTCBUSD'ETHUSDT
    #get trades
if curt=="LTCBUSD":
    order = binance.my_trades_lct()
    market_order = binance.streamObject.order_market_sell(symbol=thecurrency[bestCur], quantity=0.4)#crush by insuflienc
if curt=='ETHUSDT':
    order = binance.my_trades_eth()
    market_order = binance.streamObject.order_market_sell(symbol=thecurrency[bestCur], quantity=0.05)#crush by insuflienc
    order = binance.my_trades_btc()
    market_order = binance.streamObject.order_market_sell(symbol=thecurrency[bestCur], quantity=0.0005)
print("Suchi nach trades bendet")
>>>>>>> bb5139a261576f42443de9c7549cfb80c1f47869
