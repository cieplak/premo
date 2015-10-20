import os
import unittest

import premo


class TestCase(unittest.TestCase):

    def setUp(self):
        premo.db.init(premo.settings)
        self.connection = premo.db.engine.connect()
        self.trans = self.connection.begin()
        premo.db.Session.remove()
        premo.db.Session.configure(bind=self.connection)
        self.session = premo.db.Session
        premo.db.ModelMixin.session = self.session

        self.app = premo.apps.web.app
        self.client = self.app.test_client()
        self.app_ctx = self.app.test_request_context()
        self.app_ctx.push()

    def tearDown(self):
        self.session.close()
        self.trans.rollback()
        self.connection.close()


def get_fixture_path(fixture_path):
    test_directory = os.path.dirname(__file__)
    return os.path.join(test_directory, 'fixtures', fixture_path)


def fixture_file_object(fixture_path):
    actual_path = get_fixture_path(fixture_path)
    return file(actual_path)
