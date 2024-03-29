from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .tasks import scrape_website_manual
from .models import ScrapingHistory, Article


def home(request):
    data = Article.objects.all().order_by("-created_date")
    page = request.GET.get("page", 1)

    page_range = None
    paginator = Paginator(data, 20)
    try:
        page_list = paginator.page(page)
        page_range = paginator.get_elided_page_range(number=page)
    except PageNotAnInteger:
        page_list = paginator.page(1)
        page_range = paginator.get_elided_page_range(number=1)
    except EmptyPage:
        page_list = paginator.page(paginator.num_pages)
    return render(
        request,
        "website/home.html",
        {"page_title": "Home", "articles": page_list, "page_range": page_range},
    )


def scraping_history(request):
    histories = ScrapingHistory.objects.all().order_by("-start_datetime")
    page = request.GET.get("page", 1)

    paginator = Paginator(histories, 10)
    page_range = paginator.get_elided_page_range(number=page)
    try:
        page_list = paginator.page(page)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator.page(paginator.num_pages)
    return render(
        request,
        "website/scraping_history.html",
        {
            "histories": page_list,
            "page_range": page_range,
            "page_title": "Scraping History",
        },
    )


def run_manual_scraping(request):
    if request.method == "POST":
        sh = ScrapingHistory(status=1)
        sh.save()
        scrape_website_manual.delay(sh.id)

    return redirect("website:scraping_history")
