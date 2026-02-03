from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import os, time
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

## --------------CONSTANTS ------------##
load_dotenv()

cur_dir = os.path.dirname(__file__)
URL = "https://www.vacationstogo.com/"
user = os.getenv("mail")

## ------------- DRIVER ----------------- ##

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
chrome_options.add_experimental_option("prefs", prefs)

user_data_dir = os.path.join(cur_dir, "chrome_profile_copy")
profile_dir_name = "Profile 5"
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument(f"--profile-directory={profile_dir_name}")

my_driver = webdriver.Chrome(options=chrome_options)
my_driver.get(URL)

actions = ActionChains(my_driver)

my_driver.maximize_window()

## --------- ACTION ------------- ##

wait = WebDriverWait(my_driver, 15)

deals_btn = wait.until(EC.element_to_be_clickable((By.ID, "fabShowMeTheDeals")))
deals_btn.click()

try:
    login_input = wait.until(EC.element_to_be_clickable((By.NAME, "LogEmail")))
    login_input.click()
    time.sleep(1)

    login_input.send_keys(user)
    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="alreadyMemberForm"]/table/tbody/tr[2]/td[2]/button')
        )
    )
    login_btn.click()
except TimeoutException:
    pass

lines_select = wait.until(EC.element_to_be_clickable((By.NAME, "l")))
lines_select.click()

time.sleep(1)

ncl_select = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="LineID"]/option[20]'))
)
ncl_select.click()

actions.move_by_offset(100, 100).click().perform()

time.sleep(1)

nights_select = wait.until(EC.element_to_be_clickable((By.NAME, "n")))
nights_select.click()

time.sleep(1)

select_8_13_n = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="Length"]/option[4]'))
)
select_8_13_n.click()

actions.move_by_offset(100, 100).click().perform()

time.sleep(1)
deals_btn = wait.until(EC.element_to_be_clickable((By.ID, "fabShowMeTheDeals")))
deals_btn.click()

sort_btn = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="bodyContainer"]/div[3]/table[1]/thead/tr/td[9]/a')
    )
)
sort_btn.click()

## ----------------- BUILDING DF to CSV -------------- ##

mediter_deals_logo = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="bodyContainer"]/div[3]/table[28]/tbody/tr/td/a')
    )
)

mediter_deals_logo.click()

time.sleep(1)

mediter_deals = my_driver.find_element(
    By.XPATH,
    "//a[@name='MediterraneanAll']/ancestor::table[@class='ticker region']/following-sibling::table[@class='ticker deals']",
)

mediter_table = mediter_deals.find_elements(By.TAG_NAME, "tr")

medit_cruises_list = []

for row in mediter_table[:10]:
    columns = row.find_elements(By.TAG_NAME, "td")
    if columns:
        rows_data = []
        for column in columns[:-1]:
            cell_text = column.text.replace("\n", " ").strip()
            rows_data.append(cell_text)
        medit_cruises_list.append(rows_data)


header = mediter_deals.find_elements(By.TAG_NAME, "tr")
header_row = header[0]  # first row is <tr> which includes the 'td' elements

column_titles = []
for td in header_row.find_elements(By.TAG_NAME, "td")[:-1]:
    column_class = td.get_attribute("class").split()[0]
    column_titles.append(column_class)

column_titles[0] = "deal_#"
column_titles[1] = "nights"
column_titles[2] = "sailing_date"
column_titles[3] = "embark_in"
column_titles[4] = "disembark_in"
column_titles[5] = "cruise_line_ship"
column_titles[6] = "ship_rating"
column_titles[7] = "brochure"
column_titles[8] = "agent_price"
column_titles[9] = "saving"
print(column_titles)

df = pd.DataFrame(medit_cruises_list, columns=column_titles)
top = df.head()

## -------------- MAIL --------------- ##


test_mail = os.environ.get("test_mail")
test_password = os.environ.get("test_password")
print(test_mail, test_password)


def send_mail(top):
    subject = "Top cruise deals for you"
    body = f"Find below top-5 deals for you:\n{top.to_string(index=False)}"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = test_mail
    msg["To"] = test_mail

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(test_mail, test_password)
            connection.send_message(msg)
    except Exception as e:
        print(f"Email error: {e}")


## ---- ACTION ------ #

df.to_csv("mediterranean_deals.csv", index=False)
print("✅ Mediterranean deals saved to mediterranean_deals.csv")
send_mail(top)

## ----------- CHECKING -------------- ##
data = pd.read_csv("mediterranean_deals.csv")
print(data.head())
