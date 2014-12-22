from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'gingerio.views.home', name='home'),
    url(r'^lunch/', include('lunch.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
