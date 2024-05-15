import pandas as pd
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
import pandas as pd

# No keys required for crypto data
client = CryptoHistoricalDataClient()

# gathered from: https://coinmarketcap.com/all/views/all/

# cryptocurrencies = ["BTC/USD", "ETH/USD", "ADA/USD", "XRP/USD", "DOGE/USD", "LTC/USD"]  # Add more symbols as needed
cryptocurrencies = [
    "BTC/USD"


]

allDFs = []

#creating request object for each crypto name
for currency in cryptocurrencies:
    params = CryptoBarsRequest(
        symbol_or_symbols=[currency],
        timeframe=TimeFrame.Day,
        start=datetime(2021, 2, 5).isoformat() + "Z",
        end=datetime(2023,1, 10).isoformat() + "Z"
    )

    # get daily bars for cryptocurrency in params 
    bars = client.get_crypto_bars(params)
    df = bars.df.reset_index()
    
    df['cryptoName'] = currency
    
    #add this currencie's df to list of all curencies 
    allDFs.append(df)

resultDF = pd.concat(allDFs, ignore_index=True)

#date too long so I reformatted it 
resultDF['Date'] = resultDF['timestamp'].dt.strftime('%m/%d/%Y')
resultDF.rename(columns={'Date': 'date'}, inplace=True)
resultDF['average'] = (resultDF['high'] + resultDF['low']) /2
resultDF = resultDF[['cryptoName','date', 'open', 'close', 'high', 'low', 'average', 'volume', 'trade_count', 'vwap', 'timestamp']]



#save to csv :)
resultDF.to_csv('bitcoin.csv', index=False)
