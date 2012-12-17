#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ldap
import logging

class AuthLDAP(object):
    """
    AuthLDAP: Authenticate a user against a ldap server
    """

    def __init__(self, 
            ldapserver="127.0.0.1", 
            userattr="uid",
            searchattr="",
            groupattr="memberof",
            basedn="dc=example,dc=com", 
            searchdn="dc=example,dc=com", 
            ssl=True, 
            groups=[]):
        self.ldapserver = ldapserver
        self.basedn = basedn
        self.groupattr = groupattr
        self.searchdn = searchdn
        self.userattr = userattr
        self.ssl = ssl
        self.groups = groups

        if not searchattr:
            self.searchattr = self.userattr
        else:
            self.searchattr = searchattr

    def _initialize(self):
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        if self.ssl:
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

        self.ldap = ldap.initialize("%s://%s:%d" % (
            'ldaps' if self.ssl else 'ldap',
            self.ldapserver,
            636 if self.ssl else 389
        ))

    def authenticate(self, username, password):
        self._initialize()
        try:
            self.ldap.simple_bind_s("%s=%s,%s" % (self.userattr, username, self.basedn), password)
        except Exception, err:
            logging.warn(str(err))
            return False
        else:
            if not self.groups:
                return True

            try:
                result = self.ldap.search_s(self.searchdn, ldap.SCOPE_ONELEVEL, '(%s=%s)' % (self.searchattr, username), [str(self.groupattr)])
                if result[0][1][self.groupattr][0] in self.groups:
                    return True
            except:
                return False

            return False
