#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @File: mini_toolbox/logger.py
# @Date: 2024-03-23 22:06:11
# @Desc: 标准化日志工具

__all__ = ['Logger']

import colorlog
import logging

from logging import handlers
from typing import Any

from .utils import mkdirs


def _success(self, msg, *args, **kwargs):
    """ SUCCESS等级处理函数 """

    if self.isEnabledFor(logging.SUCCESS):
        self._log(logging.SUCCESS, msg, args, **kwargs)


class Logger():
    """ 提供标准化日志工具
    
    Warning:
        同一logger_id仅第一次初始化时生效, 后续重复初始化不再改变
        
    Example:
        >>> logger = Logger().logger
        >>> logger.info('this is info message.')
    
    Attributes:
        logger: 实例化后的日志工具
    
    Args:
        logger_id (str): logger的名称, 默认为 ``mini_toolbox``
        file_path (str): 日志文件名, 默认为 ``./all.log``
        to_file (bool): 是否写入文件, 默认为True
        to_console (bool): 是否输出至控制台, 默认为True
        color_file (bool): 文件输出为彩色, 默认为True
        color_console (bool): 控制台输出为彩色, 默认为True
        show_process (bool): 日志输出显示进程字段, 默认为False
        show_thread (bool): 日志输出显示线程字段, 默认为False
        show_module (bool): 日志输出显示模块字段, 默认为True
        level (str): 日志显示等级, 默认为 DEBUG, 可选项 ``('FATAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'SUCCESS')``
        log_size (float): 单个日志大小, 默认为10MB
        log_count (int): 日志备份数量, 默认为10个
        encode (str): 写入文件的编码, 默认为'utf-8'
    """

    def __init__(self,
                 logger_id: str = 'mini',
                 file_path: str = 'all.log',
                 to_file: bool = True,
                 to_console: bool = True,
                 color_file: bool = True,
                 color_console: bool = True,
                 show_process: bool = False,
                 show_thread: bool = False,
                 show_module: bool = True,
                 level: str = 'DEBUG',
                 log_size: float = 10.0,
                 log_count: int = 10,
                 encode: str = 'utf-8'):
        self.logger_id = logger_id
        self.file_path = file_path
        self.to_file = to_file
        self.to_console = to_console
        self.color_file = color_file
        self.color_console = color_console
        self.show_process = show_process
        self.show_thread = show_thread
        self.show_module = show_module
        self.level = level
        self.log_size = log_size
        self.log_count = log_count
        self.encode = encode

        self._add_success_level()
        self.logger = logging.getLogger(self.logger_id)
        self._set_logger()

    def _add_success_level(self):
        """ logging新增success等级 """
        logging.SUCCESS = 60
        logging.addLevelName(logging.SUCCESS, 'SUCCESS')
        logging.Logger.success = _success

    def _set_logger(self) -> Any:
        """ 初始化logger """

        logger = self.logger
        logger.setLevel(self.level)

        if len(logger.handlers) == 0:
            if self.to_file:
                file_handler = self._configure_file()
                logger.addHandler(file_handler)
                file_handler.close()
            if self.to_console:
                console_handler = self._configure_console()
                logger.addHandler(console_handler)
                console_handler.close()
        return logger

    def _configure_console(self) -> Any:
        """ 配置 console handler """

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self._get_formatter(self.color_console))
        return console_handler

    def _configure_file(self) -> Any:
        """ 配置 file handler """

        max_size = 1024 * 1024 * self.log_size  # log_size MB
        mkdirs(self.file_path)
        file_handler = handlers.RotatingFileHandler(filename=self.file_path,
                                                    maxBytes=max_size,
                                                    backupCount=self.log_count,
                                                    encoding=self.encode)
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self._get_formatter(self.color_file))
        return file_handler

    def _get_formatter(self, color: bool = False) -> Any:
        """ 配置 日志样式 """

        colors_cfg = {
            'DEBUG': 'green',
            # 'INFO': 'white',
            'WARNING': 'bold_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'red',
            'SUCCESS': 'bold_green',
        }
        log_fmt = '[%(asctime)s.%(msecs)03d] [%(name)s]{}{} [%(levelname)s] [%(filename)s:%(lineno)d]{}: %(message)s'.format(
            ' [%(processName)s]' if self.show_process else '',
            ' [%(threadName)s]' if self.show_thread else '',
            ' [%(funcName)s]' if self.show_module else '',
        )
        color_fmt = '%(log_color)s' + log_fmt
        date_fmt = "%Y-%m-%d %H:%M:%S"

        if color:
            fmt = colorlog.ColoredFormatter(fmt=color_fmt, datefmt=date_fmt, log_colors=colors_cfg)
        else:
            fmt = logging.Formatter(fmt=log_fmt, datefmt=date_fmt)
        return fmt


# 仅供内部调用, 抢占并声明id为'mini_toolbox'的logger, 以免外部引用时影响库内部日志输出
logger = Logger(logger_id='mini_toolbox', to_file=False, level='WARN').logger
