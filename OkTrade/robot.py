#coding:utf-8

import okcoin
from userdata import UserData

import time

NEGATIVE = 0
POSITIVE = 1

PRICE_RATIO = 0.002      
TRADE_RATIO = 0.5  

class Robot(object):
    def __init__(self, partner, secret_key,time = 60, count = 5):
        self.partner = partner
        self.secret_key = secret_key

        self.interval_time = time
        self.step_count = count 

        #交易信息
        self.tradeAPI = okcoin.TradeAPI(partner, secret_key)
        self.tradeResult = None
        self.tradeCount = 0

        #价格
        self.priceList = [0]
        self.effect = POSITIVE
        self.canTrade = False

        #定时请求次数
        self.timerCount = 0

    def addTicker(self, ticker):
        if(self.effect == POSITIVE):
            price = float(ticker.bid)
        else:
            price = float(ticker.ask)

        self.addPrice(price)

    def addPrice(self, price):
        curPrice = price
        self.timerCount = self.timerCount + 1
        
        self.print_time(curPrice)

        self.priceList.append(curPrice)

        self.tradeStrategy()
        
    def tradeStrategy(self):
        curPrice = self.priceList[-1]
        lastPrice = self.priceList[-2]

        if (self.canTrade == True):
            self.canTradeStrategy(curPrice, lastPrice)
        else:
            self.cannotTradeStrategy(curPrice, lastPrice)

    def canTradeStrategy(self, curPrice, lastPrice):
        if(self.effect == POSITIVE):
            if(curPrice >= lastPrice):
                return
            else:
                #一直上涨，当前下跌，卖出
                self.trade(False, curPrice)

                self.priceList = []
                self.priceList.append(curPrice)
                self.effect = NEGATIVE
        else:
            if(curPrice <= lastPrice):
                return
            else:
                #一直下跌，当前上涨，买入
                self.trade(True, curPrice)

                self.priceList = []
                self.priceList.append(curPrice)
                self.effect = NEGATIVE

    def cannotTradeStrategy(self, curPrice, lastPrice):
        priceCount = len(self.priceList)

        if self.effect == POSITIVE:
            if (curPrice >= lastPrice):
                if(priceCount >= self.step_count):
                    self.canTrade = True
            else:
                self.priceList = []
                self.priceList.append(curPrice)
                self.effect = NEGATIVE
        else:  
            if (curPrice <= lastPrice):
                if(priceCount >= self.step_count):
                    self.canTrade = True
            else:
                self.priceList = []
                self.priceList.append(curPrice)
                self.effect = POSITIVE

    def trade(self, isBuy, curPrice):   
        #用户资产信息，每次交易
        self.assetInfo = UserData(self.tradeAPI.get_userInfo()).getUserData()
        self.tradeCount += 1
        
        if(isBuy == True):
            rate = '%.2f' %( curPrice * (1 + PRICE_RATIO) )
            amount = '%.2f' % (self.assetInfo['free_cny'] / curPrice * TRADE_RATIO)
            self.tradeResult = self.tradeAPI.trade('ltc_cny', 'buy', str(rate), str(amount))

            self.print_log(timer=self.timerCount,tradeCount=self.tradeCount,isBuy=isBuy, rate=rate, amount=amount,result=self.tradeResult)
        else:
            rate = '%.2f' %( curPrice * (1 - PRICE_RATIO) )
            amount = '%.2f' %( self.assetInfo['free_ltc'] * TRADE_RATIO )
            self.tradeResult = self.tradeAPI.trade('ltc_cny', 'sell', str(rate), str(amount))

            self.print_log(timer=self.timerCount,tradeCount=self.tradeCount,isBuy=isBuy, rate=rate, amount=amount,result=self.tradeResult)

        self.canTrade = False

    def get_order(self, order_id):
        pass

    def cancel_order(self, order_id):
        pass

    def print_time(self,curPrice):
    	localtime = time.asctime( time.localtime(time.time()) )
    	print(localtime, curPrice)

    def print_log(self, *args,**kw):
        print("kw=", kw)
        print(self.priceList)
        print("free_cny=",self.assetInfo['free_cny'], "free_btc=",self.assetInfo['free_btc'], "free_ltc=",self.assetInfo['free_ltc'])
        



