import unittest
from flask_testing import TestCase

from app import create_app
#from models.users import User
from config import TestConfig
from extensions import db

import config

class TestTestingConfig(TestCase):

    def create_app(self):
        app = create_app('TestConfig')
        return app

    def setup_db(self):
        with app.app_context():
            db.create_all()
    
    def test_config(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://postgres:vimcar@127.0.0.1:5432/vimcartest')

if __name__=='__main__':
    unittest.main()
