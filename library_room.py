from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import datetime, time, base64, json

with open("credentials_bb.json","r") as f:
    credentials = json.load(f)

USERNAME = credentials["username"]
PASSWORD = credentials["password"]

# DAY = input("Make reservation for [MTuWThFSaSu]: ")
days = {0:"Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4:"Fri", 5:"Sat", 6:"Sun"}
DAY = datetime.datetime.today().weekday() #days[DAY]
HOUR = datetime.datetime.today().hour #int(input("Which hour [10, 16]: "))
MINUTE = datetime.datetime.today().minute #int(input("Which hour [10, 16]: "))

weekday = datetime.datetime.today().weekday()
RESERVATION_DAY = datetime.datetime.today() + datetime.timedelta(days=((DAY - weekday) if weekday < DAY else (7 + DAY - weekday)))
RESERVATION_HOUR = str(HOUR%12) if HOUR != 12 else str(HOUR)
RESERVATION_HOUR = RESERVATION_HOUR + ':00' if MINUTE < 30 else RESERVATION_HOUR + ':30'
AMPM = 'am' if HOUR <= 12 else 'pm'
DURATION = '120'
print(f"\n Booking room for {days[DAY]} {RESERVATION_DAY.strftime('%b')} {RESERVATION_DAY.day}, {RESERVATION_DAY.year} at {RESERVATION_HOUR} {AMPM}")

profile = FirefoxProfile()
profile.set_preference('security.tls.version.min', 1)
driver = Firefox(firefox_profile=profile)
driver.minimize_window()
driver.get("https://libbook.unibocconi.it/openroom/")

elem = driver.find_element_by_id("usernamefield")
elem.clear()
elem.send_keys(str(USERNAME))
elem1 = driver.find_element_by_id("passwordfield")
elem1.clear()
elem1.send_keys(str(PASSWORD))
elem1.send_keys(Keys.RETURN)

switch = driver.find_element_by_id("themeswitch")
switch.click()

reservations = driver.find_elements_by_class_name("reservation_button")

with open("reservations.txt","w") as f:
    print("\n Your current reservations are:")
    f.write("Your current reservations are:\n")
    for i, res in enumerate(reservations):
        text = res.text.split("\n")
        day, year = text[1].split(",")
        year = year[:5]
        day = datetime.datetime.strptime(day+year, "%b %d %Y")
        wd = day.weekday()
        s = f"\t- {days[wd]} {text[1]} in room {text[0]} ({text[2]})\n"
        f.write(s)
        print(s[:-1])
    f.write(f"\t- {days[DAY]} {RESERVATION_DAY.strftime('%b')} {RESERVATION_DAY.day}, {RESERVATION_DAY.year} at {RESERVATION_HOUR} {AMPM}")

print("\n Looking for available rooms:")

reserve = driver.find_element_by_class_name("makereservation")
reserve.click()

select = Select(driver.find_element_by_name('month'))
select.select_by_value(str(RESERVATION_DAY.month))
select = Select(driver.find_element_by_name('day'))
select.select_by_value(str(RESERVATION_DAY.day))
select = Select(driver.find_element_by_name('year'))
select.select_by_value(str(RESERVATION_DAY.year))
select = Select(driver.find_element_by_name('time'))
select.select_by_value(str(RESERVATION_HOUR))
select = Select(driver.find_element_by_name('ampm'))
select.select_by_value(str(AMPM))
select = Select(driver.find_element_by_name('duration'))
select.select_by_value(str(DURATION))
select = Select(driver.find_element_by_name('size'))
select.select_by_value(str(4))

confirm = driver.find_element_by_id("find_room_button")
confirm.click()

for i in range(5):
    print("\n still looking...")
    time.sleep(10)
    results = driver.find_element_by_id("results")
    results = results.find_elements(By.CLASS_NAME, "room_button")
    driver.execute_script("window.scrollTo(0,470)")
    try:
        results[0].click()
        time.sleep(5)
        success = driver.find_element_by_id("success_msg")
        print(f"\n Evviva! {success.text}")
        break
    except:
        continue
    
try:
    failure = driver.find_element_by_id("error_msg")
    print(f"\n Oh rabbia... {failure.text}")
except:
    pass

driver.close()
input("\npress key to close ")