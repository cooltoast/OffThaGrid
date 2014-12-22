import sys, os
sys.path.append('/opt/myenv/gingerio/lunch')
os.environ['DJANGO_SETTINGS_MODULE'] = 'gingerio.settings'
from django.conf import settings

import django
django.setup()

from lunch.models import Event

def clearEvents():
  Event.objects.all().delete()

def printEvents():
  for x in Event.objects.all():
    print "%s: %s" % (x.name, x.date)

def eventAction(opt):
  if opt == "clear":
    clearEvents()
  else:
    printEvents()

if __name__ == '__main__':
  eventAction(sys.argv[1])
