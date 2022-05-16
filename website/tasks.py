from celery import shared_task
from django.conf import settings

from scraper.scraper import make_scraper
from website.models import ScrapingHistory


@shared_task
def scrape_website_background():
    sh = ScrapingHistory(status=1)
    sh.save()

    url = getattr(settings, "SCRAPE_URL", "https://medium.com/search?q=programming")
    num_of_scrolls = getattr(settings, "SCRAPE_NUM_OF_SCROLLS", 10)
    with make_scraper(url, sh.id) as scraper:
        scraper.go_to_first_page()
        scraper.scroll_down(num_scrolls=num_of_scrolls)


@shared_task
def scrape_website_manual(scraping_history_id: int):
    url = getattr(settings, "SCRAPE_URL", "https://medium.com/search?q=programming")
    num_of_scrolls = getattr(settings, "SCRAPE_NUM_OF_SCROLLS", 10)
    with make_scraper(url, scraping_history_id) as scraper:
        scraper.go_to_first_page()
        scraper.scroll_down(num_scrolls=num_of_scrolls)
