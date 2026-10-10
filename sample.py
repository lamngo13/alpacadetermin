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
#this is for a single day
#TODO lets implement one day at a time, and then loop LATER
#TODO figure out when trading day opens (I have no idea if this is EST or what its 24 hr)

#TODO maybe we can start by considering a given time and then looking back to see the gains
#TODO it should be deterministic and dummy simple at first

#TODO this might be hard, but it doesn't have to be strictly comprehensive
#and that's tricky bc how can we find near misses??

#TODO maybe after this query we can just do pandas df stuff and not mess w the db

result = client.query(sample_query)
df = result.to_pandas()

print(df)

client.close()