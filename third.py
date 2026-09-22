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
WITH base AS (
    SELECT
        time AS bar_time,
        time AT TIME ZONE 'America/New_York' AS eastern_time,
        trade_count,
        volume,
        vwap
    FROM stock_bars
    WHERE symbol = 'SPY'
      AND time >= '2023-01-01T00:00:00Z'
)

SELECT
    b.eastern_time AS time,
    b.trade_count,
    b.volume,
    b.vwap,

    ((b15.vwap / b.vwap) - 1) * 100 AS gain_15m,
    ((b30.vwap / b.vwap) - 1) * 100 AS gain_30m,
    ((b60.vwap / b.vwap) - 1) * 100 AS gain_60m,
    ((b120.vwap / b.vwap) - 1) * 100 AS gain_120m

FROM base b

LEFT JOIN base b15
    ON b15.bar_time = b.bar_time + INTERVAL '15 minutes'

LEFT JOIN base b30
    ON b30.bar_time = b.bar_time + INTERVAL '30 minutes'

LEFT JOIN base b60
    ON b60.bar_time = b.bar_time + INTERVAL '60 minutes'

LEFT JOIN base b120
    ON b120.bar_time = b.bar_time + INTERVAL '120 minutes'

WHERE
    EXTRACT(HOUR FROM b.eastern_time) * 60
        + EXTRACT(MINUTE FROM b.eastern_time)
        >= 9 * 60 + 45

    AND EXTRACT(HOUR FROM b.eastern_time) * 60
        + EXTRACT(MINUTE FROM b.eastern_time)
        <= 13 * 60

ORDER BY b.bar_time
"""

result = client.query(query)
df = result.to_pandas()

print(df)

client.close()