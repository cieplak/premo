from __future__ import unicode_literals

import subprocess
import uuid

from sqlalchemy import MetaData, TypeDecorator, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgres
from sqlalchemy.orm import scoped_session, sessionmaker


def init(config):
    global engine, Session
    engine = create_engine(config.POSTGRES['URI'])
    Metadata.bind = engine
    Session = scoped_session(sessionmaker(bind=engine))
    Model.query = Session.query_property()
    Model.Session = Session


engine = None
Session = None
Metadata = MetaData()


class ModelMixin(object):
    def __repr__(self):
        name = self.__class__.__name__
        values = ', '.join(
            '{}={}'.format(
                key, str(getattr(self, key))
            )
            for key in self.__table__.columns.keys()
        )
        repr = '{}({})'.format(name, values)
        return repr


Model = declarative_base(cls=ModelMixin)


def create(config):
    subprocess.call('psql -U postgres -c "create database premo;"', shell=True)
    subprocess.call(
        """psql  -c 'create extension "uuid-ossp";' premo postgres""",
        shell=True
    )
    init(config)
    Metadata.create_all(engine)


def drop(config):
    subprocess.call('psql -U postgres -c "drop database premo;"', shell=True)


class UUID(TypeDecorator):

    impl = postgres.UUID

    def process_bind_param(self, value, dialect=None):
        if isinstance(value, uuid.UUID):
            return str(value)
        return value

    def process_result_value(self, value, dialect=None):
        if value is not None:
            return uuid.UUID(value)
        return None
