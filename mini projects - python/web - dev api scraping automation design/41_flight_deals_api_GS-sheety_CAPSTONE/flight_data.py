import requests, os, json, datetime
from amadeus_auth import AmadeusAuth


current_dir = os.path.dirname(__file__)


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.auth = AmadeusAuth()
        self._token = self.auth.get_token()

    def flight_search(self, destination, max_price):
        today_full = datetime.date.today()
        dept_date_str = (today_full + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        return_date_str = (today_full + datetime.timedelta(days=7)).strftime("%Y-%m-%d")

        FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

        deal_params = {
            "originLocationCode": "PAR",
            "destinationLocationCode": destination,
            "departureDate": dept_date_str,
            "returnDate": return_date_str,
            "adults": 1,
            "currencyCode": "USD",
            "maxPrice": max_price,
        }
        deal_headers = {"Authorization": f"Bearer {self._token}"}

        response = requests.get(
            url=FLIGHT_ENDPOINT, headers=deal_headers, params=deal_params, timeout=30
        )
        response.raise_for_status()
        data = response.json()
        print("Status:", response.status_code)
        # print("Response:", response.text)
        # print(data)

        # nonstop_flights = []
        # for row in data["data"]:
        #     if (
        #         len(row["itineraries"][0]["segments"]) == 1
        #         and len(row["itineraries"][1]["segments"]) == 1
        #     ):
        #         nonstop_flights.append(row)

        # file_loc = os.path.join(current_dir, "amadeus_search.json")
        # with open(file_loc, "w", encoding="utf-8") as file:
        #     json.dump(nonstop_flights, file, indent=2)
        # print(f"{len(nonstop_flights)} responses saved to file.")
        # return nonstop_flights

        nonstop_flights = []
        nondirect_flights = []
        for row in data["data"]:
            if (
                len(row["itineraries"][0]["segments"]) == 1
                and len(row["itineraries"][1]["segments"]) == 1
            ):
                nonstop_flights.append(row)
            else:
                nondirect_flights.append(row)

        file_loc = os.path.join(current_dir, "amadeus_search_dir.json")
        with open(file_loc, "w", encoding="utf-8") as file_dir:
            json.dump(nonstop_flights, file_dir, indent=2)

        file_loc1 = os.path.join(current_dir, "amadeus_search_nondir.json")
        with open(file_loc1, "w", encoding="utf-8") as file_nondir:
            json.dump(nondirect_flights, file_nondir, indent=2)
        print(
            f"{len(nonstop_flights)} responses for direct flights and {len(nondirect_flights)} responses for nondirect flights saved to file."
        )
        all_flights_list = nonstop_flights + nondirect_flights

        all_flights_list.sort(key=lambda x: float(x["price"]["total"]))

        if all_flights_list:
            cheapest_flight = all_flights_list[0]
            print(f"Cheapest flight: {cheapest_flight['price']['total']}")
            # all_flights_list = cheapest_flight
        else:
            print("No flights found.")
            # all_flights_list = []  # ensure a list is returned

        return all_flights_list
