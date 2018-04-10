
__all__ = [ 'dump' ]

import merkatilo.core as core

def dump(*seriess, first=None, last=None, dts = None):
    
    '''dump takes multiple series, with optional dates constraints and
    lists them in date order.  It is only useful interactively, but in that
    case, very useful.'''
    
    def format(n):
        return '{:12.4f}'.format(n)
    sfs = [ s.f for s in seriess ]
    dts = dts or core.current_dates()
    fd = (first or dts.first_date())
    ld = (last or dts.last_date())
    for dt in range(fd,ld+1):
        nums = [ f(dt) for f in sfs ]
        if sum([ (1 if core.is_valid_num(n) else 0) for n in nums ]):
            rounded = map(lambda n : (format(n) if core.is_valid_num(n) else '            '), nums)
            print("{} {}".format(core.jdate_to_text(dt), ' '.join(rounded)))
