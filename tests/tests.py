import unittest
from flask_testing import TestCase
from . import app, db, create_app
import json

class TestConfig(TestCase):
    def create_app(self):        
        return app

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        pass
        
    def test_config_loading(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://postgres:vimcar@postgres_db/vimcartest')


class TestRegister(TestConfig):     
    def _test_register(self,header):
        response = self.client.post('api/signup', headers=header, follow_redirects=True)
        self.assert200(response)
        reply = response.json
        self.assertTrue("confirmation_url" in reply)
        confirm_url = reply['confirmation_url']
        return confirm_url


class TestConfirm(TestRegister):
    def _test_confirm(self,header):
        confirm_url = self._test_register(header)
        response = self.client.get(confirm_url, follow_redirects=True)
        self.assert200(response)
        reply = response.json
        self.assertTrue("confirmation_message" in reply)        
        

class TestSign(TestConfirm):
    def _test_sign(self):
        header = {
            'email': 'advith.nagappa@gmail.com',
            'password': 'password'
        }
        self._test_confirm(header)
        response = self.client.get('api/sign', headers=header, follow_redirects=True)
        self.assert200(response)
        reply = response.json
        self.assertTrue("token" in reply)
        bearer=reply['token']
        #print(bearer)
        return bearer

class TestProtected(TestSign):
    def test_service(self):
        bearer = self._test_sign()
        header = {
            'Authorization': 'Bearer '+ bearer        
        }
        response = self.client.get('api/service', headers=header, follow_redirects=True)
        self.assert200(response)

    def test_tokenlessService(self):
        bearer = 'testbearertoken'
        header = {
            'Authorization': 'Bearer '+ bearer        
        }
        response = self.client.get('api/service', headers=header, follow_redirects=True)
        self.assert401(response)

