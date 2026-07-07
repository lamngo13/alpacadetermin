# run this pip install first
#pip install alpaca-py
import datetime
import os
from pathlib import Path
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame


def load_secrets_env(file_path: str) -> dict:
  secrets = {}
  if not Path(file_path).exists():
    return secrets
  for line in Path(file_path).read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
      continue
    key, value = line.split("=", 1)
    secrets[key.strip()] = value.strip()
  return secrets


def load_api_credentials() -> tuple[str, str]:
  # Prefer real shell environment variables exported in terminal.
  api_key = os.getenv("APCA_API_KEY_ID", "")
  api_secret = os.getenv("APCA_API_SECRET_KEY", "")

  if api_key and api_secret:
    return api_key, api_secret

  # Fallback to values from secrets.env.
  secrets = load_secrets_env("secrets.env")
  api_key = api_key or secrets.get("APCA-API-KEY-ID", "")
  api_secret = api_secret or secrets.get("APCA-API-SECRET-KEY", "")
  return api_key, api_secret

# No keys required for crypto data
client = CryptoHistoricalDataClient()
# Creating request object
request_params = CryptoBarsRequest(
  symbol_or_symbols=["BTC/USD"],
  timeframe=TimeFrame.Day,
  start=datetime.date(2022, 9, 1),
  end=datetime.date(2022, 9, 7)
)
# Retrieve daily bars for Bitcoin in a DataFrame and printing it
btc_bars = client.get_crypto_bars(request_params)

# Convert to dataframe
btc_bars.df
print(btc_bars.df)

#testing, print api key and secret
api_key, api_secret = load_api_credentials()

print("API Key:", api_key)
print("API Secret:", api_secret)