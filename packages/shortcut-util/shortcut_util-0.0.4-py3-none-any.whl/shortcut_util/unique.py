#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/15
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['uuid_id', 'ts_id', 'datetime_id']

import string
import time
import uuid
import random
from datetime import datetime


def uuid_id():
    return uuid.uuid3(uuid.uuid1(), uuid.uuid4().hex).hex


def make_salt(length):
    salt = str(
        ''.join(
            random.sample(
                string.ascii_letters +
                string.digits,
                length))).upper()
    return salt


def ts_id(salt_length=6):
    ts = str(int(time.time()))
    salt = make_salt(length=salt_length)
    return f'{ts}_{salt}' if salt else ts


def datetime_id(salt_length=6, fmt='%Y%m%d%H%M%S'):
    dt = datetime.now().strftime(fmt)
    salt = make_salt(length=salt_length)
    return f'{dt}_{salt}' if salt else dt
