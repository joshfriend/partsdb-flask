from flask import render_template, flash, redirect, abort, session, url_for, request, g
from partsdb import app, db
from models import Part, User, Symbol, Footprint
from datetime import datetime
import math

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/part/')
def parts():
    parts = Part.query.all()
    return render_template('part/part_list.html', title='All Parts', parts=parts)

@app.route('/part/<int:id>')
def part(id=1):
    part = Part.query.filter_by(id=id).first()
    if part:
        return render_template('part/part.html', title= '%s%i' % (part.type, part.id), part=part)
    abort(404)

@app.route('/part/<int:id>/edit')
def edit_part(id=1):
    part = Part.query.filter_by(id=id).first()
    if part:
        return render_template('part/edit_part.html', part=part)
    abort(404)

@app.route('/part/new')
def new_part():
    return render_template('part/new_part.html')

## FOOTPRINTS

@app.route('/part/<int:id>/footprints/')
def part_footprints(id=1):
    footprints = Part.query.filter_by(id=id).first().footprints.all()
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

@app.route('/part/<int:id>/footprints/new')
def new_footprint(id=1):
    part = Part.query.filter_by(id=id).first()
    if part:
        return 'create new footprint for part #%i' % part.id
    abort(404)

## Symbols

@app.route('/part/<int:id>/symbols/')
def part_symbols(id=1):
    symbols = Part.query.filter_by(id=id).first().symbols.all()
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

@app.route('/part/<int:id>/symbols/new')
def new_symbol(id=1):
    part = Part.query.filter_by(id=id).first()
    if part:
        return 'create new symbol for part #%i' % part.id
    abort(404)

## Vendors

@app.route('/part/<int:id>/vendors/')
def part_vendors(id=1):
    vendors = Part.query.filter_by(id=id).first().vendors.all()
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

@app.route('/part/<int:id>/vendors/new')
def new_vendor(id=1):
    part = Part.query.filter_by(id=id).first()
    if part:
        return 'create new vendor for part #%i' % part.id
    abort(404)

## Manufacturer

@app.route('/part/<int:id>/manufacturer')
def part_manufacturer(id=1):
    try:
        mfg = Part.query.filter_by(id=id).first().manufacturer
        if mfg:
            return 'manufacturer %s %s' % (mfg.name, mfg.pn)
        else:
            return 'part has no manufacturer data'
    except:
        pass
    abort(404)

@app.route('/part/<int:id>/manufacturer/edit')
def part_manufacturer(id=1):
    try:
        mfg = Part.query.filter_by(id=id).first().manufacturer
        if mfg:
            return 'edit manufacturer %s %s' % (mfg.name, mfg.pn)
        else:
            return 'create manufacturer data'
    except:
        pass
    abort(404)

@app.route('/u/')
@app.route('/users/')
def users():
    users = User.query
    return render_template('user/user_list.html', title='Users', users=users)

@app.route('/u/<username>')
def user(username):
    u = User.query.filter_by(name=username).first()
    if u:
        return render_template('user/user_profile.html', title=u.real_name, user=u)
    abort(404)

@app.route('/u/<username>/edit')
def edit_user(username):
    u = User.query.filter_by(name=username).first()
    if u:
        return render_template('user/edit_user.html', title='Edit Profile', user=u)
    abort(404)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
