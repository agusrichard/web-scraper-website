from django.urls import path

from .views import home, scraping_history, run_manual_scraping

app_name = "website"
urlpatterns = [
    path("", home, name="home"),
    path("scraping-history/", scraping_history, name="scraping_history"),
    path("run-manual-scraping/", run_manual_scraping, name="run_manual_scraping"),
]
