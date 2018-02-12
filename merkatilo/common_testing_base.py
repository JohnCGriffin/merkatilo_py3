__all__ = [ 'CommonTestingBase', 'approx', 'obs_to_series' ]

import unittest
from merkatilo.obs_series import obs_to_series
from merkatilo.private.test_support import TEST_SERIES_OBS, approx

import merkatilo.core as core

class CommonTestingBase(unittest.TestCase):

    def setUp(self):
        self.TEST_SERIES = obs_to_series(TEST_SERIES_OBS)
        core.current_dates(core.dates(self.TEST_SERIES))

