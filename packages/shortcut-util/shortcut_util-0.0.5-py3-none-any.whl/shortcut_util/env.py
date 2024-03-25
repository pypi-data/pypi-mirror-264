#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2024/1/2
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['read_file', 'get_or_raise']

import os


def read_file(file_path):
    """ 读取文件并设置环境变量 """
    with open(file_path, 'r', encoding='utf-8') as fd:
        for line in fd:
            if 'export' not in line:
                continue
            line = line.strip()
            if line[0] == '#':
                continue
            line = line.replace('\r', '').replace('\n', '')
            _, kv = line.split(maxsplit=1)
            key, value = kv.split('=')
            if value.startswith('$'):
                value = os.environ[value[1:]]
            if value[0] == '"':
                value = value[1:]
            if value[-1] == '"':
                value = value[:-1]
            os.environ[key] = value


def get_or_raise(key, default=None, prefix=None):
    """
    读取指定环境变量或抛出异常
    :param str key:
    :param object default: 默认值
    :param str prefix: 变量前缀，默认为None
    :return: 环境变量值
    """
    if prefix is not None:
        key = prefix + key
    if default is None:
        value = os.environ.get(key)
    else:
        value = os.environ.get(key, default)
    if value is None:
        raise RuntimeError(
            (
                'Environment variable "{}" not found, you must set this variable to run this application.'
            ).format(key)
        )
    return value
