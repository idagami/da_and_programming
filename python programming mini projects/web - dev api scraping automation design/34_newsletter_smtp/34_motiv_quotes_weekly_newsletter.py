import smtplib, os, random
import datetime as dt
from dotenv import load_dotenv

load_dotenv()

current_file_dir = os.path.dirname(__file__)
quotes_path = os.path.join(current_file_dir, "quotes.txt")
with open(quotes_path, "r") as quotes_file:
    quotes_data = quotes_file.read().splitlines()

quote = random.choice(quotes_data)
pieces = quote.split(sep=" - ")
author = pieces[1]
quote_text = pieces[0].strip('"')

curr_dof = dt.datetime.now().weekday()

my_email = os.getenv("my_email")
my_password = os.getenv("my_password")

with smtplib.SMTP("smtp.gmail.com") as my_connection:
    my_connection.starttls()
    my_connection.login(user=my_email, password=my_password)
    if curr_dof == 3:
        my_connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,  # "irenadavt@yahoo.com" as test can even send to my_email
            msg=f"Subject: Tuesday motivational newsletter\n\nDear friend,\n{quote_text}\n{author}.",
        )
# my_connection.close() # to avoid writing this like, use 'with' in line 8
