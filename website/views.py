from django.shortcuts import render

from .tasks import scrape_website


def home(request):
    scrape_website.delay()
    return render(request, "website/home.html", {"page_title": "Home"})
