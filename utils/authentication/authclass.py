#!/usr/bin/env python
# -*- coding: UTF-8 -*-


__all__ = ['AuthClass']


class AuthClass(object):
    """
    AuthClass: prototype for differenty authentication methods
    """

    def __init__(self):
        self.credentials = {}

    def authenticate(self, username, password):
        return username in self.credentials.keys() and self.credentials[username] == password
