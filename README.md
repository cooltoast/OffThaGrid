OffThaGrid
==========
HipChat room: https://www.hipchat.com/gg6xjAniq

There's a couple modules I used for this project. Here's an overview of what they each do.

Module Overview
--------------

| Module | Purpose |
| ------------- | ----------- |
| events | **Clears** Events from database, **prints** Events from database (depending on sys.argv option)|
| vendors | **Scrapes** Vendors from [OffTheGrid](http://offthegridsf.com/vendors#food), **resets** all Vendor's attended attributes in database, **prints** Vendors from database (depending on sys.argv option) |
| hipChat | **Posts** all Vendors at 5th & Minna to [HipChat room] (https://www.hipchat.com/gg6xjAniq) |
| record | **Requests** all [Facebook Events](https://www.facebook.com/OffTheGridSF/events) for that day, **queries**  event description for Vendors, **calls** hipChat module, **updates** all Vendor attended attributes in database |

To Run Locally
----

Install pip requirements in your virtualenv
```
pip install -r requirements.txt
```

In ```gingerio/settings.py```, set:
```
DEBUG = True
```
and
```
STATIC_ROOT = '/absolute-path-to-project/static/'
STATICFILES_DIRS = (
  '/absolute-path-to-project/lunch/static/', # dont use ~ here
)

```
Collect static files 
```
python manage.py collectstatic
```
Apply any migrations
```
python manage.py migrate
```
Run locally
```
python manage.py runserver
```

Crontab setup:
-----
To make the ```record.sh``` script run at 11am PST everyday, run ```sudo crontab -e``` and add this line: 
```
0 19  *   *   *    /path/to/project/record.sh >> /path/to/project/cron.log 2>&1
```
