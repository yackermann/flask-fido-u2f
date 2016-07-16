import unittest, json

from flask import Flask, session
from flask_fido_u2f import U2F

from .soft_u2f_v2 import SoftU2FDevice

class APITest(unittest.TestCase):
    def setUp(self):
        self.app      = Flask(__name__)
        self.client   = self.app.test_client()
        
        self.app.config['SECRET_KEY'] = 'DjInNB3l9GBZq2D9IsbBuHpOiLI5H1iBdqJR24VPHdj'
        self.app.config['U2F_APPID']  = 'https://example.com'

        self.u2f          = U2F(self.app)
        self.u2f_devices  = []

        self.u2f_token    = SoftU2FDevice()

        @self.u2f.read
        def read():
            return self.u2f_devices

        @self.u2f.save
        def save(u2fdata):
            self.u2f_devices = u2fdata

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


    def test_enroll(self):
        """Tests U2F enrollment"""

        self.u2f_devices = []

        # ----- Checking unauthorized enroll get ----- #
        response = self.client.get(self.u2f.enroll_route)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'status' : 'failed', 
            'error'  : 'Unauthorized!'
        })


        # ----- Checking GET enroll structure ----- #
        with self.client as c:
            with c.session_transaction() as sess:
                sess['u2f_enroll_authorized'] = True

        response = self.client.get(self.u2f.enroll_route)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        response_json = json.loads(response.get_data(as_text=True))

        enroll_seed_model = {
            'status'               : str,
            'registerRequests'     : list,
            'authenticateRequests' : list
        }

        enroll_seed_model_registerRequests = {
            'appId'     : str,
            'challenge' : str,
            'version'   : str
        }

        self.assertEqual(response_json['status'], 'ok')

        self.assertTrue(all(type(response_json[key]) == enroll_seed_model[key] for key in enroll_seed_model.keys()))

        self.assertTrue(all(type(response_json['registerRequests'][0][key]) == enroll_seed_model_registerRequests[key] for key in enroll_seed_model_registerRequests.keys()))
        
        self.assertEqual(response_json['registerRequests'][0]['version'], 'U2F_V2')

    
        # ----- Verifying enroll ----- #
        # ----- 400 BAD REQUEST ----- #
        challenge = response_json['registerRequests'][0]
        keyhandle = self.u2f_token.register(challenge)

        response = self.client.post(self.u2f.enroll_route, data=json.dumps(keyhandle), headers={
            'content-type': 'application/json'
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'error': 'Invalid key handle!', 
            'status': 'failed'
        })

        # ----- 201 CREATED ----- #

        response = self.client.get(self.u2f.enroll_route)

        response_json = json.loads(response.get_data(as_text=True))
        
        challenge = response_json['registerRequests'][0]

        keyhandle = self.u2f_token.register(challenge, facet=self.app.config['U2F_APPID'])

        response = self.client.post(self.u2f.enroll_route, data=json.dumps(keyhandle), headers={
            'content-type': 'application/json'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'status'  : 'ok', 
            'message' : 'Successfully enrolled new U2F device!'
        })

        # ----- Testing U2F device format ----- #
        u2f_device = {
            'keyHandle' : str,
            'timestamp' : int,
            'publicKey' : str,
            'counter'   : int,
            'appId'     : str
        }

        self.assertTrue(all(type(self.u2f_devices[0][key]) == u2f_device[key] for key in u2f_device.keys()))


    def test_signature(self):
        """Tests U2F signature"""

        # ----- 401 Unauthorized ----- #
        response = self.client.get(self.u2f.sign_route)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'status' : 'failed', 
            'error'  : 'Unauthorized!'
        })

        # ----- Getting challenge -----#
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess['u2f_sign_required'] = True

        # ----- 404 Not found ----- #
        response = self.client.get(self.u2f.sign_route)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'status' : 'failed', 
            'error'  : 'No devices been associated with the account!'
        })

        # ----- Creating new enroll ----- #
        with self.client as c:
            with c.session_transaction() as sess:
                sess['u2f_enroll_authorized'] = True

        enroll_response = self.client.get(self.u2f.enroll_route)
        enroll_response_json = json.loads(enroll_response.get_data(as_text=True))
        
        challenge = enroll_response_json['registerRequests'][0]
        keyhandle = self.u2f_token.register(challenge, facet=self.app.config['U2F_APPID'])

        response  = self.client.post(self.u2f.enroll_route, data=json.dumps(keyhandle), headers={
            'content-type': 'application/json'
        })
        # ----- New enroll END ----- #
    
        # ----- 200 OK ----- #
        # /u2f/sign
        response = self.client.get(self.u2f.sign_route)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        response_json = json.loads(response.get_data(as_text=True))

        sign_challenge_model = {
            'status'               : str,
            'authenticateRequests' : list
        }

        sign_challenge_authenticateRequests = {
            'challenge' : str,
            'keyHandle' : str,
            'appId'     : str,
            'version'   : str
        }

        self.assertEqual(response_json['status'], 'ok')

        self.assertTrue(all(type(response_json[key]) == sign_challenge_model[key] for key in sign_challenge_model.keys()))

        self.assertTrue(all(type(response_json['authenticateRequests'][0][key]) == sign_challenge_authenticateRequests[key] for key in sign_challenge_authenticateRequests.keys()))
        
        self.assertEqual(response_json['authenticateRequests'][0]['version'], 'U2F_V2')

        # ----- Getting signature ----- #
        # Bad signature
        response = self.client.get(self.u2f.sign_route)
        response_json = json.loads(response.get_data(as_text=True))

        challenge = response_json['authenticateRequests'][0]
        signature = self.u2f_token.getAssertion(challenge)

        response = self.client.post(self.u2f.sign_route, data=json.dumps(signature), headers={
            'content-type': 'application/json'
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'error': 'Invalid signature!', 
            'status': 'failed'
        })

        # Good signature

        response      = self.client.get(self.u2f.sign_route)
        response_json = json.loads(response.get_data(as_text=True))

        # Saving old counter for checking counter value increase
        old_counter = self.u2f_devices[0]['counter']

        challenge = response_json['authenticateRequests'][0]
        signature = self.u2f_token.getAssertion(challenge, facet=self.app.config['U2F_APPID'])

        response = self.client.post(self.u2f.sign_route, data=json.dumps(signature), headers={
            'content-type': 'application/json'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        response_json = json.loads(response.get_data(as_text=True))

        self.assertTrue(set({
            'status'  : 'ok', 
            'message' : 'Successfully verified your second factor!'
        }.items()).issubset(set(response_json.items())))

        self.assertGreater(response_json['counter'], old_counter)


    def test_facets(self):
        """Test U2F Facets"""

        # ----- Facets disabled ----- #
        response = self.client.get(self.u2f.facets_route)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        # ----- Facets enabled ----- #
        
        self.app.config['U2F_FACETS_ENABLED'] = True
        self.app.config['U2F_FACETS_LIST']    = [
            'https://security.example.com',
            'https://example.com',
        ]

        self.u2f.init_app(self.app)

        response = self.client.get(self.u2f.facets_route)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/fido.trusted-apps+json')

        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
                'trustedFacets' : [{
                    'version': { 'major': 1, 'minor' : 0 },
                    'ids': self.app.config['U2F_FACETS_LIST']
                }]
        })


    def test_device_management(self):

        # ----- 401 Unauthorized ----- #
        response = self.client.get(self.u2f.devices_route)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'status' : 'failed', 
            'error'  : 'Unauthorized!'
        })

        # ----- Enabling access to device managment ----- #
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess['u2f_device_management_authorized'] = True

        # ----- No keys enrolled ----- #

        response = self.client.get(self.u2f.devices_route)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'status'  : 'ok',
            'devices' : []
        })

        # ----- Creating new enroll ----- #

        with self.client as c:
            with c.session_transaction() as sess:
                sess['u2f_enroll_authorized'] = True

        enroll_response = self.client.get(self.u2f.enroll_route)
        enroll_response_json = json.loads(enroll_response.get_data(as_text=True))
        
        challenge = enroll_response_json['registerRequests'][0]
        keyhandle = self.u2f_token.register(challenge, facet=self.app.config['U2F_APPID'])

        response  = self.client.post(self.u2f.enroll_route, data=json.dumps(keyhandle), headers={
            'content-type': 'application/json'
        })
        # ----- New enroll END ----- #

        response = self.client.get(self.u2f.devices_route)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        response_json = json.loads(response.get_data(as_text=True))

        device = response_json['devices'][0]

        device_model = {
            'id'        : str,
            'timestamp' : int
        }

        self.assertTrue(all(type(device[key]) == device_model[key] for key in device_model.keys()))

        # ----- Delete Fail----- #
        
        device_to_delete_fail = {
            'id' : 'NoExactlyValidID'
        }

        response = self.client.delete(self.u2f.devices_route, data=json.dumps(device_to_delete_fail), headers={ 'content-type': 'application/json' })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'status' : 'failed', 
            'error'  : 'No device with such an id been found!'
        })

        # ----- Delete Success----- #
        
        device_to_delete = device

        response = self.client.delete(self.u2f.devices_route, data=json.dumps(device_to_delete), headers={ 'content-type': 'application/json' })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'status'  : 'ok', 
            'message' : 'Successfully deleted your device!'
        })

        self.assertEqual([], self.u2f_devices)


    def test_has_registered_devices(self):
        self.assertFalse(self.u2f.has_registered_devices())


if __name__ == '__main__':
    unittest.main()
