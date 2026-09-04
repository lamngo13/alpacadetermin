from secrets_utils import load_api_credentials
from datetime import datetime
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.common.exceptions import APIError
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

api_key, api_secret = load_api_credentials()

client = StockHistoricalDataClient(api_key, api_secret)

# Configure the request parameters
request_params = StockBarsRequest(
    symbol_or_symbols=["VOO"],
    timeframe=TimeFrame.Day,
    start=datetime(2025, 1, 1),
    end=datetime(2025, 1, 10)
)

# Request the data and convert it to a pandas DataFrame
try:
    bars = client.get_stock_bars(request_params)
except APIError as exc:
    raise RuntimeError(
        "Alpaca rejected the request. If your credentials are freshly regenerated, make sure you are using trading API keys rather than OAuth client credentials, and that they are loaded from APCA_API_KEY_ID/APCA_API_SECRET_KEY or secrets.env."
    ) from exc

df = bars.df

print(df.head())