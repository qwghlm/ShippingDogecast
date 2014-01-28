"""
URLs for dogecast
"""
#pylint:disable=C0103
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dogecast.views.home', name='home'),
    url(r'^dogecast\.json$', 'dogecast.views.dogecast_json', name='json'),
)
