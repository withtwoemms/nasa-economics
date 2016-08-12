import unittest

from core_test_mocks import core_mock_data
from core import *


class CoreTests(unittest.TestCase):

    def setUp(self):
        self.test_coordinates = core_mock_data.get('coordinates')[0:10]


if __name__ == '__main__':
    unittest.main()

