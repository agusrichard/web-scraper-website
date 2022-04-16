import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://medium.com/search?q=programming"


class Scraper(webdriver.Chrome):
    def __init__(self, driver_path=None, teardown=False, implicitly_time_to_wait=10):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        driver_dir = os.path.join(base_path, "driver")

        self.driver_path = (
            driver_path
            if driver_path is not None
            else os.path.join(driver_dir, "chromedriver.exe")
        )
        self.teardown = teardown
        self.implicitly_time_to_wait = implicitly_time_to_wait

        super().__init__(executable_path=self.driver_path)

        self.implicitly_wait(self.implicitly_time_to_wait)
        self.maximize_window()
        self.result = []

    def __exit__(self, *args):
        if self.teardown:
            self.quit()

    def go_to_first_page(self):
        self.get(BASE_URL)

    def get_article_section(self):
        css_selector = "article"
        sections = self.find_elements(by=By.CSS_SELECTOR, value=css_selector)
        for section in sections:
            print(str(section))

    def scroll_down(self, sleep_time=3, num_scrolls=10):
        # Get scroll height.
        last_height = self.execute_script("return document.body.scrollHeight")

        for _ in range(num_scrolls):
            self.get_article_section()

            # Scroll down to the bottom.
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(sleep_time)
            self.find_element(
                by=By.XPATH, value="//*[contains(text(), 'Show more')]"
            ).click()

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height


if __name__ == "__main__":
    with Scraper() as scraper:
        scraper.go_to_first_page()
        scraper.scroll_down()
