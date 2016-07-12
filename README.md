flask-fido-u2f
---

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
def enroll_on_fail():
    # Executes on failed U2F enroll
    pass

@u2f.sign_on_success
def sign_on_success():
    # Executes on successful U2F authentication
    pass

@u2f.sign_on_fail
def sign_on_fail():
    # Executes on failed U2F authentication
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