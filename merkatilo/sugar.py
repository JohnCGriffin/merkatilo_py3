
__all__ = [ 'lo_set_dates', 'monkey_patch_series_operators' ]

from merkatilo.load import lo
from merkatilo import series_binop
import merkatilo.core as core

def lo_set_dates(item):
    
    '''load a series, set the current_dates parameter for side-effect, 
    and finally return the series'''
    
    s = lo(item)
    core.set_dates(s)
    return s

def monkey_patch_series_operators():
    '''Opinions differ on the desirability of overloaded operators.  If you 
    believe that they are desirable, you are not alone.  Calling
    :code:`monkey_patch_series_operators()` will add the arithmetic 
    and inequality functions
    from merkatilo.series_binop into the :code:`series` class as operators 
    such that :code:`gt(IBM,200)` can be expressed as :code:`IBM>200`.
    '''
    core.series.__add__ = series_binop.add
    core.series.__sub__ = series_binop.sub
    core.series.__mul__ = series_binop.mul
    core.series.__div__ = series_binop.div
    core.series.__gt__ = series_binop.gt
    core.series.__ge__ = series_binop.ge
    core.series.__lt__ = series_binop.lt
    core.series.__le__ = series_binop.le


