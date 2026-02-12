from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

my_driver = webdriver.Chrome(options=chrome_options)
my_driver.get("https://ozh.github.io/cookieclicker/")
my_driver.maximize_window()

english_button = WebDriverWait(my_driver, 20).until(
    EC.element_to_be_clickable((By.ID, "langSelect-EN"))
)
english_button.click()

big_cookie = my_driver.find_element(By.ID, "bigCookie")


def check_upgrades():
    upgrades_unlocked = my_driver.find_elements(
        By.CSS_SELECTOR, ".product.unlocked.enabled"
    )

    upgrade_prices = {}

    for upgrade in upgrades_unlocked:
        price_el = upgrade.find_element(By.CLASS_NAME, "price")
        price = int(price_el.text.replace(",", ""))
        upgrade_prices[upgrade] = price

    if upgrade_prices:
        top_price = max(upgrade_prices, key=upgrade_prices.get)
        top_price.click()


def check_upgrades():
    upgrades = my_driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
    upgrade_prices = {}

    for upgrade in upgrades:
        try:
            price_el = upgrade.find_element(By.CLASS_NAME, "price")
            price = int(price_el.text.replace(",", ""))
            upgrade_prices[upgrade] = price
        except (StaleElementReferenceException, NoSuchElementException, ValueError):
            continue

    if upgrade_prices:
        top = max(upgrade_prices, key=upgrade_prices.get)
        try:
            top.click()
            time.sleep(0.05)  # tiny pause after click
        except (StaleElementReferenceException, NoSuchElementException):
            pass


try:
    consent_button = WebDriverWait(my_driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "cc_btn_accept_all"))
    )
    consent_button.click()
    print("Cookie consent dismissed.")
except:
    print("No cookie consent banner found.")

start_time = time.time()
end_time = start_time + 3 * 60
next_check = time.time() + 30
upgrade_interval = 15

while time.time() < end_time:
    try:
        # always find the big cookie fresh to avoid stale element
        big_cookie = my_driver.find_element(By.ID, "bigCookie")
        big_cookie.click()
    except (StaleElementReferenceException, NoSuchElementException):
        continue

    if time.time() >= next_check:
        check_upgrades()
        next_check = time.time() + upgrade_interval

    time.sleep(0.01)  # to prevent CPU overuse

max_retries = 5
for attempt in range(max_retries):
    try:
        cps_counter = my_driver.find_element(By.ID, "cookiesPerSecond")
        print(f"Cookies per second: {cps_counter.text}")
        break  # success, exit loop
    except StaleElementReferenceException:
        print("CPS element went stale, retrying...")
        time.sleep(0.1)  # small delay before retry
else:
    print("Couldn't read CPS after several attempts.")
