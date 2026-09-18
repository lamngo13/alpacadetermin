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

sample_query = f"""
    SELECT *
    FROM stock_bars
    WHERE symbol = 'SPY'
      AND time >= '{target_date}T00:00:00Z'
      AND time < '{target_date}T23:59:59Z'
    ORDER BY time
"""

query = f"""
SELECT
    time,
    close,
    future_max_high,
    ((future_max_high - close) / close) * 100 AS future_gain_pct
FROM (
    SELECT
        time,
        close,
        MAX(high) OVER (
            ORDER BY time
            RANGE BETWEEN CURRENT ROW AND INTERVAL '1 hour' FOLLOWING
        ) AS future_max_high
    FROM stock_bars
    WHERE
        symbol = 'SPY'
        AND CAST(time AT TIME ZONE 'America/New_York' AS TIME) >= TIME '10:00:00'
)
WHERE
    ((future_max_high - close) / close) * 100 >= 0.25
ORDER BY time;
"""

result = client.query(query)
df = result.to_pandas()

print(df)

client.close()