#!/usr/bin/env python

# I am so so sorry
# http://www.metoffice.gov.uk/public/weather/marine-printable/shipping-forecast.html

import os
from random import randint

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import requests_cache
import tornado.ioloop
import tornado.web
import tornado.template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
requests_cache.install_cache(cache_name='/tmp/ShippingDogecast-cache', backend='sqlite', expire_after=900)

class BaseHandler(tornado.web.RequestHandler):
    def head(self):
        return

    def set_default_headers(self):
        """
        Sets caching header
        """
        self.set_header('Cache-Control', 'max-age=300, public')
        self.clear_header('Server')

class MainHandler(BaseHandler):
    def get(self):
        debug = os.environ.get("DOGECAST_DEBUG", False)
        loader = tornado.template.Loader("./templates")
        self.write(loader.load("home.html").generate(DEBUG=debug))

class JSONHandler(BaseHandler):
    def get(self):
        forecast_xml = "http://www.metoffice.gov.uk/public/data/CoreProductCache/ShippingForecast/Latest?concise"

        try:
            r = requests.get(forecast_xml)
        except requests.exceptions.RequestException:
            xml_data = open(BASE_DIR + '/data/forecast.xml')
        else:
            if r.status_code == 200:
                xml_data = r.text
            else:
                xml_data = open(BASE_DIR + '/data/forecast.xml')

        soup = BeautifulSoup(xml_data, "lxml")

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

        self.write({
            'areas' : areas,
            'last_updated' : "%s %s" % (date, time)
        })

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
        'becoming' : 'become',
        'mainly' : '',
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

# Launch app

def make_app():
    debug = os.environ.get("DOGECAST_DEBUG", False)
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/dogecast.json", JSONHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': './static' }),
    ], debug=debug)

if __name__ == "__main__": #pragma: no cover

    # Load environment vars
    load_dotenv(BASE_DIR + '/.env')

    # Create an app
    port = os.environ.get("DOGECAST_PORT", 8888)
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()