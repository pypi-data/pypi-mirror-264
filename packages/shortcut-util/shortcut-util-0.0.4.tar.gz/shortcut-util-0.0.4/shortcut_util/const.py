#!/usr/bin/env python
# -*-coding:utf-8-*-
# Email:iamfengdy@126.com
# DateTime:2021/08/30 11:08

""" 常量 """
__version__ = '1.0'
__history__ = ''' '''
__all__ = ['Const']


class Const(object):
    __slots__ = ['__upload_interval']

    def __init__(self, **kwargs):
        # 使用这种方式命令可以实例类就不能直接访问了
        self.__upload_interval = 30
        pass

    @property
    def upload_interval(self):
        return self.__upload_interval

    @upload_interval.setter
    def upload_interval(self, value):
        # TODO: valid
        self.__upload_interval = value

    @upload_interval.deleter
    def upload_interval(self):
        del self.__upload_interval
