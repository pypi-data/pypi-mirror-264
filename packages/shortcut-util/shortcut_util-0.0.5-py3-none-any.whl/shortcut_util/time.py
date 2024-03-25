#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Email:iamfengdy@126.com
# @DateTime:2021/07/17 15:42

""" 时间 """
__version__ = '1.0'
__history__ = ''' '''
__all__ = ['ts2str', 'str2ts']

import time
from datetime import datetime, timedelta


def ts2str(ts=None, fmt='%Y-%m-%d %H:%M:%S', utc=8):
    ts = ts or int(time.time())
    _tt = time.gmtime(ts + utc * 3600)
    return time.strftime(fmt, _tt)


def str2ts(dt_str, fmt='%Y-%m-%d %H:%M:%S'):
    tm = time.strptime(dt_str, fmt)
    ts = int(time.mktime(tm))
    return ts


def utc2local(utc_str, utc_fmt):
    local_str = datetime.strptime(utc_str, utc_fmt) + timedelta(hours=8)
    return str(local_str)
