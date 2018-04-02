.. merkatilo documentation master file, created by
   sphinx-quickstart on Mon Feb 12 14:07:42 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python3 Implementation of Merkatilo
===================================

The merkatilo time-series library implementations address my 
personal financial computing research requirements.
This is the Python3 implementation.

The purpose of this library is financial computing research and
education, not trading with material funds at risk.
Use it accordingly.

Library code resides at
`Github <https://github.com/JohnCGriffin/merkatilo_py3>`_ under
MIT licensing.  Corrections, improvements, or other comments are welcome.
Please include merkatilo in the subject line.

John Griffin, griffinish at gmail


Overview
========

The basic data structures are a time series structure that wraps a simple
date-to-number function, a date, and a dateset which is an ordered collection
of dates. A time series is represented by series class which takes
only a date->optional-number function and a name. It is
the argument to many functions that beget new series instances.

The functions operating transforming series to new series come in two styles,
those oriented to a sequence of dates, and those that require no dateset.
For example, the :code:`ma` procedure creates a new series representing a running
average of the input series over some dateset. However, :code:`add` sums two input
series on a date without respect to any date sequence.

Speaking of dates, with merkatilo, they are called jdate, meaning julian date.
The julian date coincides with Postgres’ idea of a julian.

Here’s an example that loads the SPY ETF adjusted closing price, does a
cross of that series with its 200-period moving average, generating
buy (+1) and sell (-1) signals. Finally, it dumps them out in
date order, like a printed spreadsheet.

.. code-block:: python

   from merkatilo import *

   SPY = lo_set_dates('SPY')
   smoothed = ma(SPY,200)
   my_signals = cross(slower=smoothed, faster=SPY)
   dump(SPY, my_signals)


Please note that **if you attempt to do the example above, it will not work**.
That is because this library manipulates times series; it does not provide
financial data. You have to come up with that yourself. If you are just studying,
investigate using the
`St. Louis Federal Reserve FRED database <https://fred.stlouisfed.org/>`_,
`OECD <https://data.oecd.org/>`_,
and `Quandl <https://www.quandl.com/>`_.

   

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   merkatilo.core
   allocation_equity_line
   calibrate
   constant
   conviction
   cross
   drawdown
   dump
   ema
   equity_line
   first_last_ob
   fudge
   load
   ma
   min_max
   momentum
   obs_series
   performance
   repeated
   series_binop
   series_count
   series_filter
   series_logic
   series_map
   signals
   sugar
   unrepeated
   volatility
   warp

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
