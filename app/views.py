from flask import render_template, flash, redirect, abort, session, url_for, request, g
from app import app, db
from forms import LoginForm, EditForm, PostForm, SearchForm
from models import Part
from datetime import datetime

@app.route('/')
def index():
    return 'home'

@app.route('/part/')
def parts():
    parts = Part.query
    return render_template('index.html', title='All Parts', parts=parts)

@app.route('/part/<int:part_id>')
def part(part_id=1):
    part = Part.query.filter_by(id=part_id).first()
    if part:
        return render_template('part.html', title= 'Part #%i' % part.id, part=part)
    abort(404)

@app.route('/part/<int:part_id>/edit')
def edit_part(part_id=1):
    part = Part.query.filter_by(id=part_id).first()
    if part:
        return 'edit part #%i' % part.id
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

@app.route('/part/<int:part_id>/footprints/<int:fp_num>')
def part_footprint(part_id=1, fp_num=0):
    try:
        footprint = Part.query.filter_by(id=part_id).first().footprints.all()[fp_num - 1]
        if footprint:
            return 'footprint %s/%s' % (footprint.__class__.__name__, footprint.value)
    except:
        pass
    abort(404)

@app.route('/part/<int:part_id>/footprints/<int:fp_num>/edit')
def edit_footprint(part_id=1, fp_num=0):
    try:
        footprint = Part.query.filter_by(id=part_id).first().footprints.all()[fp_num - 1]
        if footprint:
            return 'edit footprint %s/%s' % (footprint.__class__.__name__, footprint.value)
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

@app.route('/part/<int:part_id>/symbols/<int:sym_num>')
def part_symbol(part_id=1, sym_num=0):
    try:
        symbol = Part.query.filter_by(id=part_id).first().symbols.all()[sym_num - 1]
        if symbol:
            return 'symbol %s/%s' % (symbol.__class__.__name__, symbol.value)
    except:
        pass
    abort(404)

@app.route('/part/<int:part_id>/symbols/<int:sym_num>/edit')
def edit_symbol(part_id=1, sym_num=0):
    try:
        symbol = Part.query.filter_by(id=part_id).first().symbols.all()[sym_num - 1]
        if symbol:
            return 'edit symbol %s/%s' % (symbol.__class__.__name__, symbol.value)
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

@app.route('/part/<int:part_id>/vendors/<int:ven_num>')
def part_vendor(part_id=1, ven_num=0):
    try:
        vendor = Part.query.filter_by(id=part_id).first().vendors.all()[ven_num - 1]
        if vendor:
            return 'vendor %s %s' % (vendor.name, vendor.pn)
    except:
        pass
    abort(404)

@app.route('/part/<int:part_id>/vendors/<int:ven_num>/edit')
def edit_vendor(part_id=1, ven_num=0):
    try:
        vendor = Part.query.filter_by(id=part_id).first().vendors.all()[ven_num - 1]
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

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
