from tokenize import Double
from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

camera = Table(
    'Camera', meta,
    Column('id', Integer, primary_key=True),
    Column('latitude', Double, nullable=False),
    Column('longitude', Double, nullable=False),
    Column('linkRTSP', String, nullable=False)
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    camera.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    camera.drop()
