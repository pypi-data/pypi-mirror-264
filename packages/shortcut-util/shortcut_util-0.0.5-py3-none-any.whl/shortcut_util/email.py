#!/usr/bin/env python
# -*-coding:utf-8-*-
# Email:iamfengdy@126.com
# DateTime:2021/08/30 13:33

""" Email """
import os.path
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from smtplib import SMTP
__version__ = '1.0'
__history__ = ''' '''
# __all__ = []


class TextEmail(MIMEText):
    """Plain/text"""

    def __init__(self, _text, **kwargs):
        super(TextEmail, self).__init__(_text,  _charset="utf-8", **kwargs)


# other mime type: binary（MIMEApplication）、image（MIMEImage）、audio（MIMEAudio）、（MIMENonMultipart）


class HtmlEmail(MIMEMultipart):
    def __init__(self, **kwargs):
        super(HtmlEmail, self).__init__(**kwargs)


def test_html_email():
    """Present as HTML.
    Resources in HTML are not shown in attachments.
    """
    email = HtmlEmail(_subtype='alternative')
    # add body
    _mime = MIMEText(
        '<p>html</p><p><img src="cid:image_id"></p>', 'html', 'utf-8')
    email.attach(_mime)
    # add attachment
    file_path = '../tests/test.png'
    _mime = MIMEImage(open(file_path, 'rb').read())
    _mime.add_header("Content-ID", "<image_id>")
    email.attach(_mime)
    return email


def test_html_email_with_attachment():
    """present as HTML.
    Resources in HTML are not shown in attachments.
    """
    email = HtmlEmail(_subtype='related')
    # add body
    _mime = MIMEText(
        '<p>html with attachment</p><p><img src="cid:image_id"></p>', 'html', 'utf-8')
    email.attach(_mime)
    # attachment1
    file_path = '../tests/test.png'
    _mime = MIMEImage(open(file_path, 'rb').read())
    _mime.add_header("Content-ID", "<image_id>")
    file_name = os.path.basename(file_path)
    _mime.add_header("Content-Disposition", "attachment", filename=file_name)
    email.attach(_mime)
    # attachment2
    file_path = 'cache_util.py'
    _mime = MIMEText(open(file_path, 'r').read())
    file_name = os.path.basename(file_path)
    # present the file_name as an attachment
    _mime.add_header("Content-Disposition", "attachment", filename=file_name)
    email.attach(_mime)
    return email


class EmailWithAttachment(MIMEMultipart):
    def __init__(self, **kwargs):
        super(EmailWithAttach, self).__init__(**kwargs)


def test_email_with_attachment():
    email = EmailWithAttach()
    # add body
    _mime = MIMEText('body is text.', _charset='utf-8')
    email.attach(_mime)
    # add attachment
    # select MIME types depend on attachment type
    file_path = 'cache_util.py'
    _mime = MIMEText(open(file_path, 'r').read())
    file_name = os.path.basename(file_path)
    # present the file_name as an attachment
    _mime.add_header("Content-Disposition", "attachment", filename=file_name)
    email.attach(_mime)
    return email


class Email:
    def __init__(self, smtp, from_user):
        assert isinstance(smtp, SMTP), 'Not SMTP instance!'
        self.smtp = smtp
        self.from_user = from_user
        pass

    @staticmethod
    def connect(host, port, user, password):
        smtp = SMTP()
        try:
            smtp.connect(host, port)
            smtp.login(user, password)
            return Email(smtp, user)
        except Exception as e:
            raise e

    def close(self):
        if self.smtp is not None:
            self.smtp.quit()
            self.smtp.close()
            self.smtp = None

    def send(self, email, to_users, cc_users, subject):
        assert isinstance(email, MIMEBase), 'Not MIMEBase!'

        email['From'] = self.from_user
        email['To'] = to_users
        email['Cc'] = cc_users
        email['Subject'] = subject
        self.smtp.sendmail(self.from_user, to_users, email.as_string())
