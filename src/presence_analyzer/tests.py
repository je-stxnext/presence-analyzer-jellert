# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""

import datetime
import json
import os.path
import unittest

from presence_analyzer import helpers
from presence_analyzer import main
from presence_analyzer import utils
from presence_analyzer import views  # pylint: disable=unused-import


TEST_DATA_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.csv'
)

TEST_DATA_XML = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.xml'
)

TEST_INI_FILENAME = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'test_debug.ini'
)


# pylint: disable=maybe-no-member, too-many-public-methods
class PresenceAnalyzerViewsTestCase(unittest.TestCase):
    """ Views tests. """

    def setUp(self):
        """ Before each test, set up a environment. """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV,
                                'DATA_XML': TEST_DATA_XML})
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
        self.assertEqual(len(data), 3)
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

    def test_user_picture_view(self):
        """ Test presence of a user picture. """
        data = utils.get_users_from_xml()
        min_user = min(data.keys())

        resp = self.client.get('/api/v1/pictures/%s' % min_user)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        resp = self.client.get('/api/v1/pictures/%s' % (min_user-1))
        self.assertEqual(resp.status_code, 404)


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """ Utility functions tests. """

    def setUp(self):
        """ Before each test, set up a environment. """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV,
                                'DATA_XML': TEST_DATA_XML})

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
        self.assertEqual(utils.get_time_from_seconds(0), [0, 0, 0])
        self.assertEqual(utils.get_time_from_seconds(60), [0, 1, 0])
        self.assertEqual(utils.get_time_from_seconds(50714), [14, 05, 14])
        self.assertRaises(ValueError, utils.get_time_from_seconds, -123)

    def test_get_users_from_xml(self):
        """ Test parsing of xml users file. """
        data = utils.get_users_from_xml()
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data[10], dict)


class PresenceAnalyzerHelpersTestCase(unittest.TestCase):
    """ Helper functions tests. """

    def setUp(self):
        """ Before each test, set up a environment. """

    def tearDown(self):
        """ Get rid of unused objects after each test. """
        pass

    def test_get_users_from_xml(self):
        """ Test parsing existence of xml users file. """
        self.assertIsNotNone(os.path.exists(helpers.get_users_xml_file()))

    def test_get_users_url(self):
        """ Test parsing of xml users file. """
        self.assertIsNotNone(helpers.get_users_url())

    def test_save_user_from_www(self):
        """ Test saving of xml user file from WWW. """
        self.assertTrue(helpers.save_users_from_www())
        self.assertFalse(helpers.save_users_from_www(TEST_INI_FILENAME))


def suite():
    """ Default test suite. """
    base_suite = unittest.TestSuite()
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerViewsTestCase))
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerUtilsTestCase))
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerHelpersTestCase))
    return base_suite


if __name__ == '__main__':
    unittest.main()
