import datetime
from django.db import models

# Create your models here.
class Vendor(models.Model):
  name = models.CharField(max_length=200)
  attended = models.PositiveIntegerField(default=0)

class Event(models.Model):
  vendor = models.ForeignKey(Vendor, default=0)
  date = models.DateField(("Date"), default=datetime.date.today)
  location = models.CharField(max_length=200)
