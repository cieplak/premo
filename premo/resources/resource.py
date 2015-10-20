import uuid

from flask import Response, request
from pilo import Form
from pilo.fields import String, UUID

from premo import db, domain, mimes


class Resource(Form):

    model = domain.Entity

    id = UUID(default=None)
    value = String()


def create():
    payload = request.json
    resource = Resource(**payload)
    obj = Resource.model.create(resource)
    db.Session.commit()
    created_resource = Resource(id=obj.id, value=obj.value)
    return Response(
        status=201,
        response=mimes.Json.encode(created_resource),
        content_type=mimes.Json.content_type
    )


def get(id):
    guid = uuid.UUID(id)
    obj = Resource.model.get(guid)
    resource = Resource(id=obj.id, value=obj.value)
    return Response(
        status=200,
        response=mimes.Json.encode(resource),
        content_type=mimes.Json.content_type
    )
