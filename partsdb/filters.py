#!/usr/bin/env python

from partsdb import app
from datetime import datetime
import math

@app.template_filter()
def friendly_time(dt, past_="ago",
    future_="from now",
    default="just now"):
    """
    Returns string representing "time since"
    or "time until" e.g.
    3 days ago, 5 hours from now etc.
    """

    now = datetime.utcnow()
    if now > dt:
        diff = now - dt
        dt_is_past = True
    else:
        diff = dt - now
        dt_is_past = False

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if period:
            return "%d %s %s" % (period, \
                singular if period == 1 else plural, \
                past_ if dt_is_past else future_)

    return default

@app.template_filter()
def to_si(d, units=''):
    inc_prefixes = ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    dec_prefixes = ['m', 'u', 'n', 'p', 'f', 'a', 'z', 'y']

    degree = int(math.floor(math.log10(math.fabs(d)) / 3))

    prefix = ''

    if degree != 0:
        ds = degree / math.fabs(degree)
        if ds == 1:
            if degree - 1 < len(inc_prefixes):
                prefix = inc_prefixes[degree - 1]
            else:
                prefix = inc_prefixes[-1]
                degree = len(inc_prefixes)

        elif ds == -1:
            if -degree - 1 < len(dec_prefixes):
                prefix = dec_prefixes[-degree - 1]
            else:
                prefix = dec_prefixes[-1]
                degree = -len(dec_prefixes)

        scaled = float(d * math.pow(1000, -degree))

        s = "{scaled}{prefix}{u}".format(scaled=scaled, prefix=prefix, u=units)

    else:
        s = "{d}{u}".format(d=d, u=units)

    return(s)

@app.template_filter()
def pretty_percent(n):
    return '{:.3%}'.format(n)
