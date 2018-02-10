
__all__ = [
    'date_range', 'dates', 'dateset', 'current_dates','date_scope',
    'today',
    'cross',
    'min_max_obs', 'min_ob', 'max_ob',
    'series_filter',
    'dump',
    'repeated',
    'unrepeated',
    'lo',
    'fudge',
    'ema',
    'sma',
    'warp',
    'conviction',
    'to_signals',
    'series_count',
    'add', 'sub', 'mul', 'div', 'lt', 'le', 'gt', 'ge',
    'series_or', 'series_and',
    'volatility', 'volatility_residual' ,
    'mo', 'mo_days',
    'set_dates',
    'lo_set_dates',
    ]

from cross import cross
from min_max import min_max_obs, min_ob, max_ob
from conviction import conviction
from core import dates, dateset, current_dates, date_scope, date_range
from core import today
from dump import dump
from ema import ema
from fudge import fudge
from load import lo
from momentum import mo, mo_days
from repeated import repeated
from series_binop import add, sub, mul, div, lt, le, gt, ge
from series_count import series_count
from series_filter import series_filter
from series_logic import series_and, series_or
from series_map import series_map
from signals import to_signals
from sma import sma
from unrepeated import unrepeated
from volatility import volatility, volatility_residual
from warp import warp

def set_dates(item):
    current_dates(dates(item))

def lo_set_dates(item):
    s = lo(item)
    set_dates(s)
    return s
