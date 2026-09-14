from secrets_utils import load_api_credentials, load_db_secret
from datetime import datetime
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.common.exceptions import APIError
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.enums import DataFeed
from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime, timedelta
import time

#creds setup
api_key, api_secret = load_api_credentials()
YOUR_INFLUX_TOKEN = load_db_secret()

#client setup w creds
client = StockHistoricalDataClient(api_key, api_secret)

#date setup
first_date = datetime(2023, 1, 1)
today = datetime.now() #this will be datetime.now() in the future

current_date = first_date

#big loop to loop until today
while current_date < today:
    #iterate next_date
    next_date = current_date + timedelta(days=1)
    request = StockBarsRequest(
        symbol_or_symbols=["SPY"],
        timeframe=TimeFrame(1, TimeFrameUnit.Minute),
        start=current_date.strftime("%Y-%m-%d"),
        end=next_date.strftime("%Y-%m-%d"),
        limit=10000, #i think its ballpark 900 anyway - also includes aftermarket i think
        feed=DataFeed.SIP,
    )
    #make request and put it in dataframe
    try:
        bars = client.get_stock_bars(request)
        df = bars.df
    except APIError as error:
        print(f"Client error: {error}. Retrying...")
        time.sleep(10)
        continue

    #ITERATE CURRENT DAY
    current_date = next_date

    #print for fun
    print(current_date.strftime("%Y-%m-%d"))
    print(df)



    influx_client = InfluxDBClient3(
        host="http://localhost:8181",
        database="voo",
        token=YOUR_INFLUX_TOKEN,
        timeout=60000, #default is 8 seconds so we increase
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
    #SLEEP
    time.sleep(1)