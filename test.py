# run this pip install first
#pip install alpaca-py
import datetime
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from secrets_utils import load_api_credentials
import ccxt
# print(ccxt.exchanges) # print a list of all available exchange classes
# print("asdf")

# Load credentials before creating the exchange client.
api_key, api_secret = load_api_credentials()
print("API Key:", api_key)
print("API Secret:", api_secret)
ex = ccxt.alpaca({"apiKey": api_key, "secret": api_secret})
t = ex.fetch_ticker('BTC/USDT')

# # No keys required for crypto data
# client = CryptoHistoricalDataClient()
# # Creating request object
# request_params = CryptoBarsRequest(
#   symbol_or_symbols=["BTC/USD"],
#   timeframe=TimeFrame.Day,
#   start=datetime.date(2022, 9, 1),
#   end=datetime.date(2022, 9, 7)
# )
# # Retrieve daily bars for Bitcoin in a DataFrame and printing it
# btc_bars = client.get_crypto_bars(request_params)

# # Convert to dataframe
# btc_bars.df
# print(btc_bars.df)

# print("API Key:", api_key)
# print("API Secret:", api_secret)