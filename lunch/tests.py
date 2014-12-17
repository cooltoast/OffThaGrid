from django.test import TestCase
from lunch.models import Event,Vendor
from datetime import datetime

# Create your tests here.
class EventTestCase(TestCase):
  def setUp(self):
    now = timezone.now()
    today = datetime(now.year, now.month, now.day)
    Event.objects.create(name="todayEvent", date=today
    Event.objects.create(name="30daysagoEvent", date=today-timedelta(days=30))
    Event.objects.create(name="31daysagoEvent", date=today-timedelta(days=31))

  def test30dayFilter(self):
    todayEvent = Event.objects.get(name="todayEvent")
    30daysagoEvent = Event.objects.get(name="30daysagoEvent")
    31daysagoEvent = Event.objects.get(name="31daysagoEvent")

    thirtyDaysAgo = today - timedelta(days=30)
    events = Event.objects.filter(date__gte=thirtyDaysAgo)
    self.assertTrue(todayEvent in events)
    self.assertTrue(30daysagoEvent in events)
    self.assertFalse(31daysagoEvent in events)
