from flask import jsonify, request, session

# U2F imports
from u2flib_server.jsapi import DeviceRegistration
from u2flib_server.u2f import (start_register, complete_register, start_authenticate, verify_authenticate)


class U2F():
    def __init__(self, app, *args, enroll_route='/enroll', sign_route='/sign'):

        self.app          = app

        self.enroll_route = enroll_route
        self.sign_route   = sign_route

        self.get_u2f_devices  = None
        self.save_u2f_devices = None
        self.call_success     = None
        self.call_fail        = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_url_rule(self.enroll_route, view_func = self.enroll, methods=['GET', 'POST'])
        app.add_url_rule(self.sign_route,   view_func = self.sign,   methods=['GET', 'POST'])

    def enroll(self):
        pass

    def sign(self):
        pass

    # ----- -----#

    def get_enroll(self):
        return self.fail()

    def verify_enroll(self, signature):
        pass

    def get_signature(self):
        pass

    def verify_signature(self, signature):
        pass    
    
    def verify_counter(self, signature):
        pass

    def read(self, func):
        self.get_u2f_devices = func

    def save(self, func):
        self.save_u2f_devices = func

    def success(self, func):
        self.call_success = func

    def fail(self, func):
        self.call_fail = func