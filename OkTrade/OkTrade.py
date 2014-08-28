#coding:utf-8

import threading  
import okcoin
from robot import Robot 

partner = 3296386
secret_key = '3DD45E548EB758613F589250150CD1ED'

interval_time = 40     
step_count = 5

#启动交易机器人
robot = Robot(partner, secret_key, interval_time, step_count)

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





