#!/usr/bin/python
# -*- coding:utf-8 -*-
# Email:iamfengdy@126.com
# DateTime:2023/11/15
# Tool:PyCharm

"""  """
__version__ = '0.0.1'
__history__ = """"""
__all__ = []


from shortcut_util.email import Email
host = 'smtp.126.com'
port = 25
user = 'xxx@126.com'
password = 'xxx'
to_users = 'xxxx'
cc_users = ''
subject = 'python发送邮件测试'
email_util = Email.connect(host, port, user, password)
# email = TextEmail('hello, world!')
# email = test_email_with_attachment()
# email = test_html_email()
# email = test_html_email_with_attachment()
# email_util.send(email, to_users, cc_users, subject)
