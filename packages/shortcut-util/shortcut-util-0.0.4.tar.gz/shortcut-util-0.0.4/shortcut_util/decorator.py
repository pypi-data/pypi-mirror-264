#!/usr/bin/env python
# -*-coding:utf-8-*-
# Email:iamfengdy@126.com
# DateTime:2021/08/30 11:33

""" 装饰器 """
__version__ = '1.0'
__history__ = ''' '''
__all__ = ['catch_exception']

from functools import wraps

from shortcut_util import logger


def catch_exception(func):
    """ 捕获异常，返回默认值（如果存在kwargs['default']）

    :param func: 方法
    :return: 返回值或默认值
    """
    @wraps(func)
    def _func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            logger.exception(exc)
            result = kwargs.get('default', None)
        finally:
            return result
    return _func
