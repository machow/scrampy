"""
Utility functions for time formats, etc..
"""

def has_adjacent(indx):
    """Takes list of integers, returns True if any integers are adjacent in list."""
    for ii, current in enumerate(indx):
        if ii != len(indx)-1:
            nextentry = indx[ii+1]
            if (current + 1 == nextentry) or (indx[ii] - 1 == nextentry): return True

def time2ms(time):
    """converts time to millisecond (e.g. 1:20 to the numeric 80*1000)"""
    min_sec = time.split(':')
    sec =  float(min_sec[0])*60 + float(min_sec[1])
    return int(sec*1000)

def ms2time(ms):
    """Converts milliseconds to time format (minutes:seconds)"""
    m = (ms / 60000)
    sec = ms % 60000 / 1000.
    return "%s:%s"%(m, sec)

def calc_gap_length(aud, mindist=None, TRdur=1500):
    """Return number of ms padding before next clip such that..
    (1) next clip starts on multiple of 1.5s
    (2) clips are seperated by at least mindist sec
    """
    if type(aud) == int: t_now = aud
    else: t_now = len(aud)
    currentTR = int(t_now / TRdur)
    t_next = (currentTR + 1) * TRdur
    while t_next - t_now < mindist:
        #currentTR += 1
        #t_next = (currentTR + 1) * 1500
        t_next += TRdur
    return t_next - t_now

