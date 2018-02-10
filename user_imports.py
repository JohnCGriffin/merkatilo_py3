
# I am open to suggestions about how to properly reexport modules.
# - John Griffin (griffinish@gmail.com)

import conviction as lib_conviction
import core as lib_core
import cross as lib_cross
import dump as lib_dump
import ema as lib_ema
import fudge as lib_fudge
import load as lib_load
import min_max as lib_min_max
import momentum as lib_momentum
import repeated as lib_repeated
import series_binop as lib_series_binop
import series_count as lib_series_count
import series_filter as lib_series_filter
import series_logic as lib_series_logic
import series_map as lib_series_map
import signals as lib_signals
import sma as lib_sma
import sugar as lib_sugar
import unrepeated as lib_unrepeated
import volatility as lib_volatility
import warp as lib_warp

def reexports (*libs):
    d = {}
    for lib in libs:
        for name in lib.__all__:
            if name in d:
                raise Exception('libs {} and {} clash on name {}'.format(d[name],lib,name))
            d[name] = lib
            globals()[name] = getattr(lib,name)
    return [ name for name in sorted(d.keys()) ]

__all__ = reexports( lib_conviction,
                     lib_core,
                     lib_cross,
                     lib_dump,
                     lib_ema,
                     lib_fudge,
                     lib_load,
                     lib_min_max,
                     lib_momentum,
                     lib_repeated,
                     lib_series_binop,
                     lib_series_count,
                     lib_series_filter,
                     lib_series_logic,
                     lib_series_map,
                     lib_signals,
                     lib_sma,
                     lib_sugar,
                     lib_unrepeated,
                     lib_volatility,
                     lib_warp)
