from datetime import datetime
from django.db import models

# Create your models here.
class Vendor(models.Model):
  name = models.CharField(max_length=200)
  attended = models.PositiveIntegerField(default=0)
  date = models.DateTimeField(default=datetime(datetime.now().year, datetime.now().month, datetime.now().day), blank=True)

