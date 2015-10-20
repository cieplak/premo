import premo
from . import TestCase


class TestEnum(TestCase):

    def test_init(self):
        directions = premo.Enum(
            'EAST',
            'WEST',
            'NORTH',
            'SOUTH',
        )
        self.assertEqual(directions.EAST, 'EAST')
        self.assertEqual(directions.WEST, 'WEST')
        self.assertEqual(directions.NORTH, 'NORTH')
        self.assertEqual(directions.SOUTH, 'SOUTH')
