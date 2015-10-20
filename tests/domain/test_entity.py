import uuid
import premo
from tests import TestCase


class TestEntity(TestCase):

    def test_create(self):
        entity = premo.domain.Entity()
        premo.db.Session.add(entity)
        premo.db.Session.flush()
        self.assertIsInstance(entity.id, uuid.UUID)
        premo.db.Session.commit()
