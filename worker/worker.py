from time import time
from celery import Celery

worker = Celery(__name__, broker='redis://redis:6379/0')

@worker.task(name='create_task')
def create_task(task_name):
    time.sleep(1)
    return 'Hello World'