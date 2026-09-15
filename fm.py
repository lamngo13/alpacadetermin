from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo

import exchange_calendars as xcals

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


# NYSE trading calendar
nyse = xcals.get_calendar("XNYS")


# Date range
start_date = date(2023, 1, 1)
end_date = datetime.now().date() - timedelta(days=1)

eastern = ZoneInfo("America/New_York")
utc = ZoneInfo("UTC")


# Get all NYSE trading sessions in our date range
sessions = nyse.sessions_in_range(
    start_date,
    end_date,
)


for session in sessions:

    # Convert session to a normal Python date
    current_date = session.date()

    # Get the actual NYSE open and close times for this day
    schedule = nyse.schedule.loc[session]

    market_open = schedule["open"].to_pydatetime()
    market_close = schedule["close"].to_pydatetime()

    # Make sure they are UTC-aware
    market_open = market_open.astimezone(utc)
    market_close = market_close.astimezone(utc)

    start_string = market_open.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_string = market_close.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Get number of bars actually in InfluxDB
    count_query = f"""
        SELECT COUNT(*) AS bar_count
        FROM stock_bars
        WHERE symbol = 'SPY'
          AND time >= '{start_string}'
          AND time < '{end_string}'
    """

    try:
        result = client.query(count_query)
        df = result.to_pandas()

        bar_count = int(df["bar_count"].iloc[0])

        # Expected number of 1-minute bars
        expected_count = int(
            (market_close - market_open).total_seconds() / 60
        )

        # If we have exactly the expected number, everything is good
        if bar_count == expected_count:
            continue

        print()
        print(
            f"{current_date} -> "
            f"{bar_count}/{expected_count} bars"
        )

        # Build every expected regular-session minute
        expected_times = []

        current_time = market_open

        while current_time < market_close:
            expected_times.append(current_time)
            current_time += timedelta(minutes=1)

        # Query timestamps that actually exist
        timestamp_query = f"""
            SELECT time
            FROM stock_bars
            WHERE symbol = 'SPY'
              AND time >= '{start_string}'
              AND time < '{end_string}'
            ORDER BY time
        """

        result = client.query(timestamp_query)
        timestamp_df = result.to_pandas()

        # Convert actual database timestamps to UTC
        actual_times = set()

        for timestamp in timestamp_df["time"]:

            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=utc)
            else:
                timestamp = timestamp.astimezone(utc)

            timestamp = timestamp.replace(
                second=0,
                microsecond=0,
            )

            actual_times.add(timestamp)

        # Find expected minutes that are missing
        missing_times = []

        for expected_time in expected_times:
            if expected_time not in actual_times:
                missing_times.append(expected_time)

        # Print missing minutes
        if missing_times:

            print("  Missing:")

            for missing_time in missing_times:

                eastern_time = missing_time.astimezone(eastern)

                print(
                    f"    {eastern_time.strftime('%H:%M %Z')}"
                )

        else:
            print("  No missing timestamps found.")

    except Exception as error:
        print(f"{current_date} -> ERROR: {error}")


client.close()

print()
print("Done.")