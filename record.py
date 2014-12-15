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

def getTimeRange():
  now = timezone.now()
  today = datetime(now.year, now.month, now.day)
  prevMid = int(time.mktime(today.timetuple()))
  tmrw_midnight = today + timedelta(days=1)
  tomorrowMid = int(time.mktime(tmrw_midnight.timetuple()))

  return 'since=%d&until=%d' % (prevMid, tomorrowMid)

def getEventsURL():
  data = open('keys.json')
  keys = json.load(data)
  data.close()

  timeRange = getTimeRange()
  access_token = '%s|%s' % (keys["app_id"], keys["app_secret"])
  url = 'https://graph.facebook.com/OffTheGridSF/events?%s&access_token=%s' % (timeRange, access_token)
  return url

def getEventURL(eventId):
  data = open('keys.json')
  keys = json.load(data)
  data.close()

  access_token = '%s|%s' % (keys["app_id"], keys["app_secret"])
  url = 'https://graph.facebook.com/%s?access_token=%s' % (eventId, access_token)
  return url


# Reset all vendor attended counts to 0, and for
# each event in the last 30 days, increment their attended count.
# I could just keep a running total for each vendor
# and subtract their events from 31 days ago, but thats
# dependent on consistently scraping events without fail.
# Also, I think this method is more explicit and straightforward.
def updateVendors():
  VendorsModule.resetVendors()

  now = timezone.now()
  today = datetime(now.year, now.month, now.day)
  thirtyDaysAgo = today - timedelta(days=30)

  # get all events from past 30 days
  events = Event.objects.filter(date__gte=thirtyDaysAgo)

  for event in events:
    try:
      v = Vendor.objects.get(name__iexact=event.name)
    except Vendor.MultipleObjectsReturned:
      # do something
      continue

    v.attended += 1
    v.save()

  return

  

def scrapeEvents(test):
  eventsUrl = getEventsURL()
  r = requests.get(eventsUrl)

  vendors = Vendor.objects.all()

  # check if wednesday or friday, and fill up list of vendors if so
  WFvendors = []
  WF = (datetime.today().weekday() == 2) or (datetime.today().weekday() == 4)

  # to be used when saving each event to db
  now = timezone.now()
  today = datetime(now.year, now.month, now.day)

  for event in r.json()["data"]:
    eventId = event["id"]
    print "getting %s's desc" % eventId
    eventUrl = getEventURL(eventId)
    r2 = requests.get(eventUrl)
    desc = r2.json()["description"]


    # unfortunately, the facebook description page is not consistent with
    # how they list the vendors appearing. just run through the list of
    # vendors and check if they're mentioned at all
    for vendor in vendors:
      if re.search(vendor.name, desc, re.IGNORECASE):
        print "vendor %s in desc" % vendor.name

        # add vendor if they're at 5th & Minna and its wednesday or friday
        if WF and re.search('5th and Minna', r2.json()["name"], re.IGNORECASE):
          WFvendors.append(vendor.name)

        '''
        vendor.attended += 1
        vendor.save()
        '''

        e = Event(name=vendor.name, date=today)
        e.save()


  if WF or test:
    HipChatModule.sendUpdate(WFvendors, test)

  updateVendors()

  return

if __name__ == '__main__':
  scrapeEvents(True)
