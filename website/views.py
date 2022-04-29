from django.shortcuts import render, redirect

from .tasks import scrape_website
from .models import ScrapingHistory


def home(request):
    return render(request, "website/home.html", {"page_title": "Home"})


def scraping_history(request):
    histories = ScrapingHistory.objects.all()

    return render(
        request,
        "website/scraping_history.html",
        {"histories": histories, "page_title": "Scraping History"},
    )


def run_manual_scraping(request):
    if request.method == "POST":
        sh = ScrapingHistory(status=1)
        sh.save()
        scrape_website.delay(sh.id)

    return redirect("website:scraping_history")
