#coding:utf-8

import threading  
import okcoin
from robot import Robot 

partner = 1234567
secret_key = 'XXXXXE548EB758613F589250150XXXXX'

interval_time = 60   
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
    list5 = [32.16, 32.17, 32.17,32.14,32.14,32.16,32.17,32.17,32.19,32.16,32.21]
    for price in list5:
    	robot.addPrice(price)
    '''
    
