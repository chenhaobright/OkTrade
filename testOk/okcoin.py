#coding:utf-8

import urllib
import urllib2
import hashlib
import simplejson

class TickerObject(object):
    def __init__(self, data):
        pass

class DepthObject(object):
    def __init__(self, data):
        pass

class MarketData(object):
    def get_json(self, url):
        pass

    def ticker(self, symbol):
        pass

    def get_depth(self, symbol):
        pass

    def get_history(self, symbol):
        pass

class TradeAPI(object):
    def __init__(self, partner, secret):
        #partner is integer, secret is string

        self.partner = partner
        self.secret = secret

    def _post(self, params, url):
        
        # params does not include the signed part, we add that
        
        sign_string = ''
        
        for pos,key in enumerate(sorted(params.keys())):
            sign_string += key + '=' + str(params[key])
            if( pos != len(params) - 1 ):
                sign_string += '&'
                
        sign_string += self.secret
        m = hashlib.md5()
        m.update(sign_string)
        signed = m.hexdigest().upper()

        params['sign'] = signed

        data = urllib.urlencode(params)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = simplejson.load(response)

        success = result[u'result']
        if( not success ):
            print('Error: ' + str(result[u'errorCode']))
            print( self.error_code_meaning(result[u'errorCode']) )
            return(result)
        else:
            return(result)
            
    def get_info(self):
        params = {'partner':self.partner}
        user_info_url = 'https://www.okcoin.cn/api/userinfo.do'
        
        return (self._post(params, user_info_url))

    def trade(self, symbol, trade_type, rate, amount):
        pass

    def cancel_order(self, order_id, symbol):
        pass

    def get_order(self, order_id, symbol):
        pass

    def error_code_meaning(self, error_code):
        codes = { 10000 : 'Required parameter can not be null',
                  10001 : 'Requests are too frequent',
                  10002 : 'System Error',
                  10003 : 'Restricted list request, please try again later',
                  10004 : 'IP restriction',
                  10005 : 'Key does not exist',
                  10006 : 'User does not exist',
                  10007 : 'Signatures do not match',
                  10008 : 'Illegal parameter',
                  10009 : 'Order does not exist',
                  10010 : 'Insufficient balance',
                  10011 : 'Order is less than minimum trade amount',
                  10012 : 'Unsupported symbol (not btc_cny or ltc_cny)',
                  10013 : 'This interface only accepts https requests' }
        return( codes[error_code] )
