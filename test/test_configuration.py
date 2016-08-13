import unittest

from flask_fido_u2f import U2F

class ConfigurationTest(unittest.TestCase):
    def test_config(self):
        new_enroll_route  = '/other/enroll'
        new_sign_route    = '/other/sign'
        new_devices_route = '/other/devices'
        new_facets_route  = '/other/facets.json'


        u2f = U2F(  enroll_route  = new_enroll_route
                  , sign_route    = new_sign_route
                  , devices_route = new_devices_route
                  , facets_route  = new_facets_route)

        self.assertEqual(new_enroll_route,  u2f._U2F__enroll_route)
        self.assertEqual(new_sign_route,    u2f._U2F__sign_route)
        self.assertEqual(new_devices_route, u2f._U2F__devices_route)
        self.assertEqual(new_facets_route,  u2f._U2F__facets_route)