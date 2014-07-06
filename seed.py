#!env/bin/python

from datetime import datetime
from partsdb import db
from partsdb.models import Part, Resistor, Capacitor, IC
from partsdb.models import MentorFootprint, MentorSymbol
from partsdb.models import Vendor, Manufacturer
from partsdb.models import User
from partsdb.models import ROLE_ADMIN


u = User(name='joshfriend',
         real_name='Josh Friend',
         email='josh@fueledbycaffeine.com',
         role=ROLE_ADMIN)
db.session.add(u)
db.session.commit()

# add some footprints
resfp = MentorFootprint(name='res0603')
capfp = MentorFootprint(name='cap0603')
icfp = MentorFootprint(name='soic18')
db.session.add(resfp)
db.session.add(capfp)
db.session.add(icfp)
db.session.commit()

# add some symbols
ressym = MentorSymbol(name='res')
capsym = MentorSymbol(name='cap')
icsym = MentorSymbol(name='pic16f1823')
db.session.add(ressym)
db.session.add(capsym)
db.session.add(icsym)
db.session.commit()

p1 = Resistor(value=1000, tolerance=0.1, power=0.1, created=datetime.now())
p1.author = u
p1.vendors.append(Vendor(name='DigiKey', pn='ERJ-1000-ND'))
p1.manufacturer = Manufacturer(name='Panasonic', pn='ERJ-1000')
p1.footprints.append(resfp)
p1.symbols.append(ressym)
db.session.add(p1)
db.session.commit()

p2 = Resistor(value=1200, tolerance=0.1, power=0.1, created=datetime.now())
p2.author = u
p2.vendors.append(Vendor(name='DigiKey', pn='ERJ-1200-ND'))
p2.manufacturer = Manufacturer(name='Panasonic', pn='ERJ-1200')
p2.footprints.append(resfp)
p2.symbols.append(ressym)
db.session.add(p2)
db.session.commit()

p3 = Capacitor(value=0.000001, tolerance=0.1, voltage=20, created=datetime.now())
p3.author = u
p3.vendors.append(Vendor(name='DigiKey', pn='EKC-1000-ND'))
p3.manufacturer = Manufacturer(name='Panasonic', pn='EKC-1000')
p3.footprints.append(capfp)
p3.symbols.append(capsym)
db.session.add(p2)
db.session.commit()

p4 = IC(value='PIC16F1823', pin_count=18, created=datetime.now())
p4.author = u
p4.vendors.append(Vendor(name='DigiKey', pn='PIC16F1823-ND'))
p4.manufacturer = Manufacturer(name='Panasonic', pn='PIC16F1823')
p4.footprints.append(icfp)
p4.symbols.append(icsym)
db.session.add(p4)
db.session.commit()


