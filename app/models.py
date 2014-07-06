from app import app, db
from hashlib import md5

MENTOR = 'mentor'
CADENCE = 'cadence'
ALLEGRO = 'allegro'

ROLE_ADMIN = 3
ROLE_MASTER = 2
ROLE_EDITOR = 1
ROLE_USER = 0

# Table holds associations between a part and a footprint
# Allows multiple parts to link to a single footprint
fp_associations = db.Table('fp_associations',
    db.Column('part_id', db.Integer, db.ForeignKey('part.id')),
    db.Column('fp_id', db.Integer, db.ForeignKey('footprint.id'))
)

# Table holds associations between a part and a symbol
# Allows multiple parts to link to a single symbol
sym_associations = db.Table('sym_associations',
    db.Column('part_id', db.Integer, db.ForeignKey('part.id')),
    db.Column('sym_id', db.Integer, db.ForeignKey('symbol.id'))
)

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    created = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)

    # Relationships
    comments = db.relationship('Comment',
                               uselist=True,
                               backref='part',
                               lazy='dynamic')
    vendors = db.relationship('Vendor',
                              uselist=True,
                              backref='part',
                              lazy='dynamic')
    manufacturer = db.relationship('Manufacturer',
                                   uselist=False,
                                   backref='part',
                                   lazy='joined')
    footprints = db.relationship('Footprint',
                                 secondary=fp_associations,
                                 backref=db.backref('parts', lazy='dynamic'),
                                 lazy='dynamic')
    symbols = db.relationship('Symbol',
                              secondary=sym_associations,
                              backref=db.backref('parts', lazy='dynamic'),
                              lazy='dynamic')

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


class Capacitor(Part):
    id = db.Column(db.Integer, db.ForeignKey('part.id'), primary_key=True)
    value = db.Column(db.Float, default=0)
    tolerance = db.Column(db.Float, default=0)
    voltage = db.Column(db.Float, default=0)
    __tablename__ = 'capacitor'
    __mapper_args__ = {'polymorphic_identity': __tablename__}


class PolarizedCapacitor(Part):
    id = db.Column(db.Integer, db.ForeignKey('part.id'), primary_key=True)
    value = db.Column(db.Float, default=0)
    tolerance = db.Column(db.Float, default=0)
    voltage = db.Column(db.Float, default=0)
    esr = db.Column(db.Float, default=0)
    ripple_current = db.Column(db.Float, default=0)
    __tablename__ = 'polarized_capacitor'
    __mapper_args__ = {'polymorphic_identity': __tablename__}


class IC(Part):
    id = db.Column(db.Integer, db.ForeignKey('part.id'), primary_key=True)
    value = db.Column(db.String(64), default='')
    pin_count = db.Column(db.Integer)
    __tablename__ = 'ic'
    __mapper_args__ = {'polymorphic_identity': __tablename__}


class Transistor(Part):
    id = db.Column(db.Integer, db.ForeignKey('part.id'), primary_key=True)
    value = db.Column(db.String(64), default='')
    pin_count = db.Column(db.Integer)
    __tablename__ = 'transistor'
    __mapper_args__ = {'polymorphic_identity': __tablename__}


class Connector(Part):
    id = db.Column(db.Integer, db.ForeignKey('part.id'), primary_key=True)
    value = db.Column(db.String(64), default='')
    pin_count = db.Column(db.Integer)
    __tablename__ = 'connector'
    __mapper_args__ = {'polymorphic_identity': __tablename__}


class Symbol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16), nullable=False)
    __mapper_args__ = {'polymorphic_on': type}

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)


class MentorSymbol(Symbol):
    id = db.Column(db.Integer, db.ForeignKey('symbol.id'), primary_key=True)
    name = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': MENTOR}


class CadenceSymbol(Symbol):
    id = db.Column(db.Integer, db.ForeignKey('symbol.id'), primary_key=True)
    name = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': CADENCE}


class AllegroSymbol(Symbol):
    id = db.Column(db.Integer, db.ForeignKey('symbol.id'), primary_key=True)
    name = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': ALLEGRO}


class Footprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16), nullable=False)
    __mapper_args__ = {'polymorphic_on': type}

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.name)


class MentorFootprint(Footprint):
    id = db.Column(db.Integer, db.ForeignKey('footprint.id'), primary_key=True)
    name = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': MENTOR}


class CadenceFootprint(Footprint):
    id = db.Column(db.Integer, db.ForeignKey('footprint.id'), primary_key=True)
    name = db.Column(db.String(256))
    __mapper_args__ = {'polymorphic_identity': CADENCE}


class AllegroFootprint(Footprint):
    id = db.Column(db.Integer, db.ForeignKey('footprint.id'), primary_key=True)
    name = db.Column(db.String(256))
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

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('part.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime)
    edited = db.Column(db.DateTime)
    text = db.Column(db.String, default='')

    def __repr__(self):
        return '<%s @ %s>' % (self.author.name, self.created.strftime('%H:%M %m/%d/%Y'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    real_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128))
    role = db.Column(db.Integer, default=ROLE_USER)

    parts = db.relationship('Part',
                            uselist=True,
                            backref='author',
                            lazy='dynamic')

    comments = db.relationship('Comment',
                               backref=db.backref('author', lazy='join'),
                               lazy='dynamic')

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    def __repr__(self):
        return '</u/%s, %i>' % (self.name, self.role)
