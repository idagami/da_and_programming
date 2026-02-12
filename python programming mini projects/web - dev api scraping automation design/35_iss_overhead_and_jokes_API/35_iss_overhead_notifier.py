import requests, datetime, smtplib, time, os
from dotenv import load_dotenv

load_dotenv()

HOME_TUPLE = (32.016499, 34.750278)

## -------------- ISS position -------- ##


def iss_overhead_check():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data_json = response.json()

    iss_latitude = float(
        data_json["iss_position"]["latitude"]
    )  # originally json gives a string
    iss_longitude = float(data_json["iss_position"]["longitude"])

    print(iss_latitude, iss_longitude)
    if abs(iss_latitude - HOME_TUPLE[0]) < 5 and abs(iss_longitude - HOME_TUPLE[1]) < 5:
        # Your position is within +5 or -5 degrees of the ISS position.
        return True


## -------------- checking time -------- ##


def dark_now_check():
    parameters = {"lat": HOME_TUPLE[0], "lng": HOME_TUPLE[1], "formatted": 0}

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data_json = response.json()

    sunset = data_json["results"]["sunset"]
    sunset_time = (sunset.split("T")[1]).split("+")[0]
    sunset_idt_hour = int(sunset_time.split(":")[0]) + 3
    # sunset_idt_time_hm = f"{sunset_idt_hour:02d}" + ":" + sunset_time.split(":")[1]

    now_full = datetime.datetime.now()
    now_hour = now_full.hour

    if now_hour > sunset_idt_hour:
        return True


## -------------- sending email -------- ##


def send_mail():
    my_email = os.getenv("my_email")
    my_password = os.getenv("my_password")

    with smtplib.SMTP("smtp.gmail.com") as my_connection:
        my_connection.starttls()
        my_connection.login(user=my_email, password=my_password)
        my_connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject: Look outside now\n\nISS should be flying above your city NOW! Look at the sky!!!",
        )


while True:
    time.sleep(60)  # my pc must remain on for it to work constantly
    if iss_overhead_check() and dark_now_check():  # if both are True
        send_mail()

# BONUS: run the code every 60 seconds.
