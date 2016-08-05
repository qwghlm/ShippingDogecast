"""
Test case
"""
import json
import re
from urllib import urlencode

import requests
from tornado.testing import AsyncHTTPTestCase
from mock import patch

from main import make_app, BASE_DIR

class BaseTestCase(AsyncHTTPTestCase):
    """
    Base test case
    """
    def get_app(self):
        """
        Overrides basic method, gets app
        """
        # Assumption is environment has already been loaded by the test runner,
        # else the below will fail
        application = make_app()
        return application

#pylint:disable=too-few-public-methods,no-init
class MockRequestsResponse:
    """Mock response from requests library"""
    status_code = 200
    text = open(BASE_DIR + '/data/forecast.xml').read()

class MockFailedRequestsResponse:
    """Mock response from requests library"""
    status_code = 404
    text = "File not found"

class DogecastTestCase(BaseTestCase):

    def test_homepage(self):
        """
        Test homepage
        """
        # Test for home
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

    def _test_json(self):
        """
        Test JSON
        """
        # Test for home
        response = self.fetch('/dogecast.json')
        self.assertEqual(response.code, 200)

        body = json.loads(response.body)
        self.assertEqual(body['last_updated'], '2014-01-28 1030')
        self.assertEqual(len(body['areas']), 17)
        labels = [area['label'] for area in body['areas'] if 'Doger' in area['label']]
        self.assertEqual(len(labels), 1)

    # Three tests - for successful download (patched), file not found, and request exception

    @patch('requests.get', return_value=MockRequestsResponse)
    def test_json(self, *args, **kwargs):
        self._test_json()

    @patch('requests.get', return_value=MockFailedRequestsResponse)
    def test_json_badcode(self, *args, **kwargs):
        self._test_json()

    @patch('requests.get', side_effect=requests.exceptions.RequestException)
    def test_json_error(self, *args, **kwargs):
        self._test_json()
