from flask import render_template, flash, redirect, abort, session, url_for, request, g
from partsdb import app, db
from models import Part, User, Symbol, Footprint
from datetime import datetime
import math
import markdown
from flask import Markup

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/part/')
def parts():
    parts = Part.query
    return render_template('part_list.html', title='All Parts', parts=parts)

@app.route('/part/<int:part_id>')
def part(part_id=1):
    part = Part.query.filter_by(id=part_id).first()
    if part:
        return render_template('part.html', title= '%s%i' % (part.type, part.id), part=part)
    abort(404)

@app.route('/part/<int:part_id>/edit')
def edit_part(part_id=1):
    part = Part.query.filter_by(id=part_id).first()
    if part:
        return render_template('edit_part.html', part=part)
    abort(404)

@app.route('/part/new')
def new_part():
    return render_template('new_part.html')

## FOOTPRINTS

@app.route('/part/<int:part_id>/footprints/')
def part_footprints(part_id=1):
    footprints = Part.query.filter_by(id=part_id).first().footprints.all()
    if footprints:
        return 'part has %i footprints' % len(footprints)
    else:
        return 'part has no footprints'
    abort(404)

@app.route('/footprint/<int:id>')
def footprint(id=0):
    try:
        footprint = Footprint.query.filter_by(id=id).first()
        if footprint:
            return 'footprint %s/%s' % (footprint.__class__.__name__, footprint.name)
    except:
        pass
    abort(404)

@app.route('/footprint/<int:id>/edit')
def edit_footprint(id=0):
    try:
        footprint = Footprint.query.filter_by(id=id).first()
        if footprint:
            return 'edit footprint %s/%s' % (footprint.__class__.__name__, footprint.name)
    except:
        pass
    abort(404)

@app.route('/part/<int:part_id>/footprints/new')
def new_footprint(part_id=1):
    part = Part.query.filter_by(id=part_id).first()
    if part:
        return 'create new footprint for part #%i' % part.id
    abort(404)

## Symbols

@app.route('/part/<int:part_id>/symbols/')
def part_symbols(part_id=1):
    symbols = Part.query.filter_by(id=part_id).first().symbols.all()
    if symbols:
        return 'part has %i symbols' % len(symbols)
    else:
        return 'part has no symbols'
    abort(404)

@app.route('/symbol/<int:id>')
def symbol(id=0):
    try:
        symbol = Symbol.query.filter_by(id=id).first()
        if symbol:
            return 'symbol %s/%s' % (symbol.__class__.__name__, symbol.name)
    except:
        pass
    abort(404)

@app.route('/symbol/<int:id>/edit')
def edit_symbol(id=0):
    try:
        symbol = Symbol.query.filter_by(id=id).first()
        if symbol:
            return 'edit symbol %s/%s' % (symbol.__class__.__name__, symbol.name)
    except:
        pass
    abort(404)

@app.route('/part/<int:part_id>/symbols/new')
def new_symbol(part_id=1):
    part = Part.query.filter_by(id=part_id).first()
    if part:
        return 'create new symbol for part #%i' % part.id
    abort(404)

## Vendors

@app.route('/part/<int:part_id>/vendors/')
def part_vendors(part_id=1):
    vendors = Part.query.filter_by(id=part_id).first().vendors.all()
    if vendors:
        return 'part has %i vendors' % len(vendors)
    else:
        return 'part has no vendors'
    abort(404)

@app.route('/vendor/<int:id>')
def vendor(id=0):
    try:
        vendor = Vendor.query.filter_by(id=id).first()
        if vendor:
            return 'vendor %s %s' % (vendor.name, vendor.pn)
    except:
        pass
    abort(404)

@app.route('/vendor/<int:id>/edit')
def edit_vendor(id=1):
    try:
        vendor = Vendor.query.filter_by(id=id).first()
        if vendor:
            return 'edit vendor %s %s' % (vendor.name, vendor.pn)
    except:
        pass
    abort(404)

@app.route('/part/<int:part_id>/vendors/new')
def new_vendor(part_id=1):
    part = Part.query.filter_by(id=part_id).first()
    if part:
        return 'create new vendor for part #%i' % part.id
    abort(404)

## Manufacturer

@app.route('/part/<int:part_id>/manufacturer')
def part_manufacturer(part_id=1):
    try:
        mfg = Part.query.filter_by(id=part_id).first().manufacturer
        if mfg:
            return 'manufacturer %s %s' % (mfg.name, mfg.pn)
        else:
            return 'part has no manufacturer data'
    except:
        pass
    abort(404)

@app.route('/part/<int:part_id>/manufacturer/edit')
def part_manufacturer(part_id=1):
    try:
        mfg = Part.query.filter_by(id=part_id).first().manufacturer
        if mfg:
            return 'edit manufacturer %s %s' % (mfg.name, mfg.pn)
        else:
            return 'create manufacturer data'
    except:
        pass
    abort(404)

@app.route('/u/<username>')
def user(username):
    u = User.query.filter_by(name=username).first()
    if u:
        return render_template('user.html', user=u)
    abort(404)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

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
