from secrets_utils import load_api_credentials
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


#we want to use an auth token IFF its expired
def get_token_for_market_data():
    #get secrets (we can totes do this everytime bc its local)
    client_id, client_secret = load_api_credentials()

    if not client_id or not client_secret:
        raise ValueError("Missing client credentials")

    payload = urlencode(
        {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
    ).encode("utf-8")

    req = Request(
        "https://authx.alpaca.markets/v1/oauth2/token",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    with urlopen(req, timeout=15) as response:
        response_body = response.read().decode("utf-8")
        print("Response body:", response_body)  # Debugging line

    return json.loads(response_body)



