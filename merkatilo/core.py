
__all__ = [ 'ymd_to_jdate',
            'jdate_to_ymd',
            'first_date',
            'last_date',
            'is_jdate',
            'set_dates',
            'jdate_year',
            'jdate_month',
            'jdate_day',
            'jdate_weekday',
            'jdate_to_text',
            'text_to_jdate',
            'to_jdate',
            'nearest',
            'today',
            'MAX_DATE',
            'MIN_DATE','series', 'vector_series', 'dates', 'dateset',
            'current_dates', 'date_scope', 'date_range' ]

import datetime
import unittest
import threading
import bisect

def set_dates(item):
    '''shortcut to current_dates(dates(item))'''
    current_dates(dates(item))

def first_date(dates=None):
    '''first date of specified dates or current_dates()'''
    dates = dates or current_dates()
    return dates.vec[0]

def last_date(dates=None):
    '''last date of specified dates or current_dates()'''
    dates = dates or current_dates()
    return dates.vec[-1]

def nearest(dt, dates=None, or_later=False):
    
    '''nearest returns the exact date or the one just
    earlier if or_later is False or later if or_later is True.'''
    
    dates = dates or current_dates()
    dv = dates.vec
    if dv[0] <= dt <= dv[-1]:
        ndx = bisect.bisect_left(dv,dt)
        found = dv[ndx]
        if found == dt or next:
            return found
        return dv[ndx-1]
    return None
            

def ymd_to_jdate (year, month, day):
    
    '''Calculate jdate from year,month,day. Input values are verified'''
    
    def leap_year (y):
        if y % 4 > 0:
            return False
        if y % 400 == 0:
            return True
        if y % 100 == 0:
            return False
        return True

    def verify():

        if not (MIN_YEAR <= year <= MAX_YEAR):
            return False

        if not (0 < month < 13):
            return False

        if month == 2:
            if day == 29:
                return leap_year(year)
            return 0 < day < 29
        
        if month in (1,3,5,7,8,10,12):
            return (0 < day < 32)

        return 0 < day < 31

    if not verify():
        raise Exception ("bad date (year = {}, month = {}, day = {})".format(year,month,day))


    a = (14 - month) // 12
    y = (year + 4800 - a)
    m = (month + (12 * a) - 3)

    return (day
            + (((153 * m) + 2) // 5)
            + (365 * y)
            + (y // 4)
            - (y // 100)
            + (y // 400)
            - 32045)


def jdate_to_ymd (julian):
    
    '''Convert jdate to year,month,day tuple'''
    
    JD = round(julian)
    L = JD + 68569
    M = (L * 4) // 146097
    N = L - ((146097 * M) + 3) // 4
    O = (4000 * (N + 1)) // 1461001
    P = N - ((1461 * O) // 4) + 31
    Q = (80 * P) // 2447
    R = P - ((2447 * Q) // 80)
    S = Q // 11
    T = Q + 2 + (-12 * S)
    U = (100 * (M - 49)) + O + S
    return (U,T,R)


MIN_YEAR = 1700
MAX_YEAR = 2100
MIN_DATE = ymd_to_jdate(MIN_YEAR,1,1)
MAX_DATE = ymd_to_jdate(MAX_YEAR,12,31)


def is_jdate(j):
    '''Is the argument a jdate?'''
    return type(j) == type(1) and (MIN_DATE <= j <= MAX_DATE)

def jdate_year(dt):
    '''Extract year from jdate.'''
    y,m,d = jdate_to_ymd(dt)
    return y

def jdate_month(dt):
    '''Extract base-1 month from jdate'''
    y,m,d = jdate_to_ymd(dt)
    return m

def jdate_day(dt):
    '''Extract day of month from jdate'''
    y,m,d = jdate_to_ymd(dt)
    return d;

def jdate_weekday(dt):
    '''Extract the day of the week from a jdate, 0=Sunday, 6=Saturday'''
    return (dt+1) % 7


def jdate_to_text(dt):
    '''Create text representation of jdate'''
    ymd = jdate_to_ymd(dt)
    return '{:04}-{:02}-{:02}'.format(*ymd)

def text_to_jdate(date_text):
    '''Create jdate from text representation'''
    return ymd_to_jdate(*[ int(f) for f in date_text.split("-") ])

def to_jdate(item):
    '''Pass through jdate and convert text to jdate'''
    if is_jdate(item):
        return item
    t = type(item)
    if type('s') == t:
        return text_to_jdate(item)
    raise Exception("to_jdate argument must be date or string of date, not {}".format(t))


def today(offset=0):

    '''With offset defaulted to zero, get jdate representing today.
    Thus, yesterday is today(-1).'''
    
    d = datetime.datetime.now().date()
    return ymd_to_jdate(d.year,d.month,d.day) + offset


#======================================================

class test_jdate(unittest.TestCase):

    def test_conversion(self):
        converted = jdate_to_text(to_jdate('2000-3-3'))
        self.assertEqual(converted, "2000-03-03")

    def test_years(self):
        self.assertEqual(to_jdate('2012-12-31') + 1, to_jdate('2013-1-1'))
        self.assertEqual(to_jdate('2000-1-1') - to_jdate('1999-1-1'), 365)
        self.assertEqual(to_jdate('2005-1-1') - to_jdate('2004-1-1'), 366)

    def test_weekday(self):
        new_millenium = to_jdate('2000-1-1')
        self.assertEqual([ jdate_weekday(new_millenium+i) for i in range(8) ],
                         [6,0,1,2,3,4,5,6]) # new-millenium was Saturday

    def test_leap_year(self):
        self.assertIsNotNone(ymd_to_jdate(2004,2,29))
        with self.assertRaises(Exception):
            ymd_to_jdate(2003,2,29)

    def test_unique_formatted_dates(self):
        start_date = to_jdate('2000-1-1')
        s1 = { start_date+i for i in range(100) }
        s2  = { len(jdate_to_text(dt)) for dt in s1 }
        self.assertEqual((len(s1), len(s2), list(s2)[0]), (100,1,10))


import numbers

def is_valid_num(x):
    '''Used pervasively within library to identify non-NaN numbers.'''
    return (isinstance(x,numbers.Number)) and x == x

def normalize_val(val):
    return None if (val is None or val is False) else val

def normalize_to_False(f):
    def normalizer(dt):
        return normalize_val(f(dt))
    return normalizer

class series(object):

    '''series is the merkatilo container with a name
    and a function mapping date to float|None.'''
    
    def __init__(self, f, name=None, require_normalization_wrapper=True):
        self.f = normalize_to_False(f) if require_normalization_wrapper else f
        self.name = name
        
    def first_date(self):
        return None
    
    def last_date(self):
        return None

    def __repr__(self):
        return '<series:{}>'.format((self.name if self.name else super().__repr__()))

class vector_series(series):

    '''A subclass of series, vector_series is used within the library.'''
    
    def __init__(self, vec, first_date, name=None):
        if not is_jdate(first_date):
            raise Exception("first_date unexpected type {}".format(type(first_date)))
        for ndx,n in enumerate(vec):
            if n and (n != n):
                raise Exception('vector_series given NaN at {}'.format(
                    jdate_to_text(ndx+first_date)))
            if not n:
                vec[ndx] = normalize_val(n)
        last_date = first_date + len(vec) - 1
        def myfunc(dt):
            return vec[dt-first_date] if (first_date <= dt <= last_date) else None
        self._first_date = first_date
        self._last_date = last_date
        super().__init__(myfunc,name=name,require_normalization_wrapper=False)

    def first_date(self):
        return self._first_date

    def last_date(self):
        return self._last_date



def to_date(item):

    '''If None,False or jdate, pass it through.  
    Otherwise, attempt conversion via to_jdate.'''

    return item and to_jdate(item)

class dateset(object):

    '''A dateset wraps an ordered vector of jdate integers.  Generally
       one constructs a dateset via the "dates" function.'''
    
    def __init__(self, vec, check_vector_validity=True):
        self.vec = vec
        if check_vector_validity:
            if type(vec) != type([]):
                raise Exception("dateset requires list of ordered dates")
            if not len(vec):
                raise Exception("dateset requires non-empty list of ordered dates")
            prev = vec[0]-1
            for dt in vec:
                if not is_jdate(dt):
                    raise Exception("encountered non-jdate in dateset constructor")
                if dt <= prev:
                    raise Exception("dateset dates not in order")

    def first_date(self):
        return self.vec[0]

    def last_date(self):
        return self.vec[-1]

    def __iter__(self):
        return self.vec.__iter__()

    def __repr__(self):
        return '<dateset:{}..{}>'.format(jdate_to_text(self.first_date()),
                                         jdate_to_text(self.last_date()))

class date_range(object):

    '''date_range describes a range of dates.'''

    def __init__(self, first, last):
        first = to_date(first)
        last = to_date(last)
        self.first = first
        self.last = last
        if not (first or last):
            raise Exception("specified date_range with neither first nor last")
        if first and last and (first > last):
            raise Exception("reversed date_range constructor arguments")

    def in_range(self, dt):
        dt = to_date(dt)
        if self.first and self.first > dt:
            return False
        if self.last and self.last < dt:
            return False
        return True

    def __repr__(self):
        return '<date_range:{}..{}>'.format(jdate_to_text(self.first),
                                           jdate_to_text(self.last))
        
def dates(*specs, first=None, last=None, expanded=False, union=False):

    '''The dates() call is a flexible way to create a dateset.  Inputs can be
    one or more specifications by dateset, date_range, or series.  These are
    further constrained by optional "first" and "last" dates.  By default,
    the intersection of the specifications defines the resulting set, but with
    "union" set to true, the union of the specifications is used.  Finally, if
    the "expanded" parameter is set True, the final set is then filled on every
    calendar day between the end points.'''

    def to_predicate(spec):
        if isinstance(spec,series):
            def f(dt):
                val = spec.f(dt)
                return not (val is None or val is False)
            return f
        if isinstance(spec,date_range):
            return spec.in_range
        if type(spec) == set:
            return lambda dt: dt in spec
        if type(spec) == dateset:
            return to_predicate(set(spec.vec))
        raise Exception ("unsupported date predicate type {}".format(type(spec)))

    preds = [ to_predicate(spec) for spec in specs ]

    min_date = to_date(first) or MIN_DATE
    max_date = to_date(last) or MAX_DATE

    if min_date > max_date:
        raise Exception("first/last parameters out of order")

    for spec in specs:
        if type(spec) == date_range:
            if spec.first:
                min_date = max(min_date,spec.first)
            if spec.last:
                max_date = min(max_date,spec.last)
        if type(spec) == dateset:
            min_date = max(min_date, spec.vec[0])
            max_date = min(max_date, spec.vec[-1])

    result = []
    for dt in range(min_date,max_date+1):
        ok = not union
        for p in preds:
            if union:
                ok = ok or p(dt)
            else:
                ok = ok and p(dt)
        if ok:
            result.append(dt)

    if expanded:
        result = [ dt for dt in range(result[0],result[-1]+1) ]


    return dateset(result, check_vector_validity=False)
    
__local = threading.local()
__local.current_dates = dates({ today() })

def current_dates(dts=None):

    '''Thread-local setting of active dateset.  Most commands utilize this value as 
    the default if no dates= argument is given.'''

    if dts:
        if not isinstance(dts,dateset):
            raise Exception('current_dates requires dateset but received {}'.format(type(dts)))
        __local.current_dates = dts
    return __local.current_dates

class date_scope(object):

    '''For use with the "with" keyword, set a scoped area in which current_dates
    thread_local is set to a date specification (i.e. date_range, dateset, series).'''

    def __init__(self, spec):
        self.dates = dates(spec)
        self.previous_dates = current_dates()
    def __enter__(self):
        current_dates(self.dates)
    def __exit__(self, exc_type, exc_value, traceback):
        current_dates(self.previous_dates)



#==================================================

class test_dates(unittest.TestCase):

    def test_contiguous_dates(self):
        dts = dates(date_range('2008-7-1','2009-1-1'), first='2001-1-1', last='2010-1-1')
        for (d1,d0) in zip(dts.vec[1:], dts.vec):
            self.assertEqual(d1-1,d0)

    def test_backwards_specification(self):
        with self.assertRaises(Exception):
            dates(first='2001-1-1', last='2000-1-1')

    
