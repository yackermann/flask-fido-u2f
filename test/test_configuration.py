import unittest

from flask_fido_u2f import U2F

class ConfigurationTest(unittest.TestCase):
    def test_config(self):
        enroll_route  = '/other/enroll'
        sign_route    = '/other/sign'
        devices_route = '/other/devices'
        facets_route  = '/other/facets.json'


        u2f = U2F(  enroll_route  = enroll_route
                  , sign_route    = sign_route
                  , devices_route = devices_route
                  , facets_route  = facets_route)

        self.assertEqual(enroll_route,  u2f.enroll_route)
        self.assertEqual(sign_route,    u2f.sign_route)
        self.assertEqual(devices_route, u2f.devices_route)
        self.assertEqual(facets_route,  u2f.facets_route)