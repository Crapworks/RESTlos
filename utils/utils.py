#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import logging.config
import logging.handlers

from json import loads

__all__ = ['config']

class Config(dict):
    """
    Config: loads the configuration file if possible. If not: use defaults
    """

    def __init__(self, cfg_file='config.json'):
        # default configuration
        self.update( {
            'nagios_main_cfg': '/etc/nagios/nagios.cfg',
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
            self.update(loads(open(cfg_file, 'r').read()))
        except Exception, err: 
            print "unable to open config file %s: %s" % (cfg_file, str(err))
            print "using defaults"

config = Config()

if __name__ == '__main__':
    logging.config.dictConfig(config['logging'])
    logger = logging.getLogger(__name__)
    logger.warn("testing logging function")

