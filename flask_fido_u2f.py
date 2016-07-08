from flask import jsonify, request, session

# U2F imports
from u2flib_server.jsapi import DeviceRegistration
from u2flib_server.u2f import (start_register, complete_register, start_authenticate, verify_authenticate)


class U2F():
    def __init__(self, app, *args, enroll_route='/enroll', sign_route='/sign'):

        self.app              = app

        self.enroll_route     = enroll_route
        self.sign_route       = sign_route

        self.get_u2f_devices  = None
        self.save_u2f_devices = None
        self.call_success     = None
        self.call_fail        = None

        self.integrity_check  = False 

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_url_rule(self.enroll_route, view_func = self.enroll, methods=['GET', 'POST'])
        app.add_url_rule(self.sign_route,   view_func = self.sign,   methods=['GET', 'POST'])

    def verify_integrity(self):
        if not self.integrity_check:
            if not self.get_u2f_devices:
                raise Exception("""Read is not defined! Please import read through @u2f.read!""")

            if not self.save_u2f_devices:
                raise Exception("""Save is not defined! Please import read through @u2f.save!""")


            if not self.call_success:
                raise Exception("""Success is not defined! Please import read through @u2f.success!""")


            if not self.call_fail:
                raise Exception("""Fail is not defined!\n Please import read through @u2f.fail!""")

            self.integrity_check = True

    def enroll(self):
        self.verify_integrity()
        pass
    def sign(self):
        self.verify_integrity()
        pass
    # ----- -----#

    def get_enroll(self):
        pass

    def verify_enroll(self, signature):
        pass

    def get_signature(self):
        pass

    def verify_signature(self, signature):
        pass    
    
    def verify_counter(self, signature):
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
        self.get_u2f_devices = func

    def save(self, func):
        self.save_u2f_devices = func

    def success(self, func):
        self.call_success = func

    def fail(self, func):
        self.call_fail = func