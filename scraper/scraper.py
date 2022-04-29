import time
from datetime import datetime
from django.utils import timezone as tz
from django.db.utils import IntegrityError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from website.models import Article, ScrapingHistory

BASE_URL = "https://medium.com/search?q=programming"


class Scraper(webdriver.Chrome):
    def __init__(self, url: str):
        super().__init__(chrome_options=self.set_chrome_options())

        self.result = dict()
        self.url = url

        scraping_history = ScrapingHistory(status=1)
        scraping_history.save()
        self.scraping_history = scraping_history

    def __exit__(self, *args):
        print("self.result", self.result)
        self.scraping_history.end_datetime = tz.now()
        self.scraping_history.status = 2
        self.scraping_history.save()
        self.quit()

    def set_chrome_options(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}

        return chrome_options

    def go_to_first_page(self):
        self.get(self.url)

    def get_elements(self, section):
        date = ""
        img = ""

        title = section.find_element(by=By.CSS_SELECTOR, value="h2").text.strip()
        author = section.find_element(
            by=By.CSS_SELECTOR, value="div.ao.o p"
        ).text.strip()
        url = section.find_element(
            by=By.CSS_SELECTOR, value='a[aria-label="Post Preview Title"]'
        ).get_attribute("href")
        spans = section.find_elements(by=By.CSS_SELECTOR, value="p.bn.bo.bp.co span")
        if len(spans) > 1:
            date = spans[1].text.strip()
        imgs = section.find_elements(by=By.CSS_SELECTOR, value="img")
        if len(imgs) > 1:
            img = imgs[1].get_attribute("src")

        print("date", date)

        data = {
            "title": title,
            "author": author,
            "published_date": datetime.strptime(date, "%b %d, %Y"),
            "url": url,
            "image_src": img,
            "scrapping_history": self.scraping_history,
        }

        return data

    def get_article_section(self):
        sections = self.find_elements(by=By.CSS_SELECTOR, value="article")
        for section in sections:
            data = self.get_elements(section)

            try:
                article = Article(**data)
                article.save()
            except IntegrityError:
                continue

    def scroll_down(self, sleep_time=3, num_scrolls=10):
        last_height = self.execute_script("return document.body.scrollHeight")

        for _ in range(num_scrolls):
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(sleep_time)
            self.get_article_section()
            self.find_element(
                by=By.XPATH, value="//*[contains(text(), 'Show more')]"
            ).click()

            new_height = self.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height


def make_scraper(url: str):
    return Scraper(url)


if __name__ == "__main__":
    with Scraper(BASE_URL) as scraper:
        scraper.go_to_first_page()
        scraper.scroll_down()
