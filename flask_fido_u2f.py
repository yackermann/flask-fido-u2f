from flask import current_app
from flask.views import View

class U2F():
    def __init__(self, **kwargs, enroll_route='/enroll', sign_route='/sign'):
        self.enroll_route = enroll_route
        self.sign_route   = sign_route

        current_app.add_url_rule(slef.enroll_route, view_func = self.enroll, methods=['GET', 'POST'])
        current_app.add_url_rule(slef.sign_route,   view_func = self.sign,   methods=['GET', 'POST'])

    def get_enroll(self):
        pass

    def verify_enroll(self, signature):
        pass

    def get_sign(self):
        pass

    def verify_sign(self, signature):
        pass    
    
    def enroll(self):
        pass

    def sign(self):
        pass