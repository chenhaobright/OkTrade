#coding:utf-8

#  date   : 2014/08/27
# author  : chenhao
# function: data base class

class UserData(object):
    def __init__(self, result = None):
        self.__data = {}
        self.setUserData(result)

    def setUserData(self, result):
        self.__result = result

        #总资金
        self.__data['asset_net'] = float(result['info']['funds']['asset']['net'])
        self.__data['asset_total'] = float(result['info']['funds']['asset']['total'])

        #剩余资金
        self.__data['free_cny'] = float(result['info']['funds']['free']['cny'])
        self.__data['free_btc'] = float(result['info']['funds']['free']['btc'])
        self.__data['free_ltc'] = float(result['info']['funds']['free']['ltc'])
        
        #冻结资金
        self.__data['freezed_cny'] = float(result['info']['funds']['freezed']['cny'])
        self.__data['freezed_btc'] = float(result['info']['funds']['freezed']['btc'])
        self.__data['freezed_ltc'] = float(result['info']['funds']['freezed']['ltc'])

    def getUserData(self):
        return self.__data



     