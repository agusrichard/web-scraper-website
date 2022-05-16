from apscheduler.schedulers.background import BackgroundScheduler

from .tasks import scrape_website_background
from .models import ScrapingHistory


def scraping_scheduler():
    print("Scraping....")

    sh = ScrapingHistory(status=1)
    sh.save()
    scrape_website_background.delay(sh.id)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scraping_scheduler, "interval", days=1)
    scheduler.start()
