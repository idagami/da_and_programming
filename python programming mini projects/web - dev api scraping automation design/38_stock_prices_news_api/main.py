import requests, os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from datetime import datetime as dt
from datetime import timedelta as td


STOCK_CODE = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_api_key = os.getenv("AA_APPID")
news_api_key = os.getenv("NEWSAPI_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
my_phone = os.getenv("MY_PHONE")
twilio_phone = os.getenv("TWILIO_PHONE")

today = dt.now().date()
yesterday = today - td(days=2)  # market was closed on saturday, so going back 2 days
db_yesterday = yesterday - td(days=1)

parameters_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_CODE,
    "apikey": stock_api_key,
}
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {  # type: ignore
    "http": os.environ.get("http_proxy"),
    "https": os.environ.get("https_proxy"),
}

response_stock = requests.get(url=STOCK_ENDPOINT, params=parameters_stock)
print(response_stock.status_code)
response_stock.raise_for_status()
data_json = response_stock.json()
# print(data_json)

time_series = data_json["Time Series (Daily)"]

# get trading dates sorted (newest first)
dates = sorted(time_series.keys(), reverse=True)

latest_day = dates[0]
previous_day = dates[1]

yest_clos = float(time_series[latest_day]["4. close"])
db_yest_clos = float(time_series[previous_day]["4. close"])


daily_change = round((yest_clos - db_yest_clos) / db_yest_clos, 4)

if daily_change < 0:
    sign = "↘️"
else:
    sign = "↗️"

# if 1 < 3:  # testing purpose, no access to stock info
#     sign = "↘️"
# else:
#     sign = "↗️"

parameters_news = {
    "q": COMPANY_NAME,  # alternatively: "qInTitle": COMPANY_NAME
    "from": yesterday,
    "language": "en",
    "apiKey": news_api_key,
}
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

response_news = requests.get(url=NEWS_ENDPOINT, params=parameters_news)
print(response_news.status_code)
response_news.raise_for_status()
data_json = response_news.json()
# print(data_json)


def send_msg():
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        from_=f"whatsapp:{twilio_phone}",
        to=f"whatsapp:{my_phone}",
        body=f"TSLA: {sign} {round(daily_change * 100,1)}%\n",
    )
    print(message.sid, message.status)


rapid_change = False
if abs(daily_change) > 0.05:
    rapid_change = True
    msgs = [
        f"Headline: {item['title']}\nBrief: {item['description']}"
        for item in data_json["articles"][:3]
    ]

    for msg in msgs:
        send_msg()

# if abs(-0.0216) > 0.01:  # testing purposes
#     rapid_change = True
#     msgs = [
#         f"Headline: {item['title']}\nBrief: {item['description']}"
#         for item in data_json["articles"][:2]
#     ]

#     for msg in msgs:
#         send_msg()


## getting top 3 freshest articles
# import pandas as pd

# # assume `data` is the parsed JSON dict you got from the API:
# # data = response.json()
# articles = data["articles"]

# df = pd.json_normalize(articles)              # flattens nested fields like source.name
# df["publishedAt_dt"] = pd.to_datetime(df["publishedAt"], utc=True, errors="coerce")
# df = df.dropna(subset=["publishedAt_dt"])     # drop if publishedAt missing or unreadable
# df = df.sort_values("publishedAt_dt", ascending=False)

# top3 = df.head(3)[["publishedAt","publishedAt_dt","source.name","title","author","url"]]
# top3 = top3.rename(columns={"source.name":"source_name"})
# print(top3.to_string(index=False))
