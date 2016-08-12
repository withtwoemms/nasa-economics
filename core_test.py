import unittest

from core_test_mocks import core_mock_data
from core import *


class CoreTests(unittest.TestCase):

    def setUp(self):
        self.test_coordinates = core_mock_data.get('coordinates')[0:10]

    def test_format_coordinate_pair(self):
        self.assertEqual(
            format_coordinate_pair(self.test_coordinates[0]),
            '32.41275,20.74575'
        )


if __name__ == '__main__':
    unittest.main()

