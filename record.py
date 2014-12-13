import sys, os
sys.path.append('/opt/myenv/gingerio/lunch')
os.environ['DJANGO_SETTINGS_MODULE'] = 'gingerio.settings'
from django.conf import settings

import django
django.setup()

from lunch.models import Vendor
import json
import re
import requests
import time
from datetime import datetime, timedelta

import hipChat as HipChatModule

def getTimeRange():
  now = datetime.now()
  previous_midnight = datetime(now.year, now.month, now.day)
  prevMid = int(time.mktime(previous_midnight.timetuple()))
  tmrw_midnight = previous_midnight + timedelta(days=1)
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
  

def scrape():
  eventsUrl = getEventsURL()
  r = requests.get(eventsUrl)
  vendors = Vendor.objects.all()
  WFvendors = []
  WF = (datetime.today().weekday() == 2) or (datetime.today().weekday() == 4)
  for event in r.json()["data"]:
    eventId = event["id"]
    print "getting %s's desc" % eventId
    eventUrl = getEventURL(eventId)
    r2 = requests.get(eventUrl)
    desc = r2.json()["description"]
    for vendor in vendors:
      if re.search(vendor.name, desc, re.IGNORECASE):
        print "vendor %s in desc" % vendor.name
        if WF and re.search('5th and Minna', r2.json()["name"], re.IGNORECASE):
          WFvendors.append(vendor.name)
        vendor.attended += 1
        vendor.save()

  if WF:
    HipChatModule.sendUpdate(WFvendors)

  return

if __name__ == '__main__':
  scrape()
