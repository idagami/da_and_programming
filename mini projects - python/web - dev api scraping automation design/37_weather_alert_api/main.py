import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os
from dotenv import load_dotenv

load_dotenv()

HOME_TUPLE = (32.016499, 34.750278)
api_key = os.environ.get("OPENWEATHER_APPID")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
my_phone = os.getenv("MY_PHONE")
twilio_phone = os.getenv("TWILIO_PHONE")

parameters = {
    "lat": HOME_TUPLE[0],
    "lon": HOME_TUPLE[1],
    "units": "metric",  # to display temp in Celcius
    "cnt": 16,  # we want 16 x 3-hour forecasts, for next 2 days
    "appid": api_key,
}

# added below as per Twilio request
proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {  # type: ignore
    "http": os.environ.get("http_proxy"),
    "https": os.environ.get("https_proxy"),
}
# client = Client(account_sid, auth_token)

endpoint = "https://api.openweathermap.org/data/2.5/forecast"

response = requests.get(url=endpoint, params=parameters)
print(response.status_code)
response.raise_for_status()
data_json = response.json()
# print(data_json)

weather_condition = data_json["list"][0]["weather"][0][
    "id"
]  # slicing list with 'int', slicing dict with 'key'

will_rain = False
serious_weather = False
message = []
for item in data_json["list"]:
    dt = item["dt_txt"]
    weather_condition = int(item["weather"][0]["id"])
    weather_descr = item["weather"][0]["description"]
    if weather_condition < 700 or weather_condition > 800:
        # will_rain = True
        print(dt, weather_condition, weather_descr)
    elif 799 >= weather_condition >= 700:
        serious_weather = True
        # print("Serious atmospheric condition is coming!")
    else:
        print(f"{dt} - good weather expected")
    message.append(dt)
    message.append(weather_descr)


if serious_weather:
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        from_=f"whatsapp:{twilio_phone}",
        to=f"whatsapp:{my_phone}",  # has to be phone number i verified on twilio website
        body=f"{message}",
    )
    print(message.sid, message.status)
