from time import sleep
from celery import shared_task


@shared_task
def add(x, y):
    sleep(1)
    return x + y
