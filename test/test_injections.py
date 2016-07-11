import unittest

from flask import Flask, session
from flask_fido_u2f import U2F

class InjectionAndConfigTest(unittest.TestCase):

    def setUp(self):
        self.app      = Flask(__name__)
        self.u2f      = U2F(self.app)

    def test_injections(self):
    # ----- Testing general fail ----- #
        with self.assertRaises(Exception) as cm:
            self.u2f.verify_integrity()

        self.assertEqual(str(cm.exception), 'U2F_APPID was not defined! Please define it in configuration file.')

    # ----- Setting U2F_APPID ----- #
        self.app.config['U2F_APPID'] = 'https://example.com'

        self.u2f.init_app(self.app)

        with self.assertRaises(Exception) as cm:
            self.u2f.verify_integrity()

        self.assertIn('handler is not defined! Please import', str(cm.exception))

   # ----- Adding new point of failure methods ----- #
        
        self.app.config['U2F_FACETS_ENABLED'] = True

        self.u2f.init_app(self.app)

        with self.assertRaises(Exception) as cm:
            self.u2f.verify_integrity()

        self.assertIn('U2F facets been enabled, but U2F facet list is empty.', str(cm.exception))

   # ----- Making empty U2F_FACETS_LIST ----- #
        self.app.config['U2F_FACETS_LIST'] = []

        self.u2f.init_app(self.app)

        with self.assertRaises(Exception) as cm:
            self.u2f.verify_integrity()

        self.assertIn('U2F facets been enabled, but U2F facet list is empty.', str(cm.exception))

    # ----- Fixing U2F_FACETS_LIST ----- #

        self.app.config['U2F_FACETS_LIST'] = [
            'https://example.com',
            'https://security.example.com',
        ]

        self.u2f.init_app(self.app)

        with self.assertRaises(Exception) as cm:
            self.u2f.verify_integrity()

        self.assertIn('handler is not defined! Please import', str(cm.exception))

    # ----- Injecting methods ----- #

        @self.u2f.read
        def read():
            pass

        @self.u2f.save
        def save():
            pass

        @self.u2f.enroll_on_success
        def enroll_on_success():
            pass

        @self.u2f.enroll_on_fail
        def enroll_on_fail():
            pass

        @self.u2f.sign_on_success
        def sign_on_success():
            pass

        @self.u2f.sign_on_fail
        def sign_on_fail():
            pass

        # All injected, should be fine now
        self.assertTrue(self.u2f.verify_integrity())

if __name__ == '__main__':
    unittest.main()