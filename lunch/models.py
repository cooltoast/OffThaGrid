from datetime import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Vendor(models.Model):
  name = models.CharField(max_length=50)
  attended = models.PositiveIntegerField(default=0)
  date = models.DateTimeField(default=datetime(timezone.now().year, timezone.now().month, timezone.now().day), blank=True)

class Event(models.Model):
  name = models.CharField(max_length=50)
  date = models.DateTimeField(default=datetime(timezone.now().year, timezone.now().month, timezone.now().day), blank=True)

