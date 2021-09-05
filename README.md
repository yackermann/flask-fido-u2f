**DEPRECATED** flask-fido-u2f **DEPRECATED**
---

**DEPRECATED** **DEPRECATED** **DEPRECATED** **DEPRECATED** **DEPRECATED**


PLEASE TAKE A LOOK AT [WEBAUTHN API](https://w3c.github.io/webauthn/#CreateCred-DetermineRpId)

MORE RESOURCES [WEBAUTHN-AWESOME](https://github.com/herrjemand/awesome-webauthn)


Flask plugin to simplify usage and management of U2F devices.

## Installation

`pip install flask-fido-u2f`

## Usage

```python
from flask_fido_u2f import U2F

app = Flask(__name__)
app.config['U2F_APPID']  = 'https://example.com'
app.config['SECRET_KEY'] = 'SomeVeryRandomKeySetYouMust'

u2f = U2F(app)

@u2f.read
def read():
    # Returns users U2F devices object
    pass

@u2f.save
def save(u2fdata):
    # Saves users U2F devices object
    pass

@u2f.enroll_on_success
def enroll_on_success():
    # Executes on successful U2F enroll
    pass

@u2f.enroll_on_fail
def enroll_on_fail(e):
    # Executes on U2F enroll fail
    # Takes argument e - exception raised
    pass

@u2f.sign_on_success
def sign_on_success():
    # Executes on successful U2F authentication
    pass

@u2f.sign_on_fail
def sign_on_fail(e):
    # Executes on U2F sign fail
    # Takes argument e - exception raised
    pass
```

# Development

## Install dev-dependencies 

`pip install -r dev-requirements.txt`

## Run tests

`python -m unittest discover`

## Docs

 * [API Docs](https://github.com/herrjemand/flask-fido-u2f/blob/master/docs/api.md)
 * [Configuration Docs](https://github.com/herrjemand/flask-fido-u2f/blob/master/docs/configuration.md)
 * [FIDO U2F](https://fidoalliance.org/specifications/download/)

## License

[MIT](https://github.com/herrjemand/flask-fido-u2f/blob/master/LICENSE.md) © [Yuriy Ackermann](https://jeman.de/)
