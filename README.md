OffThaGrid
==========
HipChat room: https://www.hipchat.com/gAPbd12VR

There's a couple modules I used for this project. Here's an overview of what they each do.

Module Overview
--------------

| Module | Purpose |
| ------------- | ----------- |
| events | **Clears** Events from database, **prints** Events from database (depending on sys.argv option)|
| vendors | **Scrapes** Vendors from [OffTheGrid](http://offthegridsf.com/vendors#food), **resets** all Vendor's attended attributes in database, **prints** Vendors from database (depending on sys.argv option) |
| hipChat | **Posts** all Vendors at 5th & Minna to [HipChat room] (https://www.hipchat.com/gAPbd12VR) |
| record | **Requests** all [Facebook Events](https://www.facebook.com/OffTheGridSF/events) for that day, **queries**  event description for Vendors, **calls** hipChat module, **updates** all Vendor attended attributes in database |


Crontab setup:
```
0 14  *   *   *    /path/to/project/record.sh >> /path/to/project/cron.log 2>&1
```

Install requirements in your virtualenv
```
pip install -r requirements.txt
```
Create db tables
```
python manage.py migrate
```
Run locally
```
python manage.py runserver
```
