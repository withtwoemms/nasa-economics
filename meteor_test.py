import meteor
import unittest


class MeteorAppTests(unittest.TestCase):

    def setUp(self):
        self.app = meteor.app.test_client()
        meteor.app.config['TESTING'] = True

    def test_index_route(self):
        assert self.app.get('/')._status_code == 200


if __name__ == '__main__':
    unittest.main()
