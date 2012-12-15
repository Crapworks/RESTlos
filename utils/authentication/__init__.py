#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

from flask import request, abort
from authclass import AuthClass

__all__ = ['AuthClass', 'AuthDict', 'Authentify']

# is the ldap module available
try:
    from ldapauth import AuthLDAP
except ImportError:
    pass
else:
    __all__.append('AuthLDAP')

class AuthDict(AuthClass):
    """
    AuthDict: Authenticate a user based on a simple dictionary
    """

    def __init__(self, credentials={'admin': 'password'}):
        self.credentials = credentials


class Authentify(object):
    """
    Authentify: Class decorator for flask views which are only accessible
    to authenticated users. Supports flexible authentication providers

    @config: A configuration dict, providing all informations on which
    authentication provider to use and what parameters to set

    example:
    ========

    {
        "provider": "AuthLDAP",
        "params": {
            "ldapserver": "ldap.example.com",
            "domain": "EXAMPLE.COM",
            "ssl": "TRUE",
            "groups": [ "admins", "developers" ]
        }
    }

    """

    def __init__(self, config=None):
        if not config:
            self.auth = AuthDict()
        else:
            try:
                self.auth = globals()[config['provider']](**config['params'])
            except Exception, err:
                logging.error("unable to load authentication provider %s (%s)." % (config['provider'], str(err)))
                logging.error("fallback to default dict authentication provider!")
                self.auth = AuthDict()

    def __call__(self, f):
        def wrapped_function(*args, **kwargs):
            credentials = request.authorization

            if credentials:
                if self.auth.authenticate(credentials.username, credentials.password):
                    return f(*args, **kwargs)

            abort(401)

        return wrapped_function
