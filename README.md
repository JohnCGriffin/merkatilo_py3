# merkatilo-py3
Merkatilo implemented in Python3

## Purpose

This library serves two goals.  First, it is used to perform active research in the stock market.  Secondly, it's a
nice size for programming research.  Other implementations exist in C++ and Racket. This version is implemented in Python3.  It is a library, not a complete system.  Specifically, you must add a data source.

## Setup

1) You need Python 3.5+
2) ``cd the-place-you-like-personal-python-libraries``
3) ``git clone this-repository-url``
4) ``cd merkatilo_py3``
5) run tests via ``make``

_Note that when running the test for the first time, test files are downloaded from another
github repository and placed in ``/tmp/merkatio-test-data/``._

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

Major operations typically associated with technical market analysis involve time series that map dates to numeric values.  The mapping function is handled by the ```series``` class and dates are contained within the ```dateset``` class.  In merkatilo, dates are simply julian date integers.  For instance, the first day of the year 2000 can be constructed via ``to_jdate("2000-1-1")``, yielding 2451545.  The date integers where chosen to match Postgres julians.  A special but common time series in merkatilo is a signal series which answers date queries with only (#f, 1, -1).

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





  







