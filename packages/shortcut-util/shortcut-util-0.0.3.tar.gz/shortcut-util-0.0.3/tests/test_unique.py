#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/15
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []

from shortcut_util.unique import uuid_id, ts_id, datetime_id

if __name__ == '__main__':
    print(uuid_id())
    print(ts_id())
    print(datetime_id())
    print(datetime_id(fmt='%Y%m%d%H', salt_length=6))
