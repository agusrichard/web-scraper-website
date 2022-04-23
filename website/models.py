from django.db import models

SCRAPPING_STATUSES = (
    (0, "Pending"),
    (1, "In Progress"),
    (2, "Completed"),
    (3, "Failed"),
)


class ScrappingHistory(models.Model):
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=SCRAPPING_STATUSES, default=0)

    def __str__(self):
        return str(self.status)


class Article(models.Model):
    title = models.CharField(max_length=500, unique=True)
    subtitle = models.TextField()
    author = models.CharField(max_length=100)
    image_src = models.TextField()
    url = models.TextField()
    published_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    scrapping_history = models.ForeignKey(ScrappingHistory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)
