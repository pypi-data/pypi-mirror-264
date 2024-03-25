#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Email:iamfengdy@126.com
# @DateTime:2021/07/17 10:57

""" 日志 """
__version__ = '1.0'
__history__ = ''' '''
__all__ = ['TimedRotatingFileHandler', 'configure_logging']

import os
import time
from stat import ST_MTIME
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler as _TimedRotatingFileHandler


class TimedRotatingFileHandler(_TimedRotatingFileHandler):

    def __init__(self, filename, **kwargs):
        _TimedRotatingFileHandler.__init__(self, filename, **kwargs)
        self._filename = filename
        self.is_first = True
        # self.rolloverAt = self.computeRollover(t)

    def shouldRollover(self, record):
        """
        增加每次执行时对日志是否需要分割的检测，需要注意日级与其他类型不同，主要是时间范围不同；
        """
        result = False
        ts = int(time.time())
        if os.path.isfile(self._filename):
            mts = os.stat(self._filename)[ST_MTIME]
        else:
            mts = ts
        _rolloverAt = self.rolloverAt - self.interval
        if self.is_first and mts < _rolloverAt:
            self.rolloverAt = _rolloverAt
            result = True
        if ts >= self.rolloverAt:
            result = True
        self.is_first = False
        return result


# 日志配置可以参考`django.utils.log`以及`logging`
DEFAULT_LOGGING_CLASS = 'utils.log.TimedRotatingFileHandler'
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {},
    'formatters': {
        'default': {
            "format": (
                "[%(asctime)s] %(pathname)s "
                "%(lineno)d %(process)d %(thread)d "
                "%(levelname)s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            "formatter": "default",
        },
        'root': {
            "class": DEFAULT_LOGGING_CLASS,
            "formatter": "default",
            "filename": "result.log",
            # "maxBytes": 1024 * 1024 * 10,
            "backupCount": 10,
        }
    },
    'loggers': {
        'root': {
            'handlers': ['root'],
            'level': 'INFO',
        },
        'console': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}


def configure_logging(logging_settings=None):
    logging_settings = logging_settings or DEFAULT_LOGGING
    logging.config.dictConfig(logging_settings)
