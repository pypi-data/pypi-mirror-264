#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2024/1/18
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = ['word2pdf']

import retry as retry


@retry(tries=3, delay=1)
def word2pdf(file_path):
    """
    https://github.com/unoconv/unoconv

    cd /tmp && wget -l https://gist.githubusercontent.com/regebro/036da022dc7d5241a0ee97efdf1458eb/raw/1bc0655423d196acd79a5d9fa60d2baada8dd534/find_uno.py && python3 find_uno.py

    apt-get install libreoffice unoconv

    如果遇到找不到的问题，通过find_uno.py查找所支持的python，然后调整unoconv(/usr/bin/unoconv)

    :param str file_path: 文件路径
    :return: str
    """
    import subprocess
    subprocess.run(['unoconv', '--format=pdf', file_path], check=True)
    # subprocess.CalledProcessError
