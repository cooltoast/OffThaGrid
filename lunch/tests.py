from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from lunch.models import Event,Vendor
from datetime import datetime

# Create your tests here.
class EventTestCase(TestCase):
  def setUp(self):
    now = timezone.now()
    today = datetime(now.year, now.month, now.day)
    Event.objects.create(name="todayEvent", date=today)
    Event.objects.create(name="thirtydaysago", date=today-timedelta(days=30))
    Event.objects.create(name="thirtyonedaysago", date=today-timedelta(days=31))

  def test30dayFilter(self):
    todayEvent = Event.objects.get(name="todayEvent")
    thirtydaysago = Event.objects.get(name="thirtydaysago")
    thirtyonedaysago = Event.objects.get(name="thirtyonedaysago")

    now = timezone.now()
    today = datetime(now.year, now.month, now.day)
    thirtyDaysAgo = today - timedelta(days=30)
    events = Event.objects.filter(date__gte=thirtyDaysAgo)
    self.assertTrue(todayEvent in events)
    self.assertTrue(thirtydaysago in events)
    self.assertFalse(thirtyonedaysago in events)
