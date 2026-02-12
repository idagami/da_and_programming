from bs4 import BeautifulSoup
import os
import requests

## -------- selenium imports --------- ##
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)
import os, time
from dotenv import load_dotenv

## ------------- CONSTANTS --------------- ##
gs_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfmUGLseDM4ktdDIFVMZV3REwCL4lGWVJk_2ccHJ78H81D1qw/viewform?usp=header"
zillow_fake_url = "https://appbrewery.github.io/Zillow-Clone/"

cur_dir = os.path.dirname(__file__)
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "i18n-prefs=USD; lc-main=en_US",
}

## ------------- SELENIUM CONSTANTS --------------- ##
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option(
    "excludeSwitches",
    ["enable-automation"],
)

prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
}
chrome_options.add_experimental_option("prefs", prefs)

user_data_dir = os.path.join(cur_dir, "chrome_profile_copy")
profile_dir_name = "Profile 5"
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument(f"--profile-directory={profile_dir_name}")

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en,q=0.9",
}

my_driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(my_driver, 5)

## ------------- BS4 --------------- ##
response = requests.get(zillow_fake_url, headers=header)
print(response.status_code)
page = response.text
my_soup = BeautifulSoup(page, "html.parser")
# print(my_soup.title) # testing purpose

address_list = my_soup.select(selector="address")
price_dirty_list = my_soup.select(selector=".PropertyCardWrapper__StyledPriceLine")
links_list = my_soup.select(selector="div.StyledPropertyCardDataWrapper > a")

## ------------- SELENIUM SCRAPING --------------- ##
my_driver.get(url=gs_form_url)
my_driver.maximize_window()

## ----------- ONE BIG LOOP --------------- ##
for a, b, c in zip(address_list, price_dirty_list, links_list):
    input_address = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
        )
    )
    input_price = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
        )
    )
    input_link = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
        )
    )

    address = a.text.strip()
    if "|" in a:
        address = address.split("| ")[1]
    input_address.send_keys(address)
    print(address)

    price_text = b.getText().replace(",", "").replace(".", "")
    price = price_text[:5]
    input_price.send_keys(price)
    print(price)

    link = c["href"]
    input_link.send_keys(link)
    print(link)

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Submit']"))
    )
    # alternative for submit_btn: //*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span
    submit_btn.click()

    next_form_link = wait.until(
        EC.presence_of_element_located((By.LINK_TEXT, "שליחת תגובה נוספת"))
    )
    next_form_link.click()
