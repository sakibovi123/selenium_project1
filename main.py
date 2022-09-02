from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
import sys
import time

app_path = os.path.dirname(sys.executable)

now = datetime.now()
month_day_year = now.strftime("%m%d%y")

options = Options()
options.add_argument("--start-maximized")

os.environ["PATH"] += r"usr/local/bin/SeleniumDriver"
driver = webdriver.Chrome()

url = 'https://www.cagematch.net/?id=1&view=cards&year=2022&Day=&Month=&Year=2022&name=&promotion=1&showtype=Pay+Per+View'

wait = WebDriverWait(driver, 10)
driver.get(url)

wait.until(EC.element_to_be_clickable((By.ID, "cookiedingsbumsCloser"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//tr[contains(@class,'TRowCard')]//a[2]")))
time.sleep(0.5)
links = driver.find_elements(By.XPATH, "//tr[contains(@class,'TRowCard')]//a[2]")

event = []
title = []
match = []
for idx, link in enumerate(links):
    wait.until(EC.element_to_be_clickable(link)).click()
    print("link " + str(idx+1) + " matches:")
    try:
        events = wait.until(EC.visibility_of_all_elements_located((
            By.CLASS_NAME, "TextHeader"
        )))
        titles = wait.until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "div.MatchType")
        ))
        matches = wait.until(EC.visibility_of_all_elements_located(
            (
                By.CSS_SELECTOR, "div.MatchResults"
            )
        ))
        for e in events:
            for t in titles:
                for m in matches:
                    event.append(e.text)
                    title.append(t.text)
                    match.append(m.text)


    except:
        print(" ")
    print(" ")
    driver.back()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//tr[contains(@class,'TRowCard')]//a[2]")))
    time.sleep(0.5)
    links = driver.find_elements(By.XPATH, "//tr[contains(@class,'TRowCard')]//a[2]")

my_dict = {"Event": event, "match_title": title, "matches": match}
print(my_dict)
df = pd.DataFrame(my_dict)
df.to_json(f"{month_day_year}.json", orient='records', lines=True)