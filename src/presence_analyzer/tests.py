# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
import os.path
import json
import datetime
import unittest

from presence_analyzer import main
from presence_analyzer import utils
from presence_analyzer import views  # pylint: disable=unused-import
from presence_analyzer.utils import get_time_from_seconds


TEST_DATA_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.csv'
)


# pylint: disable=maybe-no-member, too-many-public-methods
class PresenceAnalyzerViewsTestCase(unittest.TestCase):
    """ Views tests. """

    def setUp(self):
        """ Before each test, set up a environment. """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})
        self.client = main.app.test_client()

    def tearDown(self):
        """ Get rid of unused objects after each test. """
        pass

    def test_mainpage(self):
        """ Test main page redirect. """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        assert resp.headers['Location'].endswith('/presence_weekday.html')

    def test_api_users(self):
        """ Test users listing. """
        resp = self.client.get('/api/v1/users')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)
        self.assertDictEqual(data[0], {u'user_id': 10, u'name': u'User 10'})

    def test_mean_time_weekday(self):
        """ Test mean time weekday. """
        data = utils.get_data()
        min_user = min(data.keys())

        resp = self.client.get('/api/v1/mean_time_weekday/%s' % (min_user-1))
        self.assertEqual(resp.status_code, 404)

        for user_id in data:
            resp = self.client.get('/api/v1/mean_time_weekday/%s' % user_id)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.content_type, 'application/json')

        resp = self.client.get('/static/mean_time_weekday.html')
        self.assertEqual(resp.status_code, 200)

    def test_presence_weekday(self):
        """ Test presence weekday. """
        data = utils.get_data()
        min_user = min(data.keys())

        resp = self.client.get('/api/v1/presence_weekday/%s' % (min_user-1))
        self.assertEqual(resp.status_code, 404)

        for user_id in data:
            resp = self.client.get('/api/v1/presence_weekday/%s' % user_id)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.content_type, 'application/json')

        resp = self.client.get('/static/presence_weekday.html')
        self.assertEqual(resp.status_code, 200)

    def test_presence_start_end_view(self):
        """ Test presence of start and end means. """
        data = utils.get_data()
        min_user = min(data.keys())

        resp = self.client.get('/api/v1/presence_start_end/%s' % (min_user-1))
        self.assertEqual(resp.status_code, 404)

        for user_id in data:
            resp = self.client.get('/api/v1/presence_start_end/%s' % user_id)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.content_type, 'application/json')

        resp = self.client.get('/static/presence_start_end.html')
        self.assertEqual(resp.status_code, 200)


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """ Utility functions tests. """

    def setUp(self):
        """ Before each test, set up a environment. """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})

    def tearDown(self):
        """ Get rid of unused objects after each test. """
        pass

    def test_get_data(self):
        """ Test parsing of CSV file. """
        data = utils.get_data()
        self.assertIsInstance(data, dict)
        self.assertNotEqual(data, {})
        self.assertItemsEqual(data.keys(), [10, 11])
        sample_date = datetime.date(2013, 9, 10)
        self.assertIn(sample_date, data[10])
        self.assertItemsEqual(data[10][sample_date].keys(), ['start', 'end'])
        self.assertEqual(
            data[10][sample_date]['start'],
            datetime.time(9, 39, 5)
        )

    def test_get_time_from_seconds(self):
        """ Test for conversion from seconds to hours, minutes, seconds. """
        self.assertEqual(get_time_from_seconds(0), [0, 0, 0])
        self.assertEqual(get_time_from_seconds(60), [0, 1, 0])
        self.assertEqual(get_time_from_seconds(50714), [14, 05, 14])
        self.assertRaises(ValueError, get_time_from_seconds, -123)


def suite():
    """ Default test suite. """
    base_suite = unittest.TestSuite()
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerViewsTestCase))
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerUtilsTestCase))
    return base_suite


if __name__ == '__main__':
    unittest.main()
