A system to search for cheap flights to multiple destinations and notify users of deals.
Free testing Amadeus version has a very limited hub airports pool. i.e. TLV is not in it. 
So prject built on searching cheap flights from CDG.

Core Features:
Flight Search:
Uses a custom FlightData class to query flight prices via an external API.
Collects all flights and filters for the cheapest deals per destination.
Results saved locally in JSON files (flights_results.json, my_deals.json).

Notification System:
Uses a NotificationManager class to send email alerts with the cheapest deals.
Email body is dynamically generated with flight price and city information.

Data Sources:
A. With Sheety (Google Sheet API)
Reads city IATA codes and max prices directly from a Google Sheet via Sheety.
Can optionally fill missing IATA codes in the sheet using FlightSearch.
Minimizes hardcoding and allows non-technical users to update destinations in the Sheet.
Advantage: dynamic and maintainable; disadvantage: uses API calls / limits daily traffic.

B. Without Sheety (Hardcoded Cities List)
City names, IATA codes, and max prices are stored in a Python list of dictionaries.
All operations (flight search, cheapest price filtering, notifications) run locally without fetching from Sheety.
Advantage: no external API limits; disadvantage: changes require editing the code.

Workflow (Both Versions):
Fetch city data (from Sheet or hardcoded list).
For each city, search for available flights below the max price.
Save all flight results to flights_results.json.
Identify cheapest flights that meet the price criteria.
Save these cheapest flights to my_deals.json.
Compose and send email notifications with flight deals.

Notes:
In the Sheety version, two lines allow automatic IATA code filling for destinations with missing codes.
Both versions generate identical output files (flights_results.json and my_deals.json) for further processing.
Notification email text dynamically adapts to the city names and lowest prices found.