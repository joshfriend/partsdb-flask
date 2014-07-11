from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
manufacturer = Table('manufacturer', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('part_id', Integer),
    Column('name', String),
    Column('pn', String),
)

part = Table('part', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type', String(length=32), nullable=False),
    Column('manufacturer', String(length=64)),
    Column('manufacturer_pn', String(length=64)),
    Column('created', DateTime),
    Column('last_modified', DateTime),
    Column('user_id', Integer, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['manufacturer'].drop()
    post_meta.tables['part'].columns['last_modified'].create()
    post_meta.tables['part'].columns['manufacturer'].create()
    post_meta.tables['part'].columns['manufacturer_pn'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['manufacturer'].create()
    post_meta.tables['part'].columns['last_modified'].drop()
    post_meta.tables['part'].columns['manufacturer'].drop()
    post_meta.tables['part'].columns['manufacturer_pn'].drop()
