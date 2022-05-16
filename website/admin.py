from django.contrib import admin

from website.models import ScrapingHistory, Article

# Register your models here.
admin.site.register(ScrapingHistory)
admin.site.register(Article)
