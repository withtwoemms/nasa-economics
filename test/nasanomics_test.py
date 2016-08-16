import app.nasanomics as nasanomics
import unittest

from app.settings import configs


class nasanomicsAppTests(unittest.TestCase):

    def setUp(self):
        self.app = nasanomics.app.test_client()
        nasanomics.app.config['TESTING'] = True

    def test_index_route(self):
        assert self.app.get('/')._status_code == 200


if __name__ == '__main__':
    unittest.main()
