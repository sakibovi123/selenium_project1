from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import constant as const
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec


class CageMatch(webdriver.Chrome):
    def __init__(self, path=r"/usr/local/bin/SeleniumDriver/", teardown=False):
        self.path = path
        self.teardown = teardown
        os.environ["PATH"] += self.path
        super(CageMatch, self).__init__()
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def find_web_page(self):
        self.get(const.EVENTS_URL)

    @staticmethod
    def extract_urls_from_td_get_result(self):
        url = const.EVENTS_URL
        wait = WebDriverWait(self.path, 10)
        wait.until(ec.element_to_be_clickable((
            By.XPATH, "//tr[contains(@class, 'TRowCard')]//a[2]"
        )))
        links = self.find_elements(
            By.XPATH, "//tr[contains(@class, 'TRowCard')]//a[2]"
        )
        for idx, link in enumerate(links):
            wait.until(ec.element_to_be_clickable(link)).click()
            try:
                titles = wait.until(ec.visibility_of_all_elements_located((
                    By.CSS_SELECTOR, "div.MatchType"
                )))

                for title in titles:
                    print(title.text)
            except:
                print("No Matches Found")






