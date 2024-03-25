#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/15
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []

import logging
from shortcut_util.log import configure_logging

configure_logging()

root_logger = logging.getLogger()
logger = logging.getLogger('console')
for i in range(3):
    # root_logger.info(i)
    logger.info(i)
