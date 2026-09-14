from secrets_utils import load_api_credentials, load_db_secret

from datetime import datetime

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.common.exceptions import APIError
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.enums import DataFeed

from influxdb_client_3 import InfluxDBClient3, Point


# creds setup
api_key, api_secret = load_api_credentials()
YOUR_INFLUX_TOKEN = load_db_secret()


# client setup
client = StockHistoricalDataClient(api_key, api_secret)


# ONE DAY TEST
start_date = "2026-09-11"
end_date = "2026-09-12"


request = StockBarsRequest(
    symbol_or_symbols=["SPY"],
    timeframe=TimeFrame(1, TimeFrameUnit.Minute),
    start=start_date,
    end=end_date,
    limit=10000,
    feed=DataFeed.SIP,
)


# make request
try:
    bars = client.get_stock_bars(request)
    df = bars.df

except APIError as error:
    print(f"Client error: {error}")
    exit()


# print results
print(df)
print(f"\nReceived {len(df)} rows")