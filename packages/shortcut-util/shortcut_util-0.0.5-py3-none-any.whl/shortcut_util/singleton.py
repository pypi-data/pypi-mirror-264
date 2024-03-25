#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Email:iamfengdy@126.com
# @DateTime:2021/07/17 15:53

""" 单例模式 """
__version__ = '1.0'
__history__ = ''' '''
__all__ = []


def singleton(func):
    instances = {}

    def _func(*args, **kwargs):
        if func not in instances:
            instances[func] = func(*args, **kwargs)
        return instances[func]
    return _func
