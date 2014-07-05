from app import app, db

MENTOR = 1
CADENCE = 2
ALLEGRO = 3

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    created = db.Column(db.DateTime)
    comments = db.Column(db.String(512), default='')

    # Relationships
    vendors = db.relationship('Vendor', uselist=True, backref='part', lazy='dynamic')
    manufacturer = db.relationship('Manufacturer', uselist=False, backref='part')
    symbols = db.relationship('Symbol', uselist=True, backref='part', lazy='dynamic')
    footprints = db.relationship('Footprint', uselist=True, backref='part', lazy='dynamic')

    __tablename__ = 'part'
    __mapper_args__ = {'polymorphic_on': type}

    def __repr__(self):
        return '<%s-%i>' % (self.__class__.__name__, self.id)


class Resistor(Part):
    id = db.Column(db.Integer, db.ForeignKey('part.id'), primary_key=True)
    value = db.Column(db.Float, default=0)
    tolerance = db.Column(db.Float, default=0)
    power = db.Column(db.Float, default=0)
    __tablename__ = 'resistor'
    __mapper_args__ = {'polymorphic_identity': __tablename__}


class IC(Part):
    id = db.Column(db.Integer, db.ForeignKey('part.id'), primary_key=True)
    value = db.Column(db.String(64), default='')
    pin_count = db.Column(db.Integer)
    __tablename__ = 'ic'
    __mapper_args__ = {'polymorphic_identity': __tablename__}


class Symbol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'))
    type = db.Column(db.Integer, nullable=False)
    __mapper_args__ = {'polymorphic_on': type}

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.value)


class MentorSymbol(Symbol):
    id = db.Column(db.Integer, db.ForeignKey('symbol.id'), primary_key=True)
    value = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': MENTOR}


class CadenceSymbol(Symbol):
    id = db.Column(db.Integer, db.ForeignKey('symbol.id'), primary_key=True)
    value = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': CADENCE}


class AllegroSymbol(Symbol):
    id = db.Column(db.Integer, db.ForeignKey('symbol.id'), primary_key=True)
    value = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': ALLEGRO}


class Footprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'))
    type = db.Column(db.Integer, nullable=False)
    __mapper_args__ = {'polymorphic_on': type}

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.value)


class MentorFootprint(Footprint):
    id = db.Column(db.Integer, db.ForeignKey('footprint.id'), primary_key=True)
    value = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': MENTOR}


class CadenceFootprint(Footprint):
    id = db.Column(db.Integer, db.ForeignKey('footprint.id'), primary_key=True)
    value = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': CADENCE}


class AllegroFootprint(Footprint):
    id = db.Column(db.Integer, db.ForeignKey('footprint.id'), primary_key=True)
    value = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': ALLEGRO}


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'))
    name = db.Column(db.String(64))
    pn = db.Column(db.String(64))

    def __repr__(self):
        return '<%s: %s %s>' % (self.__class__.__name__, self.name, self.pn)


class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'))
    name = db.Column(db.String(64))
    pn = db.Column(db.String(64))

    def __repr__(self):
        return '<%s: %s %s>' % (self.__class__.__name__, self.name, self.pn)
