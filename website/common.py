from django.db import models


class ScrapingStatuses(models.IntegerChoices):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3
