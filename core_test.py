import mock
import unittest

from copy import deepcopy
from core_test_mocks import core_mock_data
from core import *


class CoreTests(unittest.TestCase):

    def setUp(self):
        self.nasa_datum_architype = core_mock_data.get('nasa_data')
        self.test_coordinates = core_mock_data.get('coordinates')[0:10]
        self.nasa_data = []
        for coord in self.test_coordinates:
            nasa_datum = deepcopy(self.nasa_datum_architype)
            nasa_datum['geolocation']['coordinates'] = coord
            self.nasa_data.append(nasa_datum)

    def test_format_coordinate_pair(self):
        self.assertEqual(
            format_coordinate_pair(self.test_coordinates[0]),
            '32.41275,20.74575'
        )

    @mock.patch('core.Socrata.get')
    def test_get_meteorite_landing_coordinates_in(self, mock_get):
        mock_get.return_value = self.nasa_data
        self.assertEqual(
            get_meteorite_landing_coordinates_in(2008),
            self.test_coordinates
        )

if __name__ == '__main__':
    unittest.main()

