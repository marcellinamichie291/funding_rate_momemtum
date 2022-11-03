import ccxt
import pandas as pd
from datetime import datetime,timedelta

ftx=ccxt.ftx({
            "apiKey":'apiKey',
            "secret":'secretKey',
            'headers':{
                'FTX-SUBACCOUNT':'subaccountName'
            }
        })
tf='1h'

def get_liquid_symbols():
    markets=ftx.load_markets()
    markets=pd.DataFrame(markets)
    markets=markets.T
    markets=markets[markets['id'].str.contains('PERP')]
    symbols=markets['id'].to_list()
    onehago=datetime.now()-timedelta(hours=6)
    onehago=onehago.timestamp()*1000
    volumes=[]
    for symbol in symbols:
        df=ftx.fetch_ohlcv(symbol,timeframe=tf,since=onehago,limit=5)
        df=pd.DataFrame(df)
        df.columns=['timestamp','open','high','low','close','volume']
        df['timestamp']=[datetime.fromtimestamp((x/1000)) for x in df['timestamp']]
        df=df.set_index('timestamp')
        volumes.append(df['volume'].median())
    volumes=pd.DataFrame(volumes)
    quantile=volumes.quantile(.75)
    quantile=quantile[0]
    volumes=volumes[0].to_list()
    volumes=[v>=quantile for v in volumes]
    markets=markets[volumes]
    return markets['id'].to_list()