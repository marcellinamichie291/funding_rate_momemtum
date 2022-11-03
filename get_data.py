import ccxt
import pandas as pd
from get_lower_higher_pairs import get_best_fr
import matplotlib.pyplot as plt
ftx=ccxt.ftx({
            "apiKey":'apiKey',
            "secret":'secretKey',
            'headers':{
                'FTX-SUBACCOUNT':'subaccountName'
            }
        })
tf='1h'
(lower,higher)=get_best_fr()
low_symbols=lower['symbol'].to_list()
high_symbols=higher['symbol'].to_list()
for symbol in low_symbols,high_symbols:
    symbol=symbol.replace('/USD:USD','-PERP')
print(symbol)
