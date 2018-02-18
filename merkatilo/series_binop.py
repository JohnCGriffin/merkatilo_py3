
'''
Arithmetic operations, i.e. add, sub ,mul, and div, take two arguments.
Arguments are either series or numbers.  Numeric arguments are converted
to constant series.  The result is a one for one arithmetic operation at 
each date.

Inequalities are similar but the first argument's value at a date is 
copied to the output only if the inequality holds true.  For instance,
to create a series representing 200 period gains in the Dow Industrials
greater only where the gains exceede 15%: :code:`gt(mo(DJIA,200),0.15)`.

One aspect of Python is that it has operator overloading.  If you find
that feature agreeable, check out :code:`monkey_patch_series_operators()`.

'''
__all__ = [ 'add', 'sub', 'mul', 'div', 'lt', 'le', 'gt', 'ge' ]

import merkatilo.core as core
from merkatilo.series_map import convert
from merkatilo.private.abbreviate import abbreviate

# Arithmetic and inequality operations

def binop(opname,op):
    def binop_series_function(a,b):
        a = convert(a)
        b = convert(b)
        af = a.f
        bf = b.f
        def f(dt):
            a_val = af(dt)
            b_val = bf(dt)
            if core.is_valid_num(a_val) and core.is_valid_num(b_val):
                return op(a_val,b_val)
        name = '{}({},{})'.format(opname,abbreviate(a),abbreviate(b))
        return core.series(f,name=name)
    return binop_series_function

add = binop("add", lambda a,b: a+b)
sub = binop("sub", lambda a,b: a-b)
mul = binop("mul", lambda a,b: a*b)
div = binop("div", lambda a,b: None if (b == 0) else (a/b))

lt = binop("lt", lambda a,b: (a<b) and a)
gt = binop("gt", lambda a,b: (a>b) and a)
le = binop("le", lambda a,b: (a<=b) and a)
ge = binop("gt", lambda a,b: (a>=b) and a)

