
__all__ = [ 'first_ob', 'last_ob' ]

import merkatilo.core as core

def first_ob(s, dates=None):
    '''Return first available (dt,value) tuple.'''
    dates = dates or core.current_dates()
    f = s.f
    for dt in dates:
        val = f(dt)
        if core.is_valid_num(val):
            return (dt,val)
    return None

def last_ob(s, dates=None):
    '''Return last available (dt,value) tuple.'''
    dates = dates or core.current_dates()
    dv = dates.vec
    f = s.f
    for ndx in range(len(dv)-1,-1,-1):
        dt = dv[ndx]
        val = f(dt)
        if core.is_valid_num(val):
            return (dt,val)
    return None



#=========================================

from merkatilo.common_testing_base import CommonTestingBase

class FirstLastTests(CommonTestingBase):

    def testFirstOb(self):
        self.assertEqual(first_ob(self.TEST_SERIES)[0], core.to_jdate('2012-1-3'))

    def testLastOb(self):
        self.assertEqual(last_ob(self.TEST_SERIES)[0], core.to_jdate('2014-12-31'))
