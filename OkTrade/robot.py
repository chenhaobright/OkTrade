#coding:utf-8

import okcoin
from userdata import UserData

import time

NEGATIVE = 0
POSITIVE = 1

PRICE_RATIO = 0.001      
TRADE_RATIO = 0.5  
PRICE_INTERVAL = 0.05

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
        self.buyCount = 0
        self.sellCount = 0

        #价格
        self.priceList = [0]
        self.effect = POSITIVE
        self.canTrade = False
        self.isUp = 1

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

        self.priceList.append(curPrice)

        self.tradeStrategy()
        
    def tradeStrategy(self):
        curPrice = self.priceList[-1]
        lastPrice = self.priceList[-2]

        if(curPrice > lastPrice):
            self.isUp = 1
        elif (curPrice < lastPrice):
            self.isUp = -1
        else:
            self.isUp = 0
                
        self.printTime(curPrice, self.isUp)

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
                if(abs(curPrice - self.priceList[0]) >= PRICE_INTERVAL or abs(curPrice - lastPrice) >= PRICE_INTERVAL):
                    self.trade(False, curPrice)

                self.canTrade = False
                self.priceList = []
                self.priceList.append(lastPrice)
                self.priceList.append(curPrice)
                self.effect = NEGATIVE
        else:
            if(curPrice <= lastPrice):
                return
            else:
                #一直下跌，当前上涨，买入
                if(abs(curPrice - self.priceList[0]) >= PRICE_INTERVAL or abs(curPrice - lastPrice) >= PRICE_INTERVAL):
                    self.trade(True, curPrice)

                self.canTrade = False
                self.priceList = []
                self.priceList.append(lastPrice)
                self.priceList.append(curPrice)
                self.effect = POSITIVE

    def cannotTradeStrategy(self, curPrice, lastPrice):
        priceCount = len(self.priceList)

        if self.effect == POSITIVE:
            if (curPrice >= lastPrice):
                if(priceCount >= self.step_count):
                    self.canTrade = True
            else:
                self.priceList = []
                self.priceList.append(lastPrice)
                self.priceList.append(curPrice)
                self.effect = NEGATIVE
        else:  
            if (curPrice <= lastPrice):
                if(priceCount >= self.step_count):
                    self.canTrade = True
            else:
                self.priceList = []
                self.priceList.append(lastPrice)
                self.priceList.append(curPrice)
                self.effect = POSITIVE

    def trade(self, isBuy, curPrice):   
        #用户资产信息，每次交易
        self.assetInfo = UserData(self.tradeAPI.get_userInfo()).getUserData()
        self.tradeCount += 1
        
        if(isBuy == True):
            rate = '%.2f' %( curPrice * (1 + PRICE_RATIO) )
            amount = '%.2f' % (self.assetInfo['free_cny'] / curPrice * self.getTradeRatio(isBuy))
            self.tradeResult = self.tradeAPI.trade('ltc_cny', 'buy', str(rate), str(amount))

            self.sellCount = 0
            self.buyCount += 1
            self.printLog(timer=self.timerCount,tradeCount=self.tradeCount,isBuy=isBuy, 
                rate=rate, amount=amount,result=self.tradeResult,buyCount=self.buyCount,
                effect=self.effect)
        else:
            rate = '%.2f' %( curPrice * (1 - PRICE_RATIO) )
            amount = '%.2f' %( self.assetInfo['free_ltc'] * self.getTradeRatio(isBuy))
            self.tradeResult = self.tradeAPI.trade('ltc_cny', 'sell', str(rate), str(amount))

            self.sellCount += 1
            self.buyCount = 0
            self.printLog(timer=self.timerCount,tradeCount=self.tradeCount,isBuy=isBuy, 
                rate=rate, amount=amount,result=self.tradeResult,sellCount=self.sellCount,
                effect=self.effect)

    def getOrder(self, order_id):
        pass

    def cancelOrder(self, order_id):
        pass

    def getTradeRatio(self, isBuy):
        tradeRatio = 0

        #如果一次交易中，涨跌幅超过1%，卖多点
        ratioDelta = abs(self.priceList[-1] - self.priceList[0]) / self.priceList[0]
        if(ratioDelta > 0.01):      #1%
            return 0.7
        elif(ratioDelta > 0.15):    #1.5%
            return 0.8
        elif(ratioDelta > 0.02):    #2%
            return 0.9
        else:
            pass

        #正常涨跌幅
        if(isBuy):
            if(self.buyCount == 0):
            	if(self.sellCount == 0):	#前面没有卖
            		tradeRatio = 0.2
            	elif(self.sellCount == 1):  #前面卖了一次
            		tradeRatio = 0.2
            	elif(self.sellCount == 2):  #前面卖了两次
            		tradeRatio = 0.1
            	elif(self.sellCount == 3):  #三次
            		tradeRatio = 0.05
            	else:
            		tradeRatio = 0.05		#N次
            elif(self.buyCount == 1):
                tradeRatio = 0.3
            elif(self.buyCount == 2):
                tradeRatio = 0.9
            else:
                tradeRatio = 0.5
        else:
            if(self.sellCount == 0):
                if(self.buyCount == 0):    #前面买0次,只有启动才发生
                    tradeRatio = 0.2
                elif(self.buyCount == 1):  #前面买了一次
                    tradeRatio = 0.2
                elif(self.buyCount == 2):  #前面买了两次
                    tradeRatio = 0.1
                elif(self.buyCount == 3):  #三次
                    tradeRatio = 0.05
                else:
                    tradeRatio = 0.05       #N次
            elif(self.sellCount == 1):
                tradeRatio = 0.3
            elif(self.sellCount == 2):
                tradeRatio = 0.9
            else:
                tradeRatio = 0.5
        
        return tradeRatio

    def printTime(self,curPrice, isUp):
    	localtime = time.asctime( time.localtime(time.time()) )
    	print(localtime, curPrice, isUp)

    def printLog(self, *args,**kw):
        print("kw=", kw)
        print(self.priceList)
        print("free_cny=",self.assetInfo['free_cny'], "free_btc=",self.assetInfo['free_btc'], "free_ltc=",self.assetInfo['free_ltc'])
        



