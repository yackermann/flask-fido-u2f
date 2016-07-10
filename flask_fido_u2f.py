import json, time

# Flask imports
from flask import jsonify, session
from flask import Response, request

# U2F imports
from u2flib_server.jsapi import DeviceRegistration
from u2flib_server.u2f import (start_register, complete_register, start_authenticate, verify_authenticate)


class U2F():
    def __init__(self, app, *args
        , enroll_route = '/enroll'
        , sign_route   = '/sign'
        , keys_route   = '/keys'
        , facets_route = '/facets.json'):

        self.app              = app

        self.enroll_route     = enroll_route
        self.sign_route       = sign_route
        self.keys_route       = keys_route
        self.facets_route     = facets_route

        self.get_u2f_devices  = None
        self.save_u2f_devices = None
        self.call_success     = None
        self.call_fail        = None

        # U2F Variables
        self.APPID            = None
        self.FACETS_ENABLED   = False
        self.FACETS_LIST      = None

        self.integrity_check  = False 

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_url_rule(self.enroll_route, view_func = self.enroll, methods=['GET', 'POST'])
        app.add_url_rule(self.sign_route,   view_func = self.sign,   methods=['GET', 'POST'])
        app.add_url_rule(self.keys_route,   view_func = self.keys,   methods=['GET', 'DELETE'])
        app.add_url_rule(self.facets_route, view_func = self.facets, methods=['GET'])

        self.APPID            = self.app.config.get('U2F_APPID', None)
        self.FACETS_ENABLED   = self.app.config.get('U2F_FACETS_ENABLED', False)
        self.FACETS_LIST      = self.app.config.get('U2F_FACETS_LIST', [])

        # Set appid to appid + /facets.json if U2F_FACETS_ENABLED
        # or U2F_APP becomes U2F_FACETS_LIST
        if self.FACETS_ENABLED:
            self.APPID += '/facets.json'
        else:
            self.FACETS_LIST = [self.APPID]


    def verify_integrity(self):
        """Verifies that all required functions been injected."""
        if not self.integrity_check:
            if not self.APPID:
                raise Exception('U2F_APPID was not defined! Please define it in configuration file.')

            if self.FACETS_ENABLED and not len(self.FACETS_LIST):
                raise Exception("""U2F facets been enabled, but U2F facet list is empty.
                                   Please either disable facets by setting U2F_FACETS_ENABLED to False.
                                   Or add facets list using, by assigning it to U2F_FACETS_LIST.
                                """)

            # Injection
            if not self.get_u2f_devices:
                raise Exception('Read is not defined! Please import read through @u2f.read!')

            if not self.save_u2f_devices:
                raise Exception('Save is not defined! Please import read through @u2f.save!')


            if not self.call_success:
                raise Exception('Success is not defined! Please import read through @u2f.success!')

            if not self.call_fail:
                raise Exception('Fail is not defined! Please import read through @u2f.fail!')

            self.integrity_check = True

        return True

# ---- ----- #
    def enroll(self):
        """Enrollment function"""
        self.verify_integrity()

        if session.get('u2f_enroll_authorized', False):
            if request.method == 'GET':
                return jsonify(self.get_enroll()), 200

            elif request.method == 'POST':
                response = self.verify_enroll(request.json)

                if response['status'] == 'ok':
                    return jsonify(response), 201
                else:
                    return jsonify(response), 400

        return jsonify({'status': 'failed', 'error': 'Unauthorized!'}), 401

    def sign(self):
        """Signature function"""
        self.verify_integrity()
        
        if session.get('u2f_sign_required', False):
            if request.method == 'GET':
                return jsonify(self.get_signature_challenge()), 200

            elif request.method == 'POST':
                pass

        return jsonify({'status': 'failed', 'error': 'Unauthorized!'}), 401


    def keys(self):
        """Manages users enrolled keys"""
        pass

    def facets(self):
        """Provides facets support. REQUIRES VALID HTTPS!!"""
        if self.FACETS_ENABLED:
            data = json.dumps({
                'trustedFacets' : [{
                    'version': { 'major': 1, 'minor' : 0 },
                    'ids': self.FACETS_LIST
                }]
            }, sort_keys=True, indent=2, separators=(',', ': '))

            mime = 'application/fido.trusted-apps+json'
            resp = Response(data, mimetype=mime)

            return resp, 200
        else:
            return jsonify({}), 404

# ----- Methods -----#

    def get_enroll(self):
        """Returns new enroll seed"""
        devices = [DeviceRegistration.wrap(device) for device in self.get_u2f_devices()]
        enroll  = start_register(self.APPID, devices)
        enroll['status'] = 'ok'

        session['_u2f_enroll_'] = enroll.json
        return enroll

    def verify_enroll(self, response):
        """Verifies and saves U2F enroll"""
        try:
            new_device, cert = complete_register(session.pop('_u2f_enroll_'), response,
                                          self.FACETS_LIST)
        except Exception as e:
            # logging.warning('%s User %s failed to provide valid signature! %s', LOG_PREFIX, user.username, str(e))
            return {'status':'failed', 'error': 'Invalid key handle!'}
        finally:
            pass
        
        # Setting new device counter to 0
        new_device['counter']   = 0
        new_device['timestamp'] = int(time.time())

        devices = self.get_u2f_devices()
        devices.append(new_device)
        
        self.save_u2f_devices(devices)

        return {'status': 'ok', 'message': 'Successfully enrolled new U2F device!'}


    def get_signature_challenge(self):
        """Returns new signature challenge"""
        devices   = [DeviceRegistration.wrap(device) for device in self.get_u2f_devices()]
        challenge = start_authenticate(devices)
        challenge['status'] = 'ok'

        session['_u2f_challenge_'] = challenge.json

        return challenge

    def verify_signature(self, signature):
        """Verifies signature"""
        pass


    def get_keys(self):
        """Returns list of enrolled U2F keys"""
        pass

    def remove_key(self, keyHandle):
        """Removes key specified by keyHandle"""
        pass

    
# ----- Utilities ----- #
    def verify_certificate(self, signature):
        """FUTURE: if enforced policy, verify certificate in public directory"""
        pass

    def verify_counter(self, signature):
        """ Verifies that counter value is greater than previous signature"""  
        devices = self.get_u2f_devices()

        for device in devices:
            # Searching for specific keyhandle
            if device['keyHandle'] == signature['keyHandle']:
                if counter > device['counter']:
                    
                    # Updating counter record
                    device['counter'] = counter
                    self.save_u2f_devices(devices)
                    
                    return True
                else:
                    return False


# ----- Injectors ----- #
    def read(self, func):
        """Injects read function that reads and returns U2F object"""
        self.get_u2f_devices = func

    def save(self, func):
        """Injects save function that takes U2F object and saves it"""
        self.save_u2f_devices = func

    def success(self, func):
        """Injects function that would be called on success"""
        self.call_success = func

    def fail(self, func):
        """Injects function that would be called on fail"""
        self.call_fail = func
