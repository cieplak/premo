import json

import flask

import premo
from tests import TestCase


class TestResource(TestCase):

    def test_resource(self):
        post_response = self.client.post(
            flask.url_for('resource.create'),
            data=json.dumps(dict(value='binary blob')),
            content_type=premo.mimes.Json.content_type
        )
        self.assertEqual(post_response.status_code, 201)
        body = json.loads(post_response.data)

        # Validate schema
        premo.resources.resource.Resource(**body)

        get_response = self.client.get(
            flask.url_for('resource.read', id=body['id'])
        )
        self.assertEqual(get_response.status_code, 200)
        body = json.loads(get_response.data)

        # Validate schema
        premo.resources.resource.Resource(**body)
