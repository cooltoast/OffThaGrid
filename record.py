import sys, os
sys.path.append('/opt/myenv/gingerio/lunch')
os.environ['DJANGO_SETTINGS_MODULE'] = 'gingerio.settings'
from django.conf import settings

from lunch.models import Event, Vendor
import json
import re
import requests
import time
from datetime import datetime, timedelta

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
  vendors = [x.name for x in Vendor.objects.all()]
  for event in r.json()["data"]:
    eventId = event["id"]
    print "getting %s's desc" % eventId
    eventUrl = getEventURL(eventId)
    r2 = requests.get(eventUrl)
    desc = r2.json()["description"]
    for vendor in vendors:
      if bool(re.search(vendor, desc, re.IGNORECASE)):
        print "vendor %s in desc" % vendor



  import pdb;pdb.set_trace()



  

if __name__ == '__main__':
  scrape()
