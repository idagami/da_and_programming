import requests, os
from dotenv import load_dotenv
from amadeus_auth import AmadeusAuth
import time

SHEETY_ENDPOINT = (
    "https://api.sheety.co/d5b632e2a361a5c17b69b9de0b5efedb/flightDeals/prices"
)
CITY_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"

load_dotenv()


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.getenv("AMADEUS_AK")
        self._api_secret = os.getenv("AMADEUS_SECRET")
        self.auth = AmadeusAuth()
        self._token = self.auth.get_token()

        print("FlightSearch initialized")

    def get_city_code(self):

        SHEETY_AUTHKEY = os.environ.get("SHEETY_AUTHKEY")
        sheety_headers_data = {
            "Authorization": SHEETY_AUTHKEY,
            "Content-Type": "application/json",
        }

        sheety_response = requests.get(url=SHEETY_ENDPOINT, headers=sheety_headers_data)
        sheety_response.raise_for_status()
        sheety_data_json = sheety_response.json()
        sheet_data = sheety_data_json["prices"]
        # print(sheet_data)

        amadeus_header = {"Authorization": f"Bearer {self._token}"}

        for row in sheet_data:
            COUNTRY_ENDPOINT = f"{SHEETY_ENDPOINT}/{row['id']}"
            city_params = {"keyword": row["city"]}

            if not row.get(
                "iatatest"
            ):  # if iata cell empty in sheet_data;  handles None, "", or missing key
                amadeus_response = requests.get(
                    url=CITY_ENDPOINT, params=city_params, headers=amadeus_header
                )
                if amadeus_response.status_code == 401:
                    self._token = self.auth.get_token()
                    amadeus_header = {"Authorization": f"Bearer {self._token}"}
                    amadeus_response = requests.get(
                        CITY_ENDPOINT, params=city_params, headers=amadeus_header
                    )

                # print("Amadeus raw response:", amadeus_response.status_code)
                # print(json.dumps(amadeus_response.json(), indent=2))
                amadeus_data = amadeus_response.json().get("data", [])
                if amadeus_data:
                    city_code = amadeus_data[0].get("iataCode")
                else:
                    city_code = None
                if city_code:  # = is not None
                    row["iatatest"] = city_code
                    edit_parameters = {"price": {"iatatest": city_code}}
                    sheety_response = requests.put(
                        url=COUNTRY_ENDPOINT,
                        headers=sheety_headers_data,
                        json=edit_parameters,
                    )
                    sheety_response.raise_for_status()
                    print(f"Updated row {row['id']} -> {city_code}")
                else:  # if amadeus cant find city code
                    print(f"No IATA found for {row['city']}")

                print(
                    f"Updated row {row['id']}: {sheety_response.status_code} {sheety_response.text}"
                )
            time.sleep(0.5)
        # finally:

        print(sheet_data)
