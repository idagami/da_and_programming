import os, requests, smtplib, re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
cur_file = os.path.dirname(__file__)
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "i18n-prefs=USD; lc-main=en_US",
}

URL = "https://www.amazon.com/gp/product/B0DQCN69HG/ref=ox_sc_saved_title_1?smid=ANFP7QDS8HVJL&th=1"
desired_price = 100

response = requests.get(URL, headers=header)
print(response.status_code)
page = response.text
my_soup = BeautifulSoup(page, "html.parser")

price_text = my_soup.select_one("span.a-offscreen").getText()
current_price = float(re.sub(r"[^\d.]", "", price_text))
# print(current_price)
item_name_span = my_soup.select("h1")
item_name = item_name_span[0].select_one("#productTitle").getText().strip()[:30]
# print(item_name)

my_email = os.getenv("GMAIL_APP_MAIL")
my_password = os.getenv("GMAIL_APP_PASSWORD")
smtp_address = os.getenv("GMAIL_SMTP_ADDRESS")


if current_price < desired_price:
    with smtplib.SMTP(smtp_address) as my_connection:
        my_connection.starttls()
        my_connection.login(user=my_email, password=my_password)
        my_connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject: Price drop for {item_name}!\n\nGo and check out the {item_name} that you wanted. It's now ${current_price}!!!\n{URL}",
        )
        print("email sent")
