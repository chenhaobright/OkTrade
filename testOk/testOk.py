import okcoin

partner = 3296386123
secret_key = '3DD45E548EB7586153F589250150CD1ED54'

T = okcoin.TradeAPI(partner, secret_key)

# Get acccount info

# Structure: { u'info':
#               { u'funds':
#                   { u'freezed': {u'ltc': 0, u'btc': 0, u'cny': 0},
#                     u'free': {u'ltc': 0, u'btc': 0, u'cny': 0}
#                   }
#               },
#              u'result': True }

print( T.get_info() )

# Trade - Buy example

trade_result_obj = T.trade('btc_cny','buy','1000','0.1')
print( trade_result_obj )

# Get btc_cny ticker
# -> partner and secret_key not needed

M = okcoin.MarketData()

print( M.ticker('btc_cny').bids, m.ticker('btc_cny').ask )

# Get btc_cny bid depth

print( M.get_depth('btc_cny').bids )

# Get btc_cny trade history

print( M.get_history('btc_cny') )
