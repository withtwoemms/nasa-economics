import mock
import unittest

from copy import deepcopy
from core_test_mocks import core_mock_data
from core import *


class CoreTests(unittest.TestCase):

    def setUp(self):
        self.worldbank_num_articles_datum_archetype = core_mock_data.get('worldbank_num_articles_datum_archetype')
        self.worldbank_article_datum_archetype = core_mock_data.get('worldbank_article_datum_archetype')
        self.worldbank_countries_datum_archetype = core_mock_data.get('worldbank_countries_datum_archetype')
        self.googlemaps_datum_archetype = core_mock_data.get('googlemaps_datum_archetype')
        self.test_coordinates = core_mock_data.get('coordinates')[0:10]
        self.formatted_coordinate = [','.join(map(str,coord)) for coord in self.test_coordinates[:1]]
        self.nasa_data = []
        nasa_datum_archetype = core_mock_data.get('nasa_datum_archetype')
        for coord in self.test_coordinates:
            nasa_datum = deepcopy(nasa_datum_archetype)
            nasa_datum['geolocation']['coordinates'] = coord
            self.nasa_data.append(nasa_datum)

#-- PRIVATE ------------------------>>>
    def _stub_response_with(self, stub):
        mock_resp = mock.Mock()
        mock_resp.json.return_value = stub
        mock_resp.status_code = 200
        return mock_resp
#----------------------------------->>>

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

    @mock.patch('core.requests.get')
    def test_get_country_data_for(self, mock_get):
        mock_get.return_value = self._stub_response_with(self.googlemaps_datum_archetype)
        self.assertCountEqual(
            get_country_data_for(self.formatted_coordinate)[0][0].keys(),
            ['place_id', 'geometry', 'formatted_address', 'address_components', 'types']
        )

    @mock.patch('core.requests.get')
    def test_get_country_names_from(self, mock_get):
        mock_get.return_value = self._stub_response_with(self.googlemaps_datum_archetype)
        country_datum = get_country_data_for(self.formatted_coordinate)
        self.assertEqual(
            get_country_names_from(country_datum),
            ['Libya']
        )

    @mock.patch('core.requests.get')
    def test_get_country_id(self, mock_get):
        mock_get.return_value = self._stub_response_with(self.worldbank_countries_datum_archetype)
        self.assertEqual(get_country_id('Libya'), 'LBY')

    @mock.patch('core.requests.get')
    def test_get_journal_article_indicator_data_for(self, mock_get):
        mock_get.return_value = self._stub_response_with(self.worldbank_article_datum_archetype)
        self.assertCountEqual(
            get_journal_article_indicator_data_for('Libya', 2008)[-1][0],
            ['value', 'decimal', 'date', 'country', 'indicator']
        )

    @mock.patch('core.requests.get')
    def test_get_journal_article_indicator_data_for_multiple(self, mock_get):
        mock_get.return_value = self._stub_response_with(self.worldbank_article_datum_archetype)
        self.assertCountEqual(
            get_journal_article_indicator_data_for_multiple(['Libya'], 2008)[0].keys(),
            ['country', 'num_articles']
        )


if __name__ == '__main__':
    unittest.main()
