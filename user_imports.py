
# I am open to suggestions about how to properly reexport modules.
# - John Griffin (griffinish@gmail.com)

import conviction    as imported_lib_conviction
import core          as imported_lib_core
import cross         as imported_lib_cross
import dump          as imported_lib_dump
import ema           as imported_lib_ema
import fudge         as imported_lib_fudge
import load          as imported_lib_load
import min_max       as imported_lib_min_max
import momentum      as imported_lib_momentum
import repeated      as imported_lib_repeated
import series_binop  as imported_lib_series_binop
import series_count  as imported_lib_series_count
import series_filter as imported_lib_series_filter
import series_logic  as imported_lib_series_logic
import series_map    as imported_lib_series_map
import signals       as imported_lib_signals
import sma           as imported_lib_sma
import sugar         as imported_lib_sugar
import unrepeated    as imported_lib_unrepeated
import volatility    as imported_lib_volatility
import warp          as imported_lib_warp

def reexports (*libs):
    d = {}
    for lib in libs:
        for name in lib.__all__:
            if name in d:
                raise Exception('libs {} and {} clash on name {}'.format(d[name],lib,name))
            d[name] = lib
            globals()[name] = getattr(lib,name)
    for key in [ k for k in globals().keys() if k.startswith('imported_lib__') ]:
        globals().pop(k)
    return [ name for name in sorted(d.keys()) ]

__all__ = reexports( imported_lib_conviction,
                     imported_lib_core,
                     imported_lib_cross,
                     imported_lib_dump,
                     imported_lib_ema,
                     imported_lib_fudge,
                     imported_lib_load,
                     imported_lib_min_max,
                     imported_lib_momentum,
                     imported_lib_repeated,
                     imported_lib_series_binop,
                     imported_lib_series_count,
                     imported_lib_series_filter,
                     imported_lib_series_logic,
                     imported_lib_series_map,
                     imported_lib_signals,
                     imported_lib_sma,
                     imported_lib_sugar,
                     imported_lib_unrepeated,
                     imported_lib_volatility,
                     imported_lib_warp)
