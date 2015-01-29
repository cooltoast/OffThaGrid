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
Create your postgres db
```
sudo su - postgres
createdb <db>
pqsl
GRANT ALL PRIVILEGES ON DATABASE <db> TO <you>;
```
Add those credentials to ```gingerio/settings.py```
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or             'oracle'.
        'NAME': '<db>', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '<you>',
        'PASSWORD': '<password>',
        'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}
```
Install pip requirements in your virtualenv
```
virtualenv <env>
source <env>/bin/activate
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

Scraping Vendors from [Off The Grid's website](http://offthegridsf.com/vendors#food)
------
```
python vendors.py scrape
```
Grabbing today's vendor appearances from [Facebook](https://www.facebook.com/OffTheGridSF/events)
-----
```
python record.py
```

Crontab setup:
-----
To make the ```record.sh``` script run at 11am PST everyday, run ```sudo crontab -e``` and add this line: 
```
0 19  *   *   *    /path/to/project/record.sh >> /path/to/project/cron.log 2>&1
```
