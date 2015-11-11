from __future__ import absolute_import
from celery import Celery
from celery import shared_task
from celery import app

app = Celery('tasks')

@app.task
def alex_test_string(msg):
    print(msg)
    