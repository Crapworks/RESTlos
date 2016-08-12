#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import logging.config
import logging.handlers

import handlers as restlos_handlers

from copy import deepcopy
from json import loads

__all__ = ['Config']

def dict_merge(a, b):
    if not isinstance(b, dict):
        return b

    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)

    return result

class Config(dict):
    """
    Config: loads the configuration file if possible. If not: use defaults
    """

    def __init__(self, filename='config.json'):
        self.update(self._default())
        self._load(filename)

    def _default(self):
        return {
            'nagios_main_cfg': None, # By default, try to autodetect nagios.cfg location
            'nagios_bin': '/usr/sbin/nagios',
            'sudo': False,
            'output_dir': '/etc/nagios/objects/api',
            'port': 5000,
            'host': "127.0.0.1",
            'auth': {
                'provider': 'AuthDict',
                'params': {}
            },
            'logging': {
                'version': 1,
                'formatters': {
                    'syslog': {
                        'class': 'logging.Formatter',
                        'format': 'monitoring-api[%(process)d]: <%(levelname)s> %(message)s'
                    },
                },
                'handlers': {
                    'console': {
                        'level': 'DEBUG',
                        'class':'logging.StreamHandler',
                    },
                    'syslog': {
                        'level': 'WARN',
                        'address': '/dev/log',
                        'facility': 'daemon',
                        'formatter': 'syslog',
                        'class':'logging.handlers.SysLogHandler',
                    },
                },
                'root': {
                    'level': 'DEBUG',
                    'handlers': ['console', 'syslog'],
                    'propagate': True,
                },
            },
        }

    def _load(self, cfg_file):
        try: 
            self.update(dict_merge(self, loads(open(cfg_file, 'r').read())))
        except Exception, err: 
            logging.warn("unable to open config file %s: %s - using defaults" % (cfg_file, str(err)))


if __name__ == '__main__':
    logging.config.dictConfig(Config()['logging'])
    logger = logging.getLogger(__name__)
    logger.warn("testing logging function")
