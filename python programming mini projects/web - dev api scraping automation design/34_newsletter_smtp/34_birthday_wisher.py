import smtplib, os, random
import datetime as dt
import pandas as pd
from dotenv import load_dotenv

## ------------ constants -------------- ##

load_dotenv()

my_email = os.getenv("my_email")
my_password = os.getenv("my_password")
current_file_dir = os.path.dirname(__file__)

## ------------ file paths ------------- ##

letter_path = os.path.join(
    current_file_dir, "letter_templates", f"letter_{random.randint(1,3)}.txt"
)
with open(letter_path, "r") as letter_file:
    letter_text = letter_file.read()

bd_csv_path = os.path.join(current_file_dir, "birthdays.csv")
with open(bd_csv_path, "r") as bd_file:
    bd_data = bd_file.read()

## ---------

today_date_tuple = (f"{dt.datetime.now().month:02d}", f"{dt.datetime.now().day:02d}")

bd_df = pd.read_csv(bd_csv_path)

bd_df["file_date_tuple"] = list(
    zip(
        bd_df["month"].astype(int).map("{:02d}".format),
        bd_df["day"].astype(int).map("{:02d}".format),
    )
)

selected_row = bd_df[
    bd_df["file_date_tuple"] == today_date_tuple
]  # is a series, may have 0, 1 or more rows

with smtplib.SMTP("smtp.gmail.com") as my_connection:
    my_connection.starttls()
    my_connection.login(user=my_email, password=my_password)
    if len(selected_row) > 0:  # if noone has bday today, do nothing
        for index, row in selected_row.iterrows():  # (index, row) is a tuple
            bd_person_mail = row["email"]
            bd_person_name = row["person_name"]
            named_letter = letter_text.replace(
                "[NAME]", bd_person_name
            )  # must save into variable
            my_connection.sendmail(
                from_addr=my_email,
                to_addrs=bd_person_mail,
                msg=f"Subject: Have you heard\n\n{named_letter}",
            )
