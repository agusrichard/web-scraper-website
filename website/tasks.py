from celery import shared_task
from django.conf import settings

from scraper.scraper import make_scraper


@shared_task
def scrape_website():
    url = getattr(settings, "SCRAPE_URL", "https://medium.com/search?q=programming")
    with make_scraper(url) as scraper:
        scraper.go_to_first_page()
        scraper.scroll_down()
