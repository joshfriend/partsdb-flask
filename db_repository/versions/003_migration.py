from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
allegro_footprint = Table('allegro_footprint', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', String(length=256)),
)

allegro_symbol = Table('allegro_symbol', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('value', String(length=256)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['allegro_footprint'].create()
    post_meta.tables['allegro_symbol'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['allegro_footprint'].drop()
    post_meta.tables['allegro_symbol'].drop()
