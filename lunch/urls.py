from django.conf.urls import patterns, url

from lunch import views

urlpatterns = patterns('',
    url(r'^$', views.lunch, name='lunch'),
    url(r'^(?P<vendor_id>\d+)/$', views.vendor, name='vendor'),
)
