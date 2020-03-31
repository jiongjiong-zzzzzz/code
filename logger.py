# -*- coding: utf-8 -*-

# @Function : 日志记录类
# @Author   : LiPengbo
# @File     : logger.py


import logging.handlers
import os
from logging.handlers import RotatingFileHandler
import time
import io
import sys
sys.stderr = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Logger(logging.Logger):
    """
    重写的日志记录类
    """
    def __init__(self, filename=None, **kwargs):
        super(Logger, self).__init__(self)
        # 日志文件名
        if filename is None:
            filename = 'log.log'
        self.filename = filename

        # 用于写入日志文件
        fh = MyRotatingFileHandler(self.filename, maxBytes=20*1024*1024, encoding='utf-8')

        fh.setLevel(logging.DEBUG)

        # 用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [{}] [%(process)s] [%(thread)s] [%(filename)s:%(lineno)d] [{}] %(message)s'.format(
                kwargs.get('computername', ''), kwargs.get('appname', '')
            )
        )
        # fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        # self.addHandler(fh)
        self.addHandler(ch)


class MyRotatingFileHandler(RotatingFileHandler):
    """
    自定义的MyRotatingFileHandler继承自RotatingFileHandler，用于重写函数
    """
    def doRollover(self):
        """
        重写doRollover函数，可自定义重命名的文件名
        :return: 无
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        dfn = self.rotation_filename(self.new_filename())
        if os.path.exists(dfn):
            os.remove(dfn)
        self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()

    def new_filename(self):
        """
        生成重命名的新文件名
        :return: 新文件名
        """
        pos = self.baseFilename.rfind('.')
        time_str = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        if pos != -1:
            filename = self.baseFilename[:pos]
            ext = self.baseFilename[pos+1:]
            return '{}_{}.{}'.format(filename, time_str, ext)
        return '{}_{}'.format(self.baseFilename, time_str)

