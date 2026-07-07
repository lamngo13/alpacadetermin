import os
from pathlib import Path


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


def load_api_credentials(secrets_file: str = "secrets.env") -> tuple[str, str]:
  # Prefer real shell environment variables exported in terminal.
  api_key = os.getenv("APCA_API_KEY_ID", "")
  api_secret = os.getenv("APCA_API_SECRET_KEY", "")

  if api_key and api_secret:
    return api_key, api_secret

  # Fallback to values from secrets file.
  secrets = load_secrets_env(secrets_file)
  api_key = api_key or secrets.get("APCA-API-KEY-ID", "")
  api_secret = api_secret or secrets.get("APCA-API-SECRET-KEY", "")
  return api_key, api_secret
