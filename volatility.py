

__all__ = [ 'volatility' ]

from private.standard_deviation import standard_deviation
from private.series_dates_values import series_dates_values
from momentum import mo_days

import core

def volatility (s, days=365, dates=None):

    '''volatility is the standard deviation of the mo_days calculation.'''
    
    dates = dates or core.current_dates()
    vals = series_dates_values(mo_days(s,days=days,dates=dates),dates)
    return standard_deviation(vals)


#=====================================

import unittest, obs_series
from private.test_support import TEST_SERIES_OBS

class test_volatility(unittest.TestCase):

    def test_volatility(self):
        TEST_SERIES = obs_series.obs_to_series(TEST_SERIES_OBS)
        dates = core.dates(TEST_SERIES)
        v = volatility(TEST_SERIES, days=200,dates=dates)
        self.assertEqual(v, 0.0468086666214253)
