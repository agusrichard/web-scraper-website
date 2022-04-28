from apscheduler.schedulers.background import BackgroundScheduler

from .tasks import scrape_website


def scraping_scheduler():
    print("Scraping....")
    scrape_website.delay()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scraping_scheduler, "interval", days=1)
    scheduler.start()
