#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import logging.config
import logging.handlers

from json import loads

__all__ = ['Config']

class Config(object):
    """
    Config: loads the configuration file if possible. If not: use defaults
    """

    config = {}

    def __init__(self):
        self.load()

    @classmethod
    def load(cls, cfg_file='config.json'):
        # default configuration
        cls.config.update( {
            'nagios_main_cfg': '/etc/nagios/nagios.cfg',
            'nagios_bin': '/usr/sbin/nagios',
            'output_dir': '/etc/nagios/objects/api',
            'port': 5000,
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
        } )

        try: 
            cls.config.update(loads(open(cfg_file, 'r').read()))
        except Exception, err: 
            logging.warn("unable to open config file %s: %s - using defaults" % (cfg_file, str(err)))

    @classmethod
    def get(cls, key):
        return cls.config[key]

if __name__ == '__main__':
    logging.config.dictConfig(Config()['logging'])
    logger = logging.getLogger(__name__)
    logger.warn("testing logging function")
