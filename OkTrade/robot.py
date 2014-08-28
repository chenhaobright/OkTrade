#coding:utf-8

import okcoin
from userdata import UserData

NEGATIVE = 0
POSITIVE = 1

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

        #用户资产信息
        self.assetInfo = UserData(self.tradeAPI.get_userInfo()).getUserData()

        #价格
        self.priceList = [0]
        self.effect = POSITIVE
        self.canTrade = False

        #定时请求次数
        self.timerCount = 0


    def addTicker(self, ticker):
        curPrice = ( (float(ticker.bid) + float(ticker.ask)) * 0.5 )
        self.timerCount = self.timerCount + 1

        self.print_log(timerCount=self.timerCount,curPrice=curPrice, canTrade=self.canTrade,effect=self.effect)
        
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
        rate = 1
        amount = 1
        if(isBuy == True):
            rate = curPrice * (1 + 0.005)
            amount = self.assetInfo['free_cny'] / curPrice * 0.5
            self.tradeResult = self.tradeAPI.trade('ltc_cny', 'buy', str(rate), str(amount))
        else:
            rate = curPrice * (1 - 0.005)
            amount = self.assetInfo['free_ltc'] * 0.5
            self.tradeResult = self.tradeAPI.trade('ltc_cny', 'sell', str(rate), str(amount))

        self.tradeCount += 1
        self.print_log(tradeCount=self.tradeCount,isBuy=isBuy, rate=rate, amount=amount,tradeResult=self.tradeResult)

    def get_order(self, order_id):
        pass

    def cancel_order(self, order_id):
        pass

    def print_log(self, *args,**kw):
        print("args = ",args, "kw = ", kw)
        



