import os
import time
import requests
from dotenv import load_dotenv

# ## ------- getting a token ----------- ##

load_dotenv()


class AmadeusAuth:
    def __init__(self):
        self.client_id = os.getenv("AMADEUS_AK")
        self.client_secret = os.getenv("AMADEUS_SECRET")
        self.token = None
        self.expiry_time = 0

    def get_token(self):
        if self.token is None or self.is_expired():
            self.token = self._fetch_new_token()
        return self.token

    def _fetch_new_token(self):
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(url, data=data, headers=headers)
        # In Amadeus docs, they say the body must be sent as x-www-form-urlencoded,
        # # Use 'data=' instead of json=, since requests will then encode it properly as form data.
        response.raise_for_status()
        token_data = response.json()

        self.expiry_time = time.time() + token_data["expires_in"]
        return token_data["access_token"]

    def is_expired(self):
        return time.time() >= self.expiry_time


# print(json.dumps(input_data_json, indent=2))
