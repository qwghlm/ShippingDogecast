"""
Views for dogecast
"""
import re
import json
from random import randint

from bs4 import BeautifulSoup
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import cache_page, cache_control

from .settings import BASE_DIR

# I am so so sorry
# http://www.metoffice.gov.uk/public/weather/marine-printable/shipping-forecast.html

@cache_control(max_age=3600)
def home(request):
    """
    Return the homepage
    """
    template = 'home.html'
    dictionary = {}
    return render(request, template, dictionary)

@cache_page(60 * 15)
def dogecast_json(request):

    forecast_xml = "http://www.metoffice.gov.uk/public/data/CoreProductCache/ShippingForecast/Latest?concise"
    try:
        r = requests.get(forecast_xml)
    except requests.exceptions.RequestException:
        xml_data = open(BASE_DIR + 'forecast.xml')
    else:
        if r.status_code == 200:
            xml_data = r.text
        else:
            xml_data = open(BASE_DIR + 'forecast.xml')

    soup = BeautifulSoup(xml_data)

    date = soup.find('i').attrs['dt']
    time = soup.find('i').attrs['tm']

    # Get all forecasts out of the XML and turn into a dictionary
    areas = []
    for forecast in soup.findAll('af'):
        d = {}
        d['wind'] = forecast.find('w').text
        d['sea_state'] = forecast.find('ss').text
        d['weather'] = forecast.find('wt').text
        d['visibility'] = forecast.find('v').text

        for (key, value) in d.items():
            d[key] = random_doge_prefix() + dogeify(value) + random_doge_suffix()

        # Especially sorry for this line
        d['label'] = forecast.find('al').text.replace('Dogger', 'Doger')
        for (key, value) in d.items():
            d[key] = value.replace("..", '.')

        areas.append(d)

    return HttpResponse(json.dumps({
        'areas' : areas,
        'last_updated' : "%s %s" % (date, time)
    }), content_type="application/json")

# Helper functions

def dogeify(text):
    """
    Look, really sorry
    """
    translations = {
        'severe' : 'very',
        'occasionally' : 'occasion',
        ' backing' : '. such back.',
        ' veering' : '. such veer.',
        'squally' : 'squall',
        ',' : '.',
        'becoming' : 'become'
    }

    # I am so sorry
    text = text.lower()
    for (word, translation) in translations.items():
        text = text.replace(word, translation)

    return text

def random_doge_prefix():
    """
    So sorry
    """
    words = ['such', 'much', 'many', 'so', '', '']
    prefix = words[randint(0, len(words)-1)]
    return '%s ' % (prefix,)

def random_doge_suffix():
    words = ['wow', '', '']
    suffix = words[randint(0, len(words)-1)]
    return suffix and '. %s.' % suffix or ''
