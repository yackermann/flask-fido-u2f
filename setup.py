"""
Flask-FIDO-U2F
-------------

This is the description for that library
"""
from setuptools import setup

setup(
    name                 = 'Flask-FIDO-U2F',
    version              = '0.1',
    url                  = 'https://github.com/herrjemand/flask-fido-u2f',
    license              = 'MIT',
    author               = 'Ackermann Yuriy',
    author_email         = 'ackermann.yuriy@gmail.com',
    description          = 'A Flask plugin that adds FIDO U2F support.',
    long_description     = __doc__,

    py_modules           = ['flask_fido_u2f'],
    zip_safe             = True,
    test_suite           = 'test',
    tests_require        = [],
    include_package_data = True,
    platforms            = 'any',
    install_requires     = [
        'Flask',
        'python-u2flib-server'
    ],
    classifiers          = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)