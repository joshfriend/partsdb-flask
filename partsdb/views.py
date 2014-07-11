#!/usr/bin/env python

from flask import render_template, flash, abort, url_for, request
from partsdb import app, db
from models import Part, User, Symbol, Footprint, Document, Vendor
from forms import ResistorForm

@app.route('/')
def index():
    nparts = Part.query.count()
    nfootprints = Footprint.query.count()
    nsymbols = Symbol.query.count()
    return render_template('index.html',
                           parts=nparts,
                           symbols=nsymbols,
                           footprints=nfootprints)

@app.route('/part/')
def parts():
    parts = Part.query.all()
    return render_template('part/part_list.html', title='All Parts', parts=parts)

@app.route('/part/<int:id>', methods=['GET', 'POST'])
def part(id=0):
    part = Part.query.filter_by(id=id).first()
    form = ResistorForm(request.form)
    if part:
        if form.validate_on_submit():
            flash('Part has been updated!')
        return render_template('part/part.html',
                               title='%s%i' % (part.type, part.id),
                               part=part,
                               form=form)
    abort(404)

@app.route('/part/new')
def new_part():
    return render_template('part/new_part.html')

## FOOTPRINTS

@app.route('/footprint/')
def footprints():
    footprints = Footprint.query.all()
    return render_template('footprint/list_footprints.html',
                           title='Footprints',
                           footprints=footprints)

@app.route('/footprint/<int:id>')
def footprint(id=0):
    footprint = Footprint.query.filter_by(id=id).first()
    if footprint:
        return 'footprint %s/%s' % (footprint.__class__.__name__, footprint.name)
    abort(404)

@app.route('/footprint/<int:id>/edit')
def edit_footprint(id=0):
    footprint = Footprint.query.filter_by(id=id).first()
    if footprint:
        return 'edit footprint %s/%s' % (footprint.__class__.__name__, footprint.name)
    abort(404)

@app.route('/footprint/new')
def new_footprint():
    return render_template('footprint/new_footprint.html')

@app.route('/part/<int:id>/footprints/')
def part_footprints(id=0):
    part = Part.query.filter_by(id=id).first()
    if part:
        footprints = part.footprints.all()
        render_template('footprint/list_footprints.html',
                        title='Part %i Footprints' % id,
                        footprints=footprints)
    abort(404)

## Symbols

@app.route('/symbol/')
def symbols():
    symbols = Symbol.query.all()
    return render_template('symbol/list_symbols.html',
                           title='Symbols',
                           symbols=symbols)

@app.route('/symbol/<int:id>')
def symbol(id=0):
    symbol = Symbol.query.filter_by(id=id).first()
    if symbol:
        return 'symbol %s/%s' % (symbol.__class__.__name__, symbol.name)
    abort(404)

@app.route('/symbol/<int:id>/edit')
def edit_symbol(id=0):
    symbol = Symbol.query.filter_by(id=id).first()
    if symbol:
        return 'edit symbol %s/%s' % (symbol.__class__.__name__, symbol.name)
    abort(404)

@app.route('/symbol/new')
def new_symbol():
    return render_template('symbol/new_symbol.html')

@app.route('/part/<int:id>/symbols/')
def part_symbols(id=0):
    part = Part.query.filter_by(id=id).first()
    if part:
        symbols = part.symbols.all()
        render_template('symbol/list_symbols.html',
                        title='Part %i symbols' % id,
                        symbols=symbols)
    abort(404)

## Vendors

@app.route('/vendor/')
def vendors():
    vendors = Vendor.query.all()
    return render_template('vendor/list_vendors.html',
                           title='Vendors',
                           vendors=vendors)

@app.route('/vendor/<int:id>')
def vendor(id=0):
    vendor = Vendor.query.filter_by(id=id).first()
    if vendor:
        return 'vendor %s/%s' % (vendor.__class__.__name__, vendor.name)
    abort(404)

@app.route('/vendor/<int:id>/edit')
def edit_vendor(id=0):
    vendor = Vendor.query.filter_by(id=id).first()
    if vendor:
        return 'edit vendor %s/%s' % (vendor.__class__.__name__, vendor.name)
    abort(404)

@app.route('/vendor/new')
def new_vendor():
    return render_template('vendor/new_vendor.html')

@app.route('/part/<int:id>/vendors/')
def part_vendors(id=0):
    part = Part.query.filter_by(id=id).first()
    if part:
        vendors = part.vendors.all()
        render_template('vendor/list_vendors.html',
                        title='Part %i Vendors' % id,
                        vendors=vendors)
    abort(404)

## Documents

@app.route('/document/')
def documents():
    documents = Document.query.all()
    return render_template('document/list_documents.html',
                           title='documents',
                           documents=documents)

@app.route('/document/<int:id>')
def document(id=0):
    document = Document.query.filter_by(id=id).first()
    if document:
        return 'document %s/%s' % (document.__class__.__name__, document.name)
    abort(404)

@app.route('/document/<int:id>/edit')
def edit_document(id=0):
    document = Document.query.filter_by(id=id).first()
    if document:
        return 'edit document %s/%s' % (document.__class__.__name__, document.name)
    abort(404)

@app.route('/document/new')
def new_document():
    return render_template('document/new_document.html')

@app.route('/part/<int:id>/documents/')
def part_documents(id=0):
    part = Part.query.filter_by(id=id).first()
    if part:
        documents = part.docs.all()
        render_template('document/list_vendors.html',
                        title='Part %i Vendors' % id,
                        vendors=vendors)
    abort(404)

## Users

@app.route('/u/')
@app.route('/users/')
def users():
    users = User.query
    return render_template('user/user_list.html',
                           title='Users',
                           users=users)

@app.route('/u/<username>')
def user(username):
    u = User.query.filter_by(name=username).first()
    if u:
        return render_template('user/user_profile.html',
                               title=u.real_name,
                               user=u)
    abort(404)

@app.route('/u/<username>/edit')
def edit_user(username):
    u = User.query.filter_by(name=username).first()
    if u:
        return render_template('user/edit_user.html',
                               title='Edit Profile',
                               user=u)
    abort(404)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
