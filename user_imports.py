#
# I am open to suggestions about how to properly reexport modules.
# - John Griffin (griffinish@gmail.com)
#
# The intent of this module is to, yes, splatter the user's environment
# with bindings because that's the way this library is used interactively.
# You are of course not obligated to import this.
#
# For me, within iPython, I will:
#
# from user_imports import *
#

import conviction    as __imported_lib_conviction
import core          as __imported_lib_core
import cross         as __imported_lib_cross
import dump          as __imported_lib_dump
import ema           as __imported_lib_ema
import fudge         as __imported_lib_fudge
import load          as __imported_lib_load
import min_max       as __imported_lib_min_max
import momentum      as __imported_lib_momentum
import repeated      as __imported_lib_repeated
import series_binop  as __imported_lib_series_binop
import series_count  as __imported_lib_series_count
import series_filter as __imported_lib_series_filter
import series_logic  as __imported_lib_series_logic
import series_map    as __imported_lib_series_map
import signals       as __imported_lib_signals
import sma           as __imported_lib_sma
import sugar         as __imported_lib_sugar
import unrepeated    as __imported_lib_unrepeated
import volatility    as __imported_lib_volatility
import warp          as __imported_lib_warp

def __reexports (*libs):
    d = {}
    for lib in libs:
        for name in lib.__all__:
            if name in d:
                raise Exception('libs {} and {} clash on name {}'.format(d[name],lib,name))
            d[name] = lib
            globals()[name] = getattr(lib,name)
    return [ name for name in sorted(d.keys()) ]

__all__ = __reexports( __imported_lib_conviction,
                       __imported_lib_core,
                       __imported_lib_cross,
                       __imported_lib_dump,
                       __imported_lib_ema,
                       __imported_lib_fudge,
                       __imported_lib_load,
                       __imported_lib_min_max,
                       __imported_lib_momentum,
                       __imported_lib_repeated,
                       __imported_lib_series_binop,
                       __imported_lib_series_count,
                       __imported_lib_series_filter,
                       __imported_lib_series_logic,
                       __imported_lib_series_map,
                       __imported_lib_signals,
                       __imported_lib_sma,
                       __imported_lib_sugar,
                       __imported_lib_unrepeated,
                       __imported_lib_volatility,
                       __imported_lib_warp)
