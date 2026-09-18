from secrets_utils import load_db_secret
from influxdb_client_3 import InfluxDBClient3


# InfluxDB setup
INFLUX_TOKEN = load_db_secret()

client = InfluxDBClient3(
    host="http://localhost:8181",
    database="voo",
    token=INFLUX_TOKEN,
    timeout=60000,
)


# Day to query, in "YYYY-MM-DD" format
target_date = "2024-01-03"

query = f"""
    SELECT *
    FROM stock_bars
    WHERE symbol = 'SPY'
      AND time >= '{target_date}T00:00:00Z'
      AND time < '{target_date}T23:59:59Z'
    ORDER BY time
"""

result = client.query(query)
df = result.to_pandas()

print(df)

client.close()