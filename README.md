# merkatilo-py3
[Merkatilo](http://merkatilo.org) implemented in Python3 

## Purpose

This library serves two goals.  First, it is used to perform 
active research in financial markets.  Secondly, this Python3 library a
nice size for programming research along with its sibling implementations in C++ and Racket. 
This is only a library, not a complete system.  Most importantly, to make it useful,
you must add a data source.

## Setup

1) You need Python 3.5+
2) ``cd the-place-you-like-personal-python-libraries``
3) ``git clone this-repository-url``
4) ``cd merkatilo_py3``
5) run tests via ``make``

_Note that when running the test for the first time, test files are downloaded from another
github repository and placed in ``/tmp/merkatilo-test-data/``._

## Get some data

You will eventually need a data source.  Time series data are loaded into the system via the ``lo`` operator, e.g. ``lo('SPY')``.  Modify load.py to suit your needs.

Also note that a built-in series exists for testing - use 

```
from merkatilo.private.test_support import TEST_SERIES_OBS
from merkatilo.obs_series import obs_to_series
TEST_SERIES = obs_to_series(TEST_SERIES_OBS)
```
You can play with that until you decide where to get your data.  

## Usage Overview

Major operations typically associated with technical market analysis involve time series that map dates to numeric values.  The mapping function is handled by the ```series``` class and dates are contained within the ```dateset``` class.  In merkatilo, dates are simply julian date integers.  For instance, the first day of the year 2000 can be constructed via ``to_jdate("2000-1-1")``, yielding 2451545.  The date integers where chosen to match Postgres julians.  A special but common time series in merkatilo is a signal series which answers date queries with only (None, 1, -1).

The following example loads the SPY ETF, sets the active dates parameter, and does a 200 period cross to create a signal series showing buy and sell signals.  The utility operator dump prints out the SPY series, the 200 period smoothing and the cross.

```
from merkatilo import *
SPY = lo_set_dates("SPY")
smoothed = sma(SPY,200)
dump(SPY, smoothed, cross(slower=smoothed,faster=SPY))

```

## Making New Series Operations

A merkatilo.series is a simple class wrapper of a function which answers a date query 
with either a real number or None.  So, if you wanted to take the log of a different series,
one possible mechanism would be:

```
from merkatilo.core import is_valid_num
from merkatilo import series
def log_series (another_series):
	def f(date):
		val = another_series.f(date)
		return math.log(val) if is_valid_num(val) else None
	return series(f)
```

Of course, an easier way to accomplish that is
```
series_map(math.log,another_series)
```


- - -
MIT License

Copyright (c) 2018 John C. Griffin, 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


