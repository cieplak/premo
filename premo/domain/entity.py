import uuid

from sqlalchemy import Column, Table, Unicode, func

from premo import db


entities = Table(
    'entities', db.Metadata,
    Column('id', db.UUID, primary_key=True,
           server_default=func.uuid_generate_v4()),
    Column('value', Unicode),
)


class Entity(db.Model):

    __table__ = entities

    @classmethod
    def create(cls, resource):
        entity = cls(**dict(resource))
        cls.Session.add(entity)
        return entity

    @classmethod
    def get(cls, guid):
        return cls.query.get(guid)
