from django.conf.urls import patterns, include, url

from dhmadness.dhmaddness.views import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^(?P<ride_id>\d+)/$', index),
)