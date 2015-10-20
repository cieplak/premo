import premo
from . import TestCase


class TestDB(TestCase):

    def test_init(self):
        premo.db.init(premo.settings)
