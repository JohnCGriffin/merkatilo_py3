

__all__ = [ 'volatility', 'volatility_residual' ]

from private.standard_deviation import standard_deviation
from private.series_dates_values import series_dates_values
from momentum import mo_days

import core

def volatility (s, days=365, dates=None):
    dates = dates or core.current_dates()
    vals = series_dates_values(mo_days(s,days=days,dates=dates),dates)
    return standard_deviation(vals)

def volatility_residual (s, days=365, dates=None):
    return 1.0 - volatility(s,days=days,dates=dates)



#=====================================

import unittest, obs_series
from private.test_support import TEST_SERIES_OBS

class test_volatility(unittest.TestCase):

    def test_volatility(self):
        TEST_SERIES = obs_series.obs_to_series(TEST_SERIES_OBS)
        dates = core.dates(TEST_SERIES)
        v = volatility(TEST_SERIES, days=200,dates=dates)
        self.assertEqual(v, 0.0468086666214253)
