import ccxt
import pandas as pd
from datetime import datetime,timedelta
from datetime import datetime,timedelta
from get_liquid_pairs import get_liquid_symbols

ftx=ccxt.ftx({
            "apiKey":'apiKey',
            "secret":'secretKey',
            'headers':{
                'FTX-SUBACCOUNT':'subaccountName'
            }
        })
tf='1h'
symbols=get_liquid_symbols()

def get_best_fr(hours_val):
    fr_lst=[]
    onehago=datetime.now()-timedelta(hours=hours_val)
    onehago=onehago.replace(second=0, microsecond=0, minute=0, hour=onehago.hour)+timedelta(hours=onehago.minute//30)
    onehago=onehago.timestamp()*1000
    for symbol in symbols:
        fr=ftx.fetch_funding_rate_history(symbol,since=onehago,limit=1)
        fr=pd.DataFrame(fr)
        fr['timestamp']=[datetime.fromtimestamp((x/1000)) for x in fr['timestamp']]
        fr_lst.append(fr)
    fr_lst=[[x['fundingRate'][0],x['symbol'][0]] for x in fr_lst]
    fr_df=pd.DataFrame(fr_lst)
    fr_df.columns=['fundingRate','symbol']
    lower=fr_df.nsmallest(5,'fundingRate')
    higher=fr_df.nlargest(5,'fundingRate')
    return(lower,higher)