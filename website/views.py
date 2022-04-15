from django.shortcuts import render

from .tasks import add

# Create your views here.
def home(request):
    add.delay(1, 2)
    return render(request, "website/home.html", {"page_title": "Home"})
