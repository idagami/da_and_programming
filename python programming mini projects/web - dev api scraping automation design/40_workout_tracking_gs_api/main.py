import requests
import os
import json
import datetime
import time
from dotenv import load_dotenv

#  free trial has expired

load_dotenv()
nutr_app_id = os.getenv("NUTR_APPID")
nutr_api_key = os.getenv("NUTR_APIKEY")
print("APP ID:", nutr_app_id)
print("API KEY:", nutr_api_key)

## ----------- NUTRONIX data ---------- ##


NUT_EXERC_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

user_input = input("Tell me which exercises you did: ")

nutr_headers_data = {"x-app-id": nutr_app_id, "x-app-key": nutr_api_key}
nutr_parameters = {
    "query": user_input,
    "gender": "female",
    "weight_kg": 61,
    "height_cm": 168.5,
    "age": 35,
}

input_response = requests.post(
    url=NUT_EXERC_ENDPOINT, json=nutr_parameters, headers=nutr_headers_data
)
# print(response.text)
print(input_response)  # returns status only, like: <Response [200]>
# print(response.status_code)  # 200
input_response.raise_for_status()
input_data_json = input_response.json()
# print(data_json)
print(json.dumps(input_data_json, indent=2))  # proper json format, visually readable

## ----------- date and time data ---------- ##
today_date_str = datetime.datetime.now().strftime("%Y-%m-%d")
today_time_str = datetime.datetime.now().time().strftime("%H:%M:%S")
# today_date_str = str(datetime.datetime.now().date())
# today_time_str = str(datetime.datetime.now().time()).split(sep=".")[0]


## ----------- Sheety data ---------- ##
GS_ENDPOINT = (
    "https://api.sheety.co/d5b632e2a361a5c17b69b9de0b5efedb/myWorkouts/workouts"
)

GS_AUTHKEY = os.getenv("GS_AUTHKEY")

gs_headers_data = {
    "Authorization": GS_AUTHKEY,
    "Content-Type": "application/json",
}

# gs_parameters = { # manual line insertion
#     "workout": {
#         "date": "2021-07-21",
#         "time": "16:00:00",
#         "exercise": "Swimming",
#         "duration": 22,
#         "calories": 200,
#     }
# }

for entry in input_data_json["exercises"]:
    gs_parameters = {  # inserting data analyzed by nutrioniz from user input
        "workout": {
            "date": today_date_str,
            "time": today_time_str,
            "exercise": entry["name"],
            "duration": entry["duration_min"],
            "calories": entry["nf_calories"],
        }
    }
    gs_response = requests.post(
        url=GS_ENDPOINT, json=gs_parameters, headers=gs_headers_data
    )
    print(gs_response.text)
    print(gs_response.status_code)
    gs_response.raise_for_status()
    gs_data_json = gs_response.json()
    print(json.dumps(gs_data_json, indent=2))
    time.sleep(0.5)  # small pause (avoid hammering API; optional)
