#!/usr/bin/env python

from flask.ext.wtf import Form
from wtforms import TextField, IntegerField
from wtforms.validators import Required, Length
from partsdb.models import Resistor, Capacitor, IC

class PartForm(Form):
    type = TextField('Type')
    manufacturer = TextField('Manufacturer')
    manufacturer_pn = TextField('Manufacturer PN')

class ResistorForm(PartForm):
    value = IntegerField('Value')
    tolerance = IntegerField('Tolerance')
    power = IntegerField('Power (W)')
