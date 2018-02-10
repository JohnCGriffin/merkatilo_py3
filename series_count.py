
__all__ = [ 'series_count' ]

import core

def series_count(s, dates=None):
    
    '''Return the number of observations.  The typical
    use of this is in unit testing.'''
    
    dates = dates or core.current_dates()
    def valid(dt):
        return core.is_valid_num(s.f(dt))
    return sum((1 for dt in dates if valid(dt)))


#=======================================

from common_testing_base import *
from momentum import mo

class SeriesCountTest(CommonTestingBase):

    # The test series has several repeated values which
    # tests inclusion of zero in the momentum.
    def testCountAfterMo1(self):
        base_count = series_count(self.TEST_SERIES)
        mo_1_count = series_count(mo(self.TEST_SERIES,1))
        self.assertEqual(base_count, mo_1_count+1)
