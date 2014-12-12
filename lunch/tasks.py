from __future__ import absolute_import

from proj.celery import app


@app.task
def add(x, y):
  return x + y


@app.task
def mul(x, y):
  return x * y


@app.task
def xsum(numbers):
  return sum(numbers)

'''
from __future__ import absolute_import

from celery import shared_task

@shared_task
def add(x, y):
  return x + y


@shared_task
def mul(x, y):
  return x * y


@shared_task
def xsum(numbers):
  return sum(numbers)
'''
