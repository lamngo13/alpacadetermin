from secrets_utils import load_api_credentials
from datetime import datetime
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.common.exceptions import APIError
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.enums import DataFeed

api_key, api_secret = load_api_credentials()

client = StockHistoricalDataClient(api_key, api_secret)

request = StockBarsRequest(
    symbol_or_symbols=["VOO"],
    timeframe=TimeFrame(1, TimeFrameUnit.Minute),
    start="2024-01-04",
    end="2024-01-05",
    limit=100,
    feed=DataFeed.IEX,
)
bars = client.get_stock_bars(request)

print(bars.df)