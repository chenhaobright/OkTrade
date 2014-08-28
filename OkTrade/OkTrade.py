#coding:utf-8

import threading  
import okcoin
from robot import Robot 

partner = 3296386
secret_key = '3DD45E548EB758613F589250150CD1ED'

interval_time = 50     
step_count = 5

#启动交易机器人
robot = Robot(partner, secret_key, interval_time, step_count)

'''
list1 = [1,2,3,4,5,6,7,6]
list2 = [7,6,5,4,3,2,1,2]
list3 = [3,2,2,4,5,6,7,8,3]
list4 = [7,8,8,6,4,3,2,1,3,1,2,3,4,5,6,7,6,7,6,5,4,3,2,1,2,3,2,2,4,5,6,7,8,3]
'''

def autoTrade():  
    #得到一次市场数据 
    market = okcoin.MarketData()
    robot.addTicker(market.ticker('ltc_cny'))

    global t 
    t = threading.Timer(interval_time, autoTrade)  
    t.start()  
  
if __name__ == "__main__":
    t = threading.Timer(interval_time, autoTrade)  
    t.start() 
    '''
    for price in list4:
    	robot.addPrice(price)
    '''





