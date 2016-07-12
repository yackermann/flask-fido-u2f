from flask import Flask, session
from flask_fido_u2f import U2F

app = Flask(__name__)

app.config['U2F_APPID']          = 'https://localhost:5000'

# VALID SSL CERT REQUIRED
app.config['U2F_FACETS_ENABLED'] = False
app.config['U2F_FACETS_LIST']    = [
    'https://localhost:5000',
    'https://secure.localhost:5000',
    'https://subhost.localhost:5000'
]

app.config['SECRET_KEY']         = 'SessionSecretKey!ChangeME!'

u2f = U2F(app)

u2f_data = []

@app.route('/', methods=['GET'])
def index():
    session['u2f_enroll_authorized']    = True
    session['u2f_sign_required']        = True
    session['u2f_allow_key_management'] = True
    return 'SUP!'

@u2f.read
def read():
    return u2f_data

@u2f.save
def save(u2fdata):
    u2f_data = u2fdata

@u2f.enroll_on_success
def enroll_on_success():
    print('Successfully enrolled new device!')

@u2f.enroll_on_fail
def enroll_on_fail():
    print('Failed to enroll new device!')

@u2f.sign_on_success
def sign_on_success():
    print('Successfully verified user!')

@u2f.sign_on_fail
def sign_on_fail():
    print('Failed to verified user!')


context = ('domain.crt', 'domain.key')
app.run(debug=True, ssl_context=context)