import requests, os
from dotenv import load_dotenv
import data_manager


load_dotenv()

SHEETY_PRICES_ENDPOINT = (
    "https://api.sheety.co/d5b632e2a361a5c17b69b9de0b5efedb/flightDeals/prices"
)
SHEETY_USERS_ENDPOINT = (
    "https://api.sheety.co/d5b632e2a361a5c17b69b9de0b5efedb/flightDeals/users"
)


class SheetyDataManager:
    def __init__(self):
        self.sheety_authkey = os.getenv("SHEETY_AUTHKEY")
        self.headers = {
            "Authorization": self.sheety_authkey,
            "Content-Type": "application/json",
        }

    def get_prices(self):
        sheety_response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=self.headers)
        sheety_response.raise_for_status()
        sheety_data_json = sheety_response.json()
        sheet_data = sheety_data_json["prices"]
        return sheet_data

    def get_client_emails(self):
        sheety_response = requests.get(url=SHEETY_USERS_ENDPOINT, headers=self.headers)
        sheety_response.raise_for_status()
        sheety_data_json = sheety_response.json()
        sheet_data = sheety_data_json["users"]
        # print(sheet_data)
        # When I pull data from Sheety, the keys in the JSON don’t keep spaces. Instead, they usually become camelCase or something like this:
        emails = [user["enterYourEmail"] for user in sheet_data]
        return emails


# emails_list = get_client_email()
# print(emails_list)
