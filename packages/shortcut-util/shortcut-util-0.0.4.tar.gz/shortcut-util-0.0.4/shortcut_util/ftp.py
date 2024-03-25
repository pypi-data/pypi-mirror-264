#!/usr/bin/env python
# -*-coding:utf-8-*-
# Email:iamfengdy@126.com
# DateTime:2021/08/30 17:24

""" FTP """
import logging
import os
from ftplib import FTP as _FTP
__version__ = '1.0'
__history__ = ''' '''
__all__ = ['FTP']

from shortcut_util import logger


class FTP:
    __slots__ = ['ftp']

    def __init__(self, ftp):
        self.ftp = ftp

    @staticmethod
    def connect(**kwargs):
        logger.info('Connect FTP. kwargs=%s.' % kwargs)
        ftp = _FTP(**kwargs)
        ftp.encoding = 'utf-8'
        ftp.set_debuglevel(0)
        return FTP(ftp)

    def close(self):
        logger.info('Close FTP.')
        if self.ftp is not None:
            self.ftp.close()
            self.ftp = None

    def list_dir(self, path):
        # TODO(fengdy): 如果文件很多会很慢
        # FIXME(fengdy): 文件名称不能包含空格
        logger.info(f'list dir. path={path}')
        infos = []
        files = []
        folders = []
        # FIXME(fengdy): 如果目录不存在会出错
        self.ftp.dir(path, infos.append)
        for info in infos:
            # info示例："drwxr-xr-x 1 ftp ftp 0 Mar 06 13:59 a"
            _, _name = info.rsplit(' ', 1)
            if _name in ('.', ):
                continue
            ff_type = info[0]
            if ff_type == 'd':
                folders.append(_name)
            else:
                files.append(_name)
        return files, folders

    def create_folder(self, path):
        logger.info(f'create folder. path={path}')
        assert os.path.isabs(path), 'must be abs path'
        folders = path.split('/')
        dir_path = '/'
        for folder in folders:
            tmp_path = os.path.join(dir_path, folder)
            if not self.exist_folder(tmp_path):
                self.ftp.cwd(dir_path)
                self.ftp.mkd(folder)
            dir_path = tmp_path

    def exist_folder(self, path):
        try:
            self.ftp.cwd(path)
            return True
        except Exception as e:
            return False

    def exist_file(self, path):
        dir_path, file_name = os.path.split(path)
        if self.exist_folder(dir_path):
            files, _ = self.list_dir(dir_path)
            return file_name in files
        return False

    def __upload_file(self, src_path, dst_path, cover=False):
        """ 上传文件（这里不创建文件夹）

        :param str src_path: 文件源路径，必须是绝对路径
        :param str dst_path: 文件目标路径，必须是绝对路径
        :param bool cover: 是否覆盖，默认False
        :return:
        """
        logger.debug(
            f'upload file. src_path={src_path}. dst_path=%{dst_path}. cover={cover}')
        self.ftp.cwd(dst_path)
        file_name = os.path.basename(src_path)
        self.ftp.storbinary('STOR {0}'.format(
            file_name), open(src_path, 'rb'))

    def __upload_folder(self, src_path, dst_path, cover=False):
        """ 上传文件夹（不上传.开头的文件即隐藏文件）

        :param str src_path: 源路径，必须为绝对路径
        :param str dst_path: 目标路径，比如为绝对路径
        :param bool cover: 是否覆盖，默认False
        """
        logger.debug(
            f'upload folder. source_path={src_path}. dst_path={dst_path}. cover={cover}')
        self.create_folder(dst_path)
        ffs = os.listdir(src_path)
        # files_or_folders
        for ff in ffs:
            if ff.startswith('.'):
                continue
            ff_path = os.path.join(src_path, ff)
            if os.path.isfile(ff_path):
                self.__upload_file(ff_path, dst_path)
            elif os.path.isdir(ff_path):
                self.__upload_folder(ff_path, os.path.join(dst_path, ff))

    def upload(self, src_path, dst_path, cover=False):
        """ 上传文件或文件夹

        :param str src_path: 源路径，必须为绝对路径，如果以”/“结尾，则上传该目录下的内容
        :param str dst_path: 目标路径，比如为绝对路径
        :param bool cover: 是否覆盖，默认False

        ::

            source_path directory structure：'/a/b/c/{1.txt,2.txt,...}'
            upload('/a/b/c', '/t/e')
                => /t/e/c/{1.txt,2.txt,...}
            upload('/a/b/c/', '/t/e')
                => /t/e/{1.txt,2.txt,...}
        """
        # FIXME(fengdy):怎样保证事务
        logger.info(
            f'upload. src_path={src_path}. dst_path={dst_path}. cover={cover}')
        assert os.path.isabs(src_path), 'Source path must be an absolute path!'
        assert os.path.isabs(dst_path), 'Target path must be an absolute path!'
        if not os.path.exists(src_path):
            return
        if src_path.endswith('/'):
            self.__upload_folder(src_path, dst_path, cover)
        else:
            # upload file or folder
            if os.path.isfile(src_path):
                self.__upload_file(src_path, dst_path, cover)
            elif os.path.isdir(src_path):
                _basename = os.path.basename(src_path)
                _dst_path = os.path.join(dst_path, _basename)
                self.__upload_folder(src_path, _dst_path, cover)
            else:
                logger.warning(
                    'Source path type is invalid. path=%s.' % src_path)

    def __download_file(self, src_path, dst_path, cover=False):
        logger.debug(
            f'download file. src_path={src_path}. dst_path={dst_path}. cover={cover}')
        dir_path, file_name = os.path.split(src_path)
        dst_file_path = os.path.join(dst_path, file_name)
        self.ftp.cwd(dir_path)
        self.ftp.retrbinary('RETR {0}'.format(
            file_name), open(dst_file_path, 'wb').write)

    def __download_folder(self, src_path, dst_path, cover=False):
        logger.debug(
            f'download folder. src_path={src_path}. dst_path={dst_path}. cover={cover}')
        os.path.makedirs(dst_path)
        files, folders = self.list_dir(src_path)
        for _file in files:
            _src_path = os.path.join(src_path, _file)
            self.__download_file(_src_path, dst_path)
        for _folder in folders:
            _src_path = os.path.join(src_path, _folder)
            _dst_path = os.path.join(dst_path, _folder)
            self.__download_folder(_src_path, _dst_path)

    def download(self, src_path, dst_path, cover=False):
        logger.debug(
            f'Download folder. src_path={src_path}. dst_path={dst_path}. cover={cover}')
        assert os.path.isabs(src_path), 'Source path must be an absolute path!'
        assert os.path.isabs(dst_path), 'Target path must be an absolute path!'
        if src_path.endswith('/'):
            self.__download_folder(src_path, dst_path, cover)
        else:
            if self.exist_file(src_path):
                self.__download_file(src_path, dst_path, cover)
            elif self.exist_folder(src_path):
                _basename = os.path.basename(src_path)
                _dst_path = os.path.join(dst_path, _basename)
                self.__download_folder(src_path, _dst_path, cover)
