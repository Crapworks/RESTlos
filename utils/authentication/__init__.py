#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

    def __init__(self):
        self.auth = {}
        self.auth['admin'] = 'password'


class Authentify(object):
    """
    Authentify: Class decorator for flask views which are only accessible
    to authenticated users. Supports flexible authentication providers

    @provider: Authentication provider class, inheriting form AuthClass
    """

    def __init__(self, provider=AuthDict()):
        self.auth = provider

    def __call__(self, f):
        def wrapped_function(*args, **kwargs):
            credentials = request.authorization

            if credentials:
                if self.auth.authenticate(credentials.username, credentials.password):
                    return f(*args, **kwargs)

            abort(401)

        return wrapped_function
