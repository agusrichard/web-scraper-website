from django.conf import settings

from scraper.scraper import make_scraper


def print_sekar():
    print("Sekardayu Hana Pradiani")
    print("I love you")
    print("Sekardayu Hana Pradiani")


def scrape_website():
    url = getattr(settings, "SCRAPE_URL", "https://medium.com/search?q=programming")
    with make_scraper(url) as scraper:
        scraper.go_to_first_page()
        scraper.scroll_down()
