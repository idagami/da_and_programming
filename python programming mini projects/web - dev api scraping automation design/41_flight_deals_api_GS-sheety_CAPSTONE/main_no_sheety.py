import requests, os, json, datetime, time
from dotenv import load_dotenv
from pprint import pprint
from requests.auth import HTTPBasicAuth
import flight_data, city_code_fill_search, notification_manager, amadeus_auth

current_dir = os.path.dirname(__file__)
load_dotenv()

cities_data_list = [
    {"city": "Auckland", "iata": "AKL", "max_price": 1000},
    {"city": "Vancouver", "iata": "YVR", "max_price": 700},
    {"city": "Calgary", "iata": "YYC", "max_price": 700},
    {"city": "Sacramento", "iata": "SMF", "max_price": 700},
    {"city": "Winnipeg", "iata": "YWG", "max_price": 700},
    {"city": "Minneapolis", "iata": "MSP", "max_price": 650},
    {"city": "San Francisco", "iata": "SFO", "max_price": 650},
    {"city": "Quebec", "iata": "YQB", "max_price": 600},
    {"city": "Seattle", "iata": "SEA", "max_price": 600},
    {"city": "Portland", "iata": "PDX", "max_price": 600},
    {"city": "Ottawa", "iata": "YOW", "max_price": 600},
    {"city": "Halifax", "iata": "YHZ", "max_price": 600},
    {"city": "Hartford", "iata": "BDL", "max_price": 500},
    {"city": "Philadelphia", "iata": "PHL", "max_price": 500},
    {"city": "Baltimore", "iata": "BWI", "max_price": 500},
    {"city": "Washington", "iata": "DCA", "max_price": 500},
    {"city": "Montreal", "iata": "YUL", "max_price": 470},
    {"city": "Toronto", "iata": "YYZ", "max_price": 460},
    {"city": "Boston", "iata": "BOS", "max_price": 450},
    {"city": "New York", "iata": "JFK", "max_price": 420},
    {"city": "Gdansk", "iata": "GDN", "max_price": 200},
    {"city": "Munich", "iata": "MUC", "max_price": 150},
    {"city": "Tbilisi", "iata": "TBS", "max_price": 120},
    {"city": "Chisinau", "iata": "KIV", "max_price": 150},
]


## ------- requests ----------- ##

## commented due to reaching limit at Sheety
# GS_ENDPOINT = (
#     "https://api.sheety.co/d5b632e2a361a5c17b69b9de0b5efedb/flightDeals/prices"
# )
# gs_headers_data = {
#     "Authorization": os.getenv("SHEETY_AUTHKEY"),
#     "Content-Type": "application/json",
# }

# gs_response = requests.get(url=GS_ENDPOINT, headers=gs_headers_data)
# gs_response.raise_for_status()
# gs_data_json = gs_response.json()
# sheet_data = gs_data_json["prices"]

# for row in sheet_data:
#     COUNTRY_ENDPOINT = f"{GS_ENDPOINT}/{row['id']}"
#     sheety_response = requests.get(
#         url=COUNTRY_ENDPOINT,
#         headers=gs_headers_data,
#     )
#     sheety_response.raise_for_status()
#     flight_results.flight_search(row["iatatest"])

flight_results = flight_data.FlightData()
all_flights = {}

for entry in cities_data_list:
    city = entry["city"]
    iata = entry["iata"]
    price = entry["max_price"]
    if not iata:
        print(f"skipping {city}")
        continue
    flights = flight_results.flight_search(iata, price)
    all_flights[city] = flights

file_loc1 = os.path.join(current_dir, "flights_results.json")
with open(file_loc1, "w", encoding="utf-8") as f:
    json.dump(all_flights, f, indent=2)

# cheapest_flight = {item.city: item.total_price for city[item] in all_flights.items()}

city_data_by_city_name = {
    city_data["city"]: city_data for city_data in cities_data_list
}

cheapest_flights = {}

for destination_city, flight_offers in all_flights.items():
    for flight_offer in flight_offers:
        if float(flight_offer["price"]["total"]) < float(
            city_data_by_city_name[destination_city]["max_price"]
        ):
            cheapest_flights[destination_city] = flight_offer["price"]["total"]

my_deals_loc = os.path.join(current_dir, "my_deals.json")
with open(my_deals_loc, "a", encoding="utf-8") as f:
    json.dump(cheapest_flights, f, indent=2)
    f.write(",\n")

send_mail = notification_manager.NotificationManager()
mail_body = ""
for a, b in cheapest_flights.items():
    line = f"Check the deals to your dream destinations:\n{a} : ${b}\n"
    mail_body += line

send_mail.sending_mail(mail_body)
