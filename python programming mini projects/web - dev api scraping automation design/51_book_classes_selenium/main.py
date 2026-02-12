from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)
import os, time

## ----------------- CONFIG -------------------- ##
cur_dir = os.path.dirname(__file__)
ACCOUNT_EMAIL = "irenadav17@gmail.com"
ACCOUNT_PASSWORD = "Dre@mGym1990"
GYM_URL = "https://appbrewery.github.io/gym/"
target_time_slot = "7:00 pm"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
chrome_options.add_experimental_option("prefs", prefs)

user_data_dir = os.path.join(cur_dir, "chrome_profile_copy")
profile_dir_name = "Profile 5"
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument(f"--profile-directory={profile_dir_name}")

my_driver = webdriver.Chrome(options=chrome_options)
my_driver.get(GYM_URL)
my_driver.maximize_window()

wait = WebDriverWait(my_driver, 10)


def retry(func, retries=5, description=""):
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt}: {description}")
            result = func()
            print("✅ Success!")
            return result
        except Exception as e:
            print(f"❌ Failed on attempt {attempt}: {e}")
            time.sleep(2)
    raise Exception(f"All {retries} retries failed for {description}")


def login():
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_button.click()

    email_input = wait.until(EC.presence_of_element_located((By.ID, "email-input")))
    # email_input.send_keys(Keys.chord(Keys.CONTROL, "a"), Keys.DELETE)
    email_input.clear()  # alternative to above
    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = wait.until(
        EC.presence_of_element_located((By.ID, "password-input"))
    )
    # password_input.send_keys(Keys.chord(Keys.CONTROL, "a"), Keys.DELETE)
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)

    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-button")))
    submit_button.click()

    wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))


retry(login, description="Logging in to Gym")


def book_class():
    tuesday_section = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[id*='tue']"))
    )
    thursday_section = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[id*='thu']"))
    )

    tue_thu_section_list = []
    for day, section in (("tue", tuesday_section), ("thu", thursday_section)):
        class_cards = section.find_elements(By.CSS_SELECTOR, "div[id^='class-card']")
        class_date = section.find_element(By.TAG_NAME, "h2").text
        for card in class_cards:
            my_tuple = (card, class_date, day)
            tue_thu_section_list.append(my_tuple)

    classes_booked_count = 0
    classes_waitlist_joined_count = 0
    tue_thu_bookings_total_count = 0
    found_per_day = {"tue": False, "thu": False}
    for card, class_date, day in tue_thu_section_list:
        time_text = (
            card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']")
            .text.strip()
            .lower()
        )
        # print("Detected class time:", time_text)
        if target_time_slot in time_text:
            found_per_day[day] = True
            # print(f"Found 6pm class: {card.text} on {class_date} ({day})")
            print(f"Found class: [Info: '{card.text}' on {class_date} ({day})]")
            class_name = card.find_element(By.TAG_NAME, "h3").text
            time.sleep(0.8)
            try:

                book_button = card.find_element(
                    By.CSS_SELECTOR, "button[id^='book-button']"
                )
                # print("Button HTML:", book_button.get_attribute("outerHTML")) # for debugging
                button_text = book_button.text.strip().replace("\u00a0", " ").lower()
                # print(f"Button text detected: '{button_text}'")  # for debugging
                if "book class" in button_text:
                    time.sleep(0.5)
                    book_button.click()
                    print(f"✓ Booked: {class_name} on {class_date}")
                    classes_booked_count += 1
                elif "join waitlist" in button_text:
                    time.sleep(0.5)
                    book_button.click()
                    print(f"✓ Added to waitlist: {class_name} on {class_date}")
                    classes_waitlist_joined_count += 1
                elif "booked" in button_text:
                    print(
                        f"✓ Class: {class_name} on {class_date} has been previously booked"
                    )
                else:
                    print(
                        f"✓ Class: {class_name} on {class_date} has been previously added to waitlist"
                    )
            except ElementClickInterceptedException:
                print("⚠️ Button not clickable — intercepted by another element.")
            except Exception as e:
                print("No button found in this card:", e)
            # break

    for day in ("tue", "thu"):
        if not found_per_day[day]:
            print(f"No {target_time_slot} class found for {day.upper()}.")

    time.sleep(2)

    for card, class_date, day in tue_thu_section_list:
        try:
            status_button = card.find_element(
                By.CSS_SELECTOR, "button[id^='book-button']"
            )
            status_button_text = (
                status_button.text.strip().replace("\u00a0", " ").lower()
            )
            if "booked" in status_button_text or "waitlisted" in status_button_text:
                tue_thu_bookings_total_count += 1
        except Exception:
            pass

    print(
        f"--- BOOKING SUMMARY ---\nNew bookings: {classes_booked_count}\nNew waitlist entries: {classes_waitlist_joined_count}\nTotal Tue & Thu classes saved: {tue_thu_bookings_total_count}"
    )


retry(book_class, retries=5, description="Booking a class")


def check_tue_thu_booked():
    wanted_class_count = 0
    booked_class_count = 0
    tuesday_section = None
    thursday_section = None

    try:
        tuesday_section = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[id*='tue']"))
        )
    except TimeoutException:
        print("⚠️ Tuesday section not found.")

    try:
        thursday_section = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[id*='thu']"))
        )
    except TimeoutException:
        print("⚠️ Thursday section not found.")

    tue_thu_section_list = []
    for day, section in (("tue", tuesday_section), ("thu", thursday_section)):
        if section is None:
            print(f"⚠️ Skipping {day.upper()} — section not found.")
            continue
        try:
            class_cards = section.find_elements(
                By.CSS_SELECTOR, "div[id^='class-card']"
            )
            class_date = section.find_element(By.TAG_NAME, "h2").text
            for card in class_cards:
                my_tuple = (card, class_date, day)
                tue_thu_section_list.append(my_tuple)
                try:
                    time_text = (
                        card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']")
                        .text.strip()
                        .lower()
                    )
                except (
                    NoSuchElementException,
                    TimeoutException,
                    StaleElementReferenceException,
                ):
                    continue
                if target_time_slot in time_text:
                    wanted_class_count += 1
        except (
            NoSuchElementException,
            TimeoutException,
            StaleElementReferenceException,
        ):
            continue

    my_bookings_link = wait.until(
        EC.presence_of_element_located((By.ID, "my-bookings-link"))
    )
    my_bookings_link.click()
    my_bookings_container = wait.until(
        EC.presence_of_element_located((By.ID, "my-bookings-page"))
    )
    booked_class_cards = my_bookings_container.find_elements(
        By.CLASS_NAME, "MyBookings_bookingCard__VRdrR"
    )

    for i in booked_class_cards:
        if (
            "thu" in i.text.lower() or "tue" in i.text.lower()
        ) and target_time_slot in i.text.lower():
            booked_class_count += 1

    print(
        f"Tue & Thu {target_time_slot} classes: [available: {wanted_class_count}; booked: {booked_class_count}]"
    )
    diff = wanted_class_count - booked_class_count
    print(f"{diff} missing classes.")

    check_passed = wanted_class_count > 0 and wanted_class_count == booked_class_count

    return check_passed


def rebook_if_necessary():
    check_passed = check_tue_thu_booked()
    if check_passed:
        print("✅ All wanted classes are booked!")

        return

    print("Retrying to book missing classes")
    if "schedule" not in my_driver.current_url:
        my_driver.get(GYM_URL + "schedule/")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[id^='book-button']"))
    )
    retry(book_class, retries=5, description="Booking a class")

    raise Exception("Not all classes are booked!")


retry(
    rebook_if_necessary,
    retries=5,
    description="Checking that all properly booked.",
)
