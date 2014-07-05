from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
capacitor = Table('capacitor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', Float, default=ColumnDefault(0)),
    Column('tolerance', Float, default=ColumnDefault(0)),
    Column('voltage', Float, default=ColumnDefault(0)),
)

connector = Table('connector', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', String(length=64), default=ColumnDefault('')),
    Column('pin_count', Integer),
)

polarized_capacitor = Table('polarized_capacitor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', Float, default=ColumnDefault(0)),
    Column('tolerance', Float, default=ColumnDefault(0)),
    Column('voltage', Float, default=ColumnDefault(0)),
    Column('esr', Float, default=ColumnDefault(0)),
    Column('ripple_current', Float, default=ColumnDefault(0)),
)

transistor = Table('transistor', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', String(length=64), default=ColumnDefault('')),
    Column('pin_count', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['capacitor'].create()
    post_meta.tables['connector'].create()
    post_meta.tables['polarized_capacitor'].create()
    post_meta.tables['transistor'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['capacitor'].drop()
    post_meta.tables['connector'].drop()
    post_meta.tables['polarized_capacitor'].drop()
    post_meta.tables['transistor'].drop()
