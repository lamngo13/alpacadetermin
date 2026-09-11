from secrets_utils import load_api_credentials, load_db_secret
from datetime import datetime
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.common.exceptions import APIError
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.enums import DataFeed
from influxdb_client_3 import InfluxDBClient3, Point

api_key, api_secret = load_api_credentials()

YOUR_INFLUX_TOKEN = load_db_secret()

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

df = bars.df

influx_client = InfluxDBClient3(
    host="http://localhost:8181",
    database="voo",
    token=YOUR_INFLUX_TOKEN,
)

points = []
for (symbol, timestamp), row in df.iterrows():
    point = (
        Point("stock_bars")
        .tag("symbol", symbol)
        .field("open", float(row["open"]))
        .field("high", float(row["high"]))
        .field("low", float(row["low"]))
        .field("close", float(row["close"]))
        .field("volume", float(row["volume"]))
        .field("trade_count", float(row["trade_count"]))
        .field("vwap", float(row["vwap"]))
        .time(timestamp)
    )

    points.append(point)


influx_client.write(points)


influx_client.close()

print(f"Wrote {len(df)} rows to InfluxDB")