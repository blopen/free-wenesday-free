<<<<<<< HEAD
#importing lyps
from distutils.log import info
from locale import currency
import os
import string
import symbol
import sys

from binance.client import Client
from binance.enums import *
import pprint
import time
import random
#import webbrowser as wb
import logging
import json  
import datetime
#import vlc

##Repo und optzizen**********BCCBTC
#init Env Variabels
exchangeName = "binance"
API_KEY = 'IdOB74VGLBdyafLEJEaDbKr0ucE4oWROC94qLjYRFDdIRxusEjZryBRaNSOBs4a7'
SECRET_KEY = 'bTpX1dsKhOgWudEXft9ihOOCU2id7eG6QFe2P22nujrDaklck9Ze9nClxVMi5x7f'
RECV_WINDOW=6000
url='https://api.binance.com'
thecurrency=['LTCBUSD','BTCBUSD','ETHUSDT']
ranum=random.randint(0,2)
cur= thecurrency[0]#'LTCBUSD'#'BTCBUSD'ETHUSDT
lastOneSell = 0
lastOneBuy = 0
best_price_before = 0
worest_price_before = 0
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
        print(self.streamObject.get_account(recvWindow=6000))
              
    def my_trades_lct(self):
        #symbol='BTCBUSD'
        #quantity=0.0002
        #trade = self.streamObject.get_my_trades(symbol='BTCBUSD')
        print(self.streamObject.get_my_trades(symbol='LTCBUSD',recvWindow=6000))
        
    def my_trades_btc(self):
        print(self.streamObject.get_my_trades(symbol='BTCBUSD',recvWindow=6000))
        
    def my_trades_eth(self):
        print(self.streamObject.get_my_trades(symbol='ETHUSDT',recvWindow=6000))
        
    def synced(self, fn_name, **args):
        args['timestamp'] = int(time.time() * 1000 + self.time_offset)
        return getattr(self.streamObject, fn_name)(**args)
  #syncorder sycn idea    
"""     def synced_order(self, fn_name, **args):
        resp = self.streamObject.get_server_time()
        resp['serverTime'] - int(time.time() * 1000 + self.time_offset)
        return getattr(self.streamObject, fn_name)(**args) """
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))

# logging  
LOG = "/home/nelson/wenstday/right/binance_API/tmp/wenstday_action.log"                                                     
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)  

# console handler  
console = logging.StreamHandler()  
console.setLevel(logging.ERROR)  
logging.getLogger("").addHandler(console)


binance = Binance(API_KEY, SECRET_KEY)
prGreen("Mein Name ist Wenstay")
prGreen("Suchi nach deals isch gstartet :D")
prCyan(binance._get_time_offset())
#test for all
tickersValues = binance.streamObject.get_orderbook_tickers() #list of all possibel curenysy
thePossibleCurrency=[]
for resultes in tickersValues:
    for value in resultes:
        if value== "symbol":
            thePossibleCurrency.append(resultes[value])

##ave fortuna 40%
thecurrency.append(random.choice(thePossibleCurrency))
thecurrency.append(random.choice(thePossibleCurrency))

#Compare Values
curList = []
for curentcur in thecurrency:
    prCyan("Es wird berchent Strategie für: "+curentcur)
    depth = binance.streamObject.get_order_book(symbol=curentcur)
    tickers = binance.streamObject.get_orderbook_tickers() #list of all possibel curenysy
    binance.my_balance()
    avg_price = binance.streamObject.get_avg_price(symbol=curentcur)
    avg_price = avg_price['price']
    depth = binance.streamObject.get_order_book(symbol=curentcur)
    ask_price = depth['asks'][1][0]
    a = float(avg_price)
    b = float(ask_price)
    curList.append(a - b)
    prGreen(print(avg_price,ask_price))
    
bestCur=curList.index(min(curList))   #eigendlich min azuf max test 27.10.2022
worestCur=curList.index(max(curList))   #eigendlich min azuf max test 27.10.2022
prGreen(curList)
with open('/home/nelson/wenstday/right/binance_API/tmp/lastOne.json', 'r') as outFileJson:
    lastOneJson = json.load(outFileJson)

#statistik resason for contionues    
for outFileJson in lastOneJson:
    for lastAction, value in lastOneJson.items():
        for lastCurrencyKey, amount in value.items():
            if int(float(amount) > 0) & int(thecurrency[bestCur]==lastCurrencyKey):
                if 'buy' in lastAction:
                    best_price_before = amount
                if 'sell' in lastAction:
                    worest_price_before = amount

prCyan(binance._get_time_offset())

depth = binance.streamObject.get_order_book(symbol=thecurrency[bestCur])
prGreen(depth['asks'][1]) #to buy for
prGreen(depth['bids'][-1]) #to sell for

#order book
tickers = binance.streamObject.get_orderbook_tickers()
pprint.pprint(tickers)
prGreen(depth['asks'][1])

#account info -- working method
infos = binance.synced('get_account',recvWindow=6000)
prGreen(infos)

#trading strategy
#1 Get Average price
avg_price = binance.streamObject.get_avg_price(symbol=thecurrency[bestCur])
prGreen(avg_price)
avg_price = avg_price['price']
prGreen(avg_price)
#depth 
depth = binance.streamObject.get_order_book(symbol=thecurrency[bestCur])
prGreen(depth)
ask_price = depth['asks'][1][0]

prGreen(print(avg_price,ask_price))

prGreen(infos)
if float(avg_price) > float(best_price_before):
    if avg_price > ask_price:
        prGreen('add strategy für '+thecurrency[bestCur])
        #place trade
        prCyan(binance._get_time_offset())
        check_symbol = thecurrency[bestCur] #'LTCBUSD' # BTCBUSD  ETHUSDT
        #symbol = curt #'LTCBUSD' # BTCBUSD  ETHUSDT
        try:
            #order = binance.synced_order('get_my_trades','BTCBUSD',0.0002)
            if check_symbol=="LTCBUSD":
                    order = binance.my_trades_lct()
                    market_order = binance.synced('order_limit_buy',symbol=thecurrency[bestCur], quantity=0.2, price=ask_price, recvWindow=6000)
            elif check_symbol=='BTCBUSD':
                    order = binance.my_trades_btc()
                    market_order = binance.synced('order_limit_buy',symbol=thecurrency[bestCur], quantity=0.0005, price=ask_price, recvWindow=6000)#working
            elif check_symbol=='ETHUSDT':
                    order = binance.my_trades_eth()
                    market_order = binance.synced('order_limit_buy',symbol=thecurrency[bestCur], quantity=0.007, price=ask_price, recvWindow=6000)  
            else:
                    order = binance.synced('get_my_trades',symbol=thecurrency[bestCur], recvWindow=6000)
                    try:
                        market_order = binance.synced('order_limit_buy',symbol=thecurrency[bestCur], quantity=1, price=ask_price, recvWindow=6000)  
                    except Exception as e:
                        market_order = binance.synced('order_limit_buy',symbol=thecurrency[bestCur], quantity=10, price=ask_price, recvWindow=6000)  
                        prGreen(e)
                    
                
            prGreen('add try für '+check_symbol)
            prCyan(binance._get_time_offset())
            lastOneBuy = avg_price
            
            prGreen(market_order)
            prGreen(order)
            if market_order['status'] == 'FILLED':
                time.sleep(3)
                prGreen('success :D')
                price = order['fills'][0]['price']
                quantity_filled = order['fills'][0]['qty']
                prCyan(binance._get_time_offset())
                prGreen('price ' + price, ' qty '+ quantity_filled)
            
            else:
                #get trades
                prGreen(market_order)
                prGreen('FAILS')
                prGreen(binance._get_time_offset())
        except Exception as e:
            prGreen(e)

    
time.sleep(2)

prGreen(binance._get_time_offset())
prCyan(binance._get_time_offset())

depth = binance.streamObject.get_order_book(symbol=thecurrency[worestCur])
prRed(depth['asks'][1]) #to buy for
prRed(depth['bids'][-1]) #to sell for

#order book
tickers = binance.streamObject.get_orderbook_tickers()
prRed(tickers)
prRed(depth['asks'][1])

#account info
infos = binance.my_balance()
prRed(infos)

#trading strategy
#1 Get Average price
avg_price = binance.streamObject.get_avg_price(symbol=thecurrency[worestCur])
prRed(avg_price)
avg_price = avg_price['price']
prRed(avg_price)
#depth 
depth = binance.streamObject.get_order_book(symbol=thecurrency[worestCur])
prRed(depth)
ask_price = depth['asks'][1][0]

prRed(print(avg_price,ask_price))

prRed(pprint.pprint(infos))

if float(ask_price) > float(worest_price_before):
    if avg_price > ask_price:
        prRed('add strategy für '+thecurrency[worestCur])
        #place trade
        prCyan(binance._get_time_offset())
        check_symbol = thecurrency[worestCur] #'LTCBUSD' # BTCBUSD  ETHUSDT
        #symbol = curt #'LTCBUSD' # BTCBUSD  ETHUSDT
        try:
            #order = binance.synced_order('get_my_trades','BTCBUSD',0.0002)
            if check_symbol=="LTCBUSD":
                order = binance.my_trades_lct()
                market_order = binance.synced('order_market_sell',symbol=thecurrency[worestCur], quantity=0.2, recvWindow=6000)#crush by insuflienc
            elif check_symbol=='ETHUSDT':
                order = binance.my_trades_eth()
                market_order = binance.synced('order_market_sell',symbol=thecurrency[worestCur], quantity=0.007, recvWindow=6000)#crush by insuflienc
            elif check_symbol=='BTCBUSD':
                order = binance.my_trades_btc()
                market_order = binance.synced('order_market_sell',symbol=thecurrency[worestCur], quantity=0.0005, recvWindow=6000)
            else:
                order = binance.synced('get_my_trades',symbol=thecurrency[worestCur], recvWindow=6000)
                try:
                    market_order = binance.synced('order_market_sell',symbol=thecurrency[worestCur], quantity=1, price=ask_price, recvWindow=6000)  
                except Exception as e:
                    market_order = binance.synced('order_market_sell',symbol=thecurrency[worestCur], quantity=10, price=ask_price, recvWindow=6000)  
                    prGreen(e)
            
                
            prRed('add try für '+check_symbol)
            prCyan(binance._get_time_offset())
        
            prRed(market_order)
            prRed(order)
            if market_order['status'] == 'FILLED':
                lastOneSell = avg_price
                prRed('success :D')
                price = order['fills'][0]['price']
                quantity_filled = order['fills'][0]['qty']
                prCyan(binance._get_time_offset())
                prRed('price ' + price, ' qty '+ quantity_filled)
            
            else:
                #get trades
                prRed(market_order)
                print('FAILS')
                print(binance._get_time_offset())
        except Exception as e:
            print(e)
time.sleep(3)
#get current date and time
x = datetime.datetime.now()

#convert date and time to string
dateTimeStr = str(x)

prRed(dateTimeStr)
lastOne = {
    "buy "+str(dateTimeStr): {
        thecurrency[worestCur]:lastOneBuy
        },
    "sell "+str(dateTimeStr): {
             thecurrency[bestCur]:lastOneSell
            }
}
with open('/home/nelson/wenstday/right/binance_API/tmp/lastOne.json') as outfile:
    data = json.load(outfile)

data.update(lastOne)

with open('/home/nelson/wenstday/right/binance_API/tmp/lastOne.json', 'w')  as outfile:
    json.dump(data, outfile)  




=======
#importing lyps
from distutils.log import info
from locale import currency
import os
import string
import symbol
import sys

from binance.client import Client
from binance.enums import *
import pprint
import time
import random
#import webbrowser as wb
import logging
import json  
import datetime
#import vlc

##Repo und optzizen**********BCCBTC
#init Env Variabels
exchangeName = "binance"
API_KEY = 'IdOB74VGLBdyafLEJEaDbKr0ucE4oWROC94qLjYRFDdIRxusEjZryBRaNSOBs4a7'
SECRET_KEY = 'bTpX1dsKhOgWudEXft9ihOOCU2id7eG6QFe2P22nujrDaklck9Ze9nClxVMi5x7f'
RECV_WINDOW=6000
url='https://api.binance.com'
thecurrency=['LTCBUSD','BTCBUSD','ETHUSDT']
ranum=random.randint(0,2)
cur= thecurrency[0]#'LTCBUSD'#'BTCBUSD'ETHUSDT
lastOneSell = 0
lastOneBuy = 0
best_price_before = 0
worest_price_before = 0
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
        print(self.streamObject.get_account(recvWindow=6000))
              
    def my_trades_lct(self):
        #symbol='BTCBUSD'
        #quantity=0.0002
        #trade = self.streamObject.get_my_trades(symbol='BTCBUSD')
        print(self.streamObject.get_my_trades(symbol='LTCBUSD',recvWindow=6000))
        
    def my_trades_btc(self):
        print(self.streamObject.get_my_trades(symbol='BTCBUSD',recvWindow=6000))
        
    def my_trades_eth(self):
        print(self.streamObject.get_my_trades(symbol='ETHUSDT',recvWindow=6000))
        
    def synced(self, fn_name, **args):
        args['timestamp'] = int(time.time() * 1000 + self.time_offset)
        return getattr(self.streamObject, fn_name)(**args)
  #syncorder sycn idea    
"""     def synced_order(self, fn_name, **args):
        resp = self.streamObject.get_server_time()
        resp['serverTime'] - int(time.time() * 1000 + self.time_offset)
        return getattr(self.streamObject, fn_name)(**args) """
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))

# logging  
LOG = "/home/nelson/wenstday/right/binance_API/tmp/wenstday_action.log"                                                     
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)  

# console handler  
console = logging.StreamHandler()  
console.setLevel(logging.ERROR)  
logging.getLogger("").addHandler(console)


binance = Binance(API_KEY, SECRET_KEY)
prGreen("Mein Name ist Wenstay")
prGreen("Suchi nach deals isch gstartet :D")
prCyan(binance._get_time_offset())
#test for all
tickersValues = binance.streamObject.get_orderbook_tickers() #list of all possibel curenysy
thePossibleCurrency=[]
for resultes in tickersValues:
    for value in resultes:
        if value== "symbol":
            thePossibleCurrency.append(resultes[value])

##ave fortuna 40%
thecurrency.append(random.choice(thePossibleCurrency))
thecurrency.append(random.choice(thePossibleCurrency))

#Compare Values
curList = []
for curentcur in thecurrency:
    prCyan("Es wird berchent Strategie für: "+curentcur)
    depth = binance.streamObject.get_order_book(symbol=curentcur)
    tickers = binance.streamObject.get_orderbook_tickers() #list of all possibel curenysy
    binance.my_balance()
    avg_price = binance.streamObject.get_avg_price(symbol=curentcur)
    avg_price = avg_price['price']
    depth = binance.streamObject.get_order_book(symbol=curentcur)
    ask_price = depth['asks'][1][0]
    a = float(avg_price)
    b = float(ask_price)
    curList.append(a - b)
    prGreen(print(avg_price,ask_price))
    
bestCur=curList.index(min(curList))   #eigendlich min azuf max test 27.10.2022
worestCur=curList.index(max(curList))   #eigendlich min azuf max test 27.10.2022
prGreen(curList)
with open('/home/nelson/wenstday/right/binance_API/tmp/lastOne.json', 'r') as outFileJson:
    lastOneJson = json.load(outFileJson)

#statistik resason for contionues    
for outFileJson in lastOneJson:
    for lastAction, value in lastOneJson.items():
        for lastCurrencyKey, amount in value.items():
            if int(float(amount) > 0) & int(thecurrency[bestCur]==lastCurrencyKey):
                if 'buy' in lastAction:
                    best_price_before = amount
                if 'sell' in lastAction:
                    worest_price_before = amount

prCyan(binance._get_time_offset())

depth = binance.streamObject.get_order_book(symbol=thecurrency[bestCur])
prGreen(depth['asks'][1]) #to buy for
prGreen(depth['bids'][-1]) #to sell for

#order book
tickers = binance.streamObject.get_orderbook_tickers()
pprint.pprint(tickers)
prGreen(depth['asks'][1])

#account info -- working method
infos = binance.synced('get_account',recvWindow=6000)
prGreen(infos)

#trading strategy
#1 Get Average price
avg_price = binance.streamObject.get_avg_price(symbol=thecurrency[bestCur])
prGreen(avg_price)
avg_price = avg_price['price']
prGreen(avg_price)
#depth 
depth = binance.streamObject.get_order_book(symbol=thecurrency[bestCur])
prGreen(depth)
ask_price = depth['asks'][1][0]

prGreen(print(avg_price,ask_price))

prGreen(infos)
if float(avg_price) > float(best_price_before):
    if avg_price > ask_price:
        prGreen('add strategy für '+thecurrency[bestCur])
        #place trade
        prCyan(binance._get_time_offset())
        check_symbol = thecurrency[bestCur] #'LTCBUSD' # BTCBUSD  ETHUSDT
        #symbol = curt #'LTCBUSD' # BTCBUSD  ETHUSDT
        try:
            #order = binance.synced_order('get_my_trades','BTCBUSD',0.0002)
            if check_symbol=="LTCBUSD":
                    order = binance.my_trades_lct()
                    market_order = binance.synced('order_limit_buy',symbol=thecurrency[bestCur], quantity=0.2, price=ask_price, recvWindow=6000)
            elif check_symbol=='BTCBUSD':
                    order = binance.my_trades_btc()
                    market_order = binance.synced('order_limit_buy',symbol=thecurrency[bestCur], quantity=0.0005, price=ask_price, recvWindow=6000)#working
            elif check_symbol=='ETHUSDT':
                    order = binance.my_trades_eth()
                    market_order = binance.synced('order_limit_buy',symbol=thecurrency[bestCur], quantity=0.007, price=ask_price, recvWindow=6000)  
            else:
                    order = binance.synced('get_my_trades',symbol=thecurrency[bestCur], recvWindow=6000)
                    try:
                        market_order = binance.synced('order_limit_buy',symbol=thecurrency[bestCur], quantity=1, price=ask_price, recvWindow=6000)  
                    except Exception as e:
                        market_order = binance.synced('order_limit_buy',symbol=thecurrency[bestCur], quantity=10, price=ask_price, recvWindow=6000)  
                        prGreen(e)
                    
                
            prGreen('add try für '+check_symbol)
            prCyan(binance._get_time_offset())
            lastOneBuy = avg_price
            
            prGreen(market_order)
            prGreen(order)
            if market_order['status'] == 'FILLED':
                time.sleep(3)
                prGreen('success :D')
                price = order['fills'][0]['price']
                quantity_filled = order['fills'][0]['qty']
                prCyan(binance._get_time_offset())
                prGreen('price ' + price, ' qty '+ quantity_filled)
            
            else:
                #get trades
                prGreen(market_order)
                prGreen('FAILS')
                prGreen(binance._get_time_offset())
        except Exception as e:
            prGreen(e)

    
time.sleep(2)

prGreen(binance._get_time_offset())
prCyan(binance._get_time_offset())

depth = binance.streamObject.get_order_book(symbol=thecurrency[worestCur])
prRed(depth['asks'][1]) #to buy for
prRed(depth['bids'][-1]) #to sell for

#order book
tickers = binance.streamObject.get_orderbook_tickers()
prRed(tickers)
prRed(depth['asks'][1])

#account info
infos = binance.my_balance()
prRed(infos)

#trading strategy
#1 Get Average price
avg_price = binance.streamObject.get_avg_price(symbol=thecurrency[worestCur])
prRed(avg_price)
avg_price = avg_price['price']
prRed(avg_price)
#depth 
depth = binance.streamObject.get_order_book(symbol=thecurrency[worestCur])
prRed(depth)
ask_price = depth['asks'][1][0]

prRed(print(avg_price,ask_price))

prRed(pprint.pprint(infos))

if float(ask_price) > float(worest_price_before):
    if avg_price > ask_price:
        prRed('add strategy für '+thecurrency[worestCur])
        #place trade
        prCyan(binance._get_time_offset())
        check_symbol = thecurrency[worestCur] #'LTCBUSD' # BTCBUSD  ETHUSDT
        #symbol = curt #'LTCBUSD' # BTCBUSD  ETHUSDT
        try:
            #order = binance.synced_order('get_my_trades','BTCBUSD',0.0002)
            if check_symbol=="LTCBUSD":
                order = binance.my_trades_lct()
                market_order = binance.synced('order_market_sell',symbol=thecurrency[worestCur], quantity=0.2, recvWindow=6000)#crush by insuflienc
            elif check_symbol=='ETHUSDT':
                order = binance.my_trades_eth()
                market_order = binance.synced('order_market_sell',symbol=thecurrency[worestCur], quantity=0.007, recvWindow=6000)#crush by insuflienc
            elif check_symbol=='BTCBUSD':
                order = binance.my_trades_btc()
                market_order = binance.synced('order_market_sell',symbol=thecurrency[worestCur], quantity=0.0005, recvWindow=6000)
            else:
                order = binance.synced('get_my_trades',symbol=thecurrency[worestCur], recvWindow=6000)
                try:
                    market_order = binance.synced('order_market_sell',symbol=thecurrency[worestCur], quantity=1, price=ask_price, recvWindow=6000)  
                except Exception as e:
                    market_order = binance.synced('order_market_sell',symbol=thecurrency[worestCur], quantity=10, price=ask_price, recvWindow=6000)  
                    prGreen(e)
            
                
            prRed('add try für '+check_symbol)
            prCyan(binance._get_time_offset())
        
            prRed(market_order)
            prRed(order)
            if market_order['status'] == 'FILLED':
                lastOneSell = avg_price
                prRed('success :D')
                price = order['fills'][0]['price']
                quantity_filled = order['fills'][0]['qty']
                prCyan(binance._get_time_offset())
                prRed('price ' + price, ' qty '+ quantity_filled)
            
            else:
                #get trades
                prRed(market_order)
                print('FAILS')
                print(binance._get_time_offset())
        except Exception as e:
            print(e)
time.sleep(3)
#get current date and time
x = datetime.datetime.now()

#convert date and time to string
dateTimeStr = str(x)

prRed(dateTimeStr)
lastOne = {
    "buy "+str(dateTimeStr): {
        thecurrency[worestCur]:lastOneBuy
        },
    "sell "+str(dateTimeStr): {
             thecurrency[bestCur]:lastOneSell
            }
}
with open('/home/nelson/wenstday/right/binance_API/tmp/lastOne.json') as outfile:
    data = json.load(outfile)

data.update(lastOne)

with open('/home/nelson/wenstday/right/binance_API/tmp/lastOne.json', 'w')  as outfile:
    json.dump(data, outfile)  




>>>>>>> bb5139a261576f42443de9c7549cfb80c1f47869
