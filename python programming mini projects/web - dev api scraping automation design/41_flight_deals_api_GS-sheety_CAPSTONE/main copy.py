import requests, os, json
from dotenv import load_dotenv
import city_code_fill_search, flight_data, notification_manager, data_manager

current_dir = os.path.dirname(__file__)
load_dotenv()

# # uncomment below 2 lines only in need to fill the iata codes in GS, as its eating Sheety traffic
# fs = city_code_fill_search.FlightSearch()
# fs.get_city_code()

sheety_manager = data_manager.SheetyDataManager()
sheet_data = sheety_manager.get_prices()

all_flights = {}

for row in sheet_data:
    flight_results = flight_data.FlightData()
    flights = flight_results.flight_search(row["iatatest"], row["maxPrice"])
    all_flights[row["city"]] = flights


file_loc1 = os.path.join(current_dir, "flights_results.json")
with open(file_loc1, "a", encoding="utf-8") as f:
    json.dump(all_flights, f, indent=2)

# ------- Find cheapest flights ----------- #
city_price_map = {row["city"]: row["maxPrice"] for row in sheet_data}

cheapest_flights = {}
for destination_city, flight_offers in all_flights.items():
    for flight_offer in flight_offers:
        if float(flight_offer["price"]["total"]) < float(
            city_price_map[destination_city]
        ):
            cheapest_flights[destination_city] = flight_offer["price"]["total"]
            break  # as i sorted the best deals ASC, i just take the first one from list and no need to continue iterating


my_deals_loc = os.path.join(current_dir, "my_deals.json")
with open(my_deals_loc, "a", encoding="utf-8") as f:
    json.dump(cheapest_flights, f, indent=2)
    f.write(",\n")

send_mail = notification_manager.NotificationManager()
mail_body = ""
for a, b in cheapest_flights.items():
    line = f"Check the deals to your dream destinations:\nDirect and indirect flights:\n{a} : ${b}\n\n"
    mail_body += line

send_mail.sending_mail(mail_body)
