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

# Start at 11:30 and identify gains from 9:30 to 11:30.
# Identify (average?) gains and determine what is a ‘good’ gain (maybe with a gain from 9:30 to 11:30 greater than a certain number or percentage?
# Start with just that lol
#TODO put those gains into a separate dataframe

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