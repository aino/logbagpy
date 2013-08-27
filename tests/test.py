import unittest
import os
import sys
import urllib2
import urllib
import threading


params = {}

# monkey patching
def urlopen(url, data):
    global params
    params = {'url': url, 'data': data}

def urlencode(data):
    return data

class Thread(object):
    def __init__(self, target, args, kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def start(self):
        self.target(*self.args, **self.kwargs)


urllib2.urlopen = urlopen
urllib.urlencode = urlencode
threading.Thread = Thread


# path patch
here = os.path.abspath( os.path.dirname(__file__) )
sys.path[0:0] = ['../..', '..']

import logbag


class TestLogbag(unittest.TestCase):

    def setUp(self):
        self.log = logbag.Logger('url', 'user', 'log', 'info')
        global params
        params = None

    def test_lowlevel(self):
        self.log.debug('msg')
        self.assertEqual(params, None)

    def test_data_and_level(self):
        self.log.info('msg')
        self.assertEqual(params['url'], 'url')
        self.assertEqual(params['data']['user'], 'user')
        self.assertEqual(params['data']['log'], 'log')

    def test_level(self):
        self.log.warning('msg')
        self.assertEqual(params['data']['level'], 'warning')

    def test_xxx_level(self):
        self.log.log('xxx', 'yyy')
        self.assertEqual(params['data']['level'], 'xxx')
        self.assertEqual(params['data']['message'], 'yyy')


def run_tests(verbosity=2):
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLogbag)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
