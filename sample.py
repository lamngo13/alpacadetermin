from secrets_utils import load_db_secret
from influxdb_client_3 import InfluxDBClient3
from datetime import datetime, timedelta


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

#TODO honestly lets just start at 2 pm and go back
#TODO we can start dummy simple
#TODO what are we looking for in the last 3 hrs from given date?
# we are looking for gains


start_time = f"{target_date}T14:00:00Z"
for i in range(0, 180, 1):
    current_time = (datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ") - timedelta(minutes=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
    print("current_time:", current_time)

exit(0)




#NOTE can uncomment this
#print(df)

client.close()