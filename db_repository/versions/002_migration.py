from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
cadence_footprint = Table('cadence_footprint', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', String(length=256)),
)

cadence_symbol = Table('cadence_symbol', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', String(length=256)),
)

footprint = Table('footprint', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('part_id', Integer),
    Column('type', Integer, nullable=False),
)

manufacturer = Table('manufacturer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('part_id', Integer),
    Column('name', String(length=64)),
    Column('pn', String(length=64)),
)

mentor_footprint = Table('mentor_footprint', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', String(length=256)),
)

mentor_symbol = Table('mentor_symbol', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', String(length=256)),
)

symbol = Table('symbol', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('part_id', Integer),
    Column('type', Integer, nullable=False),
)

vendor = Table('vendor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('part_id', Integer),
    Column('name', String(length=64)),
    Column('pn', String(length=64)),
)

part = Table('part', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type', String(length=32), nullable=False),
    Column('created', DateTime),
    Column('comments', String(length=512), default=ColumnDefault('')),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cadence_footprint'].create()
    post_meta.tables['cadence_symbol'].create()
    post_meta.tables['footprint'].create()
    post_meta.tables['manufacturer'].create()
    post_meta.tables['mentor_footprint'].create()
    post_meta.tables['mentor_symbol'].create()
    post_meta.tables['symbol'].create()
    post_meta.tables['vendor'].create()
    post_meta.tables['part'].columns['created'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['cadence_footprint'].drop()
    post_meta.tables['cadence_symbol'].drop()
    post_meta.tables['footprint'].drop()
    post_meta.tables['manufacturer'].drop()
    post_meta.tables['mentor_footprint'].drop()
    post_meta.tables['mentor_symbol'].drop()
    post_meta.tables['symbol'].drop()
    post_meta.tables['vendor'].drop()
    post_meta.tables['part'].columns['created'].drop()
