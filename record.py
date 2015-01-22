import sys, os
sys.path.append('/opt/myenv/gingerio/lunch')
os.environ['DJANGO_SETTINGS_MODULE'] = 'gingerio.settings'
from django.conf import settings
from django.utils import timezone

import django
django.setup()

from lunch.models import Vendor, Event
import json
import re
import requests
import time
from datetime import datetime, timedelta

import hipChat as HipChatModule
import vendors as VendorsModule

class Keys():
  def __init__(self):
    data = open('/var/www/gingerio/keys.json')
    self.keys = json.load(data)
    self.access_token = '%s|%s' % (self.keys["app_id"], self.keys["app_secret"])
    data.close()

  pass

def getTimeRange():
  """Return last midnight and next midnight"""
  now = timezone.now()
  today = datetime(now.year, now.month, now.day)
  prevMid = int(time.mktime(today.timetuple()))
  tmrw_midnight = today + timedelta(days=1)
  tomorrowMid = int(time.mktime(tmrw_midnight.timetuple()))

  return prevMid, tomorrowMid

def getEventsURL(keys):
  """Return url and options for request"""
  since, until = getTimeRange()
  url = 'https://graph.facebook.com/OffTheGridSF/events'

  # filter events only for today using since and until timestamps
  options = {
    "since": since,
    "until": until,
    "access_token": keys.access_token,
  }

  return url, options

# Reset all vendor attended counts to 0, and for
# each event in the last 30 days, increment their attended count.
# I could just keep a running total for each vendor
# and subtract their events from 31 days ago, but thats
# dependent on consistently scraping events without fail.
# Also, I think this method is more explicit and straightforward.

# 2014.12.21
# don't need to reset vendor attended integer attribute
# we'll just overwrite it with the correct amount once per day.
# VendorsModule.resetVendors()
def updateVendors():
  """Update vendor attended count from Event db"""

  now = timezone.now()
  today = datetime(now.year, now.month, now.day)
  thirtyDaysAgo = today - timedelta(days=30)

  # get all events within past 30 days
  events = Event.objects.filter(date__gte=thirtyDaysAgo)

  vendorCount = {}

  # first, count up all the vendor appearances over last 30 days
  for event in events:
    if event.name in vendorCount:
      vendorCount[event.name] += 1
    else:
      vendorCount[event.name] = 1

  # overwrite each vendor appearance count
  for vendorName in vendorCount:
    try:
      v = Vendor.objects.get(name__iexact=vendorName)
    except Vendor.MultipleObjectsReturned:
      # do something
      continue

    v.attended = vendorCount[vendorName]
    v.save()

  return

  

def scrapeEvents():
  """Gets facebook events for the day and stores in db"""
  keys = Keys()
  eventsUrl, eventsOptions = getEventsURL(keys)
  r = requests.get(eventsUrl, params=eventsOptions)
  events = r.json()["data"]

  vendors = Vendor.objects.all()

  # check if wednesday or friday, and fill up list of vendors if so
  WFvendors = []
  WF = (datetime.today().weekday() == 2) or (datetime.today().weekday() == 4)

  # to be used when saving each event to db
  now = timezone.now()
  today = datetime(now.year, now.month, now.day)

  for event in events:
    eventId = event["id"]

    eventUrl = 'https://graph.facebook.com/%s' % eventId
    r2 = requests.get(eventUrl, params={'access_token':keys.access_token})

    desc = r2.json()["description"]
    eventName = r2.json()["name"]

    # unfortunately, the facebook description page is not consistent with
    # how they list the vendors appearing. just run through the list of
    # vendors and check if they're mentioned at all
    for vendor in vendors:
      if re.search(vendor.name, desc, re.IGNORECASE):
        print "vendor %s in desc" % vendor.name

        # add vendor if they're at 5th & Minna and its wednesday or friday
        if WF and re.search('5th and Minna', eventName, re.IGNORECASE):
          WFvendors.append(vendor.name)

        e = Event(name=vendor.name, date=today)
        e.save()


  if WF:
    HipChatModule.sendUpdate(WFvendors)

  updateVendors()

  return

if __name__ == '__main__':

  # if there are events in table, find the latest one's date
  # and scrape events if latest event is before today.
  # else if there are no events in table, scrape events anyway.
  try:
    latestEventDate = Event.objects.order_by('-date')[0].date
  except IndexError: # scrape events if no events in table
    scrapeEvents()
  else: # inspect the latest event's date in the table, compare to today
    now = timezone.now()
    today = datetime(now.year, now.month, now.day)

    # I haven't already scraped today, scrape events.
    # I'll know that if the date of the latest event in the table isn't today.
    if (today != latestEventDate):
      scrapeEvents()
    else:
      print "already scraped events today, %s" % now
