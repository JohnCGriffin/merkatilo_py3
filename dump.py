
__all__ = [ 'dump' ]

import core

def dump(*seriess, first=None, last=None, dts = None):
    def format(n):
        return '{:12.4f}'.format(n)
    sfs = [ s.f for s in seriess ]
    dts = dts or core.current_dates()
    fd = (first or dts.first_date())
    ld = (last or dts.last_date())
    for dt in range(fd,ld+1):
        nums = [ f(dt) for f in sfs ]
        if sum([ (1 if n else 0) for n in nums ]):
            rounded = map(lambda n : (format(n) if n else '            '), nums)
            print("{} {}".format(core.jdate_to_text(dt), ' '.join(rounded)))
