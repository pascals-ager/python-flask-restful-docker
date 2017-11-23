import unittest
from . import app

class TestConfig(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_config_loading(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://postgres:vimcar@127.0.0.1:5432/vimcartest')
