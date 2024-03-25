#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/15
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []

import time

from shortcut_util.time import ts2str, str2ts

ts = int(time.time())

s = ts2str(ts)
print(s)
print(str2ts(s))
