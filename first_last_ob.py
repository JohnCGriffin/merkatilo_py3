
__all__ = [ 'first_ob', 'last_ob', 'first_value', 'last_value' ]

import core

def first_ob(s, dates=None):
    dates = dates or core.current_dates()
    f = s.f
    for dt in dates:
        val = f(dt)
        if core.is_valid_num(val):
            return (dt,val)
    return None

def last_ob(s, dates=None):
    dates = dates or core.current_dates()
    dv = dates.vec
    f = s.f
    for ndx in range(len(dv)-1,-1,-1):
        dt = dv[ndx]
        val = f(dt)
        if core.is_valid_num(val):
            return (dt,val)
    return None

def first_value(s, dates=None):
    ob = first_ob(s,dates=dates)
    return ob[1] if ob else None

def last_value(s, dates=None):
    ob = last_ob(s,dates=dates)
    return ob[1] if ob else None



#=========================================

import unittest
from private.test_support import TEST_SERIES_OBS
from obs_series import obs_to_series

class FirstLastTests(unittest.TestCase):

    def setUp(self):
        self.TEST_SERIES = obs_to_series(TEST_SERIES_OBS)
        core.current_dates(core.dates(self.TEST_SERIES))

    def testFirstOb(self):
        self.assertEqual(first_ob(self.TEST_SERIES)[0], core.to_jdate('2012-1-3'))

    def testLastOb(self):
        self.assertEqual(last_ob(self.TEST_SERIES)[0], core.to_jdate('2014-12-31'))
