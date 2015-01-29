import sys, os
sys.path.append('/opt/myenv/gingerio/lunch')
os.environ['DJANGO_SETTINGS_MODULE'] = 'gingerio.settings'
from django.conf import settings

import django
django.setup()

import requests
from pyquery import PyQuery as pq
from lunch.models import Vendor

def getVendors():
  """Scrape vendors from site's raw html"""
  #r = requests.get('http://offthegridsf.com/vendors#food')
  URL = "http://offthegridsf.com/vendors#food"
  query = pq(url=URL)
  yo = query('.otg-vendor-name').find('.otg-vendor-name-link')
  vendors = yo.contents()
  vendors = list(set(vendors))
  vendors.append("Smothered Fries")
  vendors.sort()
  vendors[0] = vendors[0][1:]
  return vendors

def scrapeVendors():
  """Scrape and save vendors to database's vendor table"""
  vendors = getVendors()
  vendorsAdded = 0
  for x in vendors:
    # avoid adding duplicates to the Vendor table.
    # see if the vendor is already in the table
    try:
      Vendor.objects.get(name__iexact=x)
    # if its not in the table, add it
    except Vendor.DoesNotExist:
      v = Vendor(name=x)
      v.save()
      vendorsAdded += 1
    # else, move on to the next vendor
    else:
      continue

  print "Saved %d new vendors to db" % vendorsAdded

def resetVendors():
  """Reset vendor attended counts"""
  for x in Vendor.objects.all():
    x.attended = 0
    x.save()

def printVendors(attendedFilter):
  for x in Vendor.objects.all():
    if x.attended > attendedFilter:
      print "%s: %s, %d" % (x.name, x.date, x.attended)


def vendorAction(opt="print"):
  if opt == "scrape":
    scrapeVendors()
  elif opt == "reset":
    resetVendors()
  else:
    printVendors(0)
   
if __name__ == '__main__':
  vendorAction(sys.argv[1])
