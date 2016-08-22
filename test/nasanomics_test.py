import json
import mock
import unittest

from app.nasanomics import *
from app.settings import configs
from core_test_mocks import core_mock_data


class NasanomicsAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        self.test_year = 2008

#-- TEST ROUTES -------------------->>>
    def test_index_route(self):
        assert self.app.get('/')._status_code == 200
#----------------------------------->>>

    def test_get_a_question(self):
        self.assertEqual(get_question(3).__class__.__name__, 'str')

    def test_get_questions(self):
        self.assertEqual(json.loads(get_question(None)).__class__.__name__, 'dict')

    @mock.patch('app.nasanomics.get_journal_article_indicator_data_for_multiple')
    @mock.patch('app.nasanomics.get_countries_with_meteorite_landings_in')
    def test_get_answer(self, mock_meteorite_countries, mock_journal_article_data):
        mock_meteorite_countries.return_value = ['Libya']
        mock_journal_article_data.return_value = core_mock_data.get('meteorite_countries_with_num_articles')
        self.assertEqual(json.loads(get_answer(self.test_year)).__class__.__name__, 'list')

    @mock.patch('app.nasanomics.get_countries_with_meteorite_landings_in')
    def test_meteorite_landings(self, mock_landings):
        mock_landings.return_value = core_mock_data.get('countries_with_meteorite_landings')
        self.assertEqual(
            json.loads(meteorite_landings(self.test_year)).__class__.__name__,
            'list'
        )


if __name__ == '__main__':
    unittest.main()
