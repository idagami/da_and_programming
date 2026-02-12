import requests, os
from dotenv import load_dotenv


load_dotenv()

SHEETY_ENDPOINT = (
    "https://api.sheety.co/d5b632e2a361a5c17b69b9de0b5efedb/flightDeals/users"
)

SHEETY_AUTHKEY = os.environ.get("SHEETY_AUTHKEY")
sheety_headers_data = {
    "Authorization": SHEETY_AUTHKEY,
    "Content-Type": "application/json",
}


def get_client_email():
    sheety_response = requests.get(url=SHEETY_ENDPOINT, headers=sheety_headers_data)
    sheety_response.raise_for_status()
    sheety_data_json = sheety_response.json()
    sheet_data = sheety_data_json["users"]
    # print(sheet_data)
    # When I pull data from Sheety, the keys in the JSON don’t keep spaces. Instead, they usually become camelCase or something like this:
    emails = [user["enterYourEmail"] for user in sheet_data]
    return emails


emails_list = get_client_email()
print(emails_list)
