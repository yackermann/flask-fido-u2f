import unittest, json

from flask import Flask, session
from flask_fido_u2f import U2F

from .soft_u2f_v2 import SoftU2FDevice

TEST_U2F_DEVICES = [
    {
        'keyHandle': '0OGIrhL98eOT4lUoqS4_ep586dC7GGGpVRyfkmEtYCbK_TORJUV9FGslZRafgxnHYLwXXNF4j2o8mhMmoDfurA', 
        'timestamp': 1468133593, 
        'publicKey': 'BPr6Kf2bH3hPvrtH4DF0Y2Kl2evIzbDu_htYi3-vfBx-F89rGhIrH_60L1l4pqqBexGRqYWZenbhXaM9O5DYMi0', 
        'counter': 0, 
        'appId': 'https://example.com'
    }
]


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

        @self.u2f.success
        def success():
            pass

        @self.u2f.fail
        def fail():
            pass

    def test_enroll(self):
        """Tests U2F enrollment"""

        self.u2f_devices = []

        # ----- Checking unauthorized enroll get ----- #
        response = self.client.get('/enroll')

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

        response = self.client.get('/enroll')

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

        response = self.client.post('/enroll', data=json.dumps(keyhandle), headers={"content-type": "application/json"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
            'error': 'Invalid key handle!', 
            'status': 'failed'
        })

        # ----- 201 CREATED ----- #

        response = self.client.get('/enroll')

        response_json = json.loads(response.get_data(as_text=True))
        
        challenge = response_json['registerRequests'][0]

        keyhandle = self.u2f_token.register(challenge, facet=self.app.config['U2F_APPID'])

        response = self.client.post('/enroll', data=json.dumps(keyhandle), headers={"content-type": "application/json"})

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
        self.u2f_devices = TEST_U2F_DEVICES
        pass

    def test_facets(self):
        """Test U2F Facets"""

        # ----- Facets disabled ----- #
        response = self.client.get('/facets.json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')


        # ----- Facets enabled ----- #
        
        self.app.config['U2F_FACETS_ENABLED'] = True
        self.app.config['U2F_FACETS_LIST']    = [
            'https://security.example.com',
            'https://example.com',
        ]

        self.u2f.init_app(self.app)

        response = self.client.get('/facets.json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/fido.trusted-apps+json')

        response_json = json.loads(response.get_data(as_text=True))

        self.assertDictEqual(response_json, {
                'trustedFacets' : [{
                    'version': { 'major': 1, 'minor' : 0 },
                    'ids': self.app.config['U2F_FACETS_LIST']
                }]
        })

        self.app.config['U2F_FACETS_ENABLED'] = True
        self.app.config['U2F_FACETS_LIST']    = [
            'https://security.example.com',
            'https://example.com',
        ]
        

    def test_key_management(self):
        self.u2f_devices = []
        pass


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

# app.config['U2F_APPID']          = 'https://localhost:5000'
# app.config['U2F_FACETS_ENABLED'] = False
# app.config['U2F_FACETS_LIST']    = ['https://localhost']