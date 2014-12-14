from django.conf.urls import patterns, url

from lunch import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<vendor_id>\d+)/$', views.detail, name='detail'),
)
