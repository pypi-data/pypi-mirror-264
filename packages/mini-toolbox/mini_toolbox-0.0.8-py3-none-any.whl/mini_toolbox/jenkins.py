#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @File: mini_toolbox/jenkins.py
# @Date: 2024-03-23 22:31:14
# @Desc: 用于jenkins相关操作

__all__ = ['JenkinsTools']

import time
from typing import Optional

import chardet
from jenkinsapi.jenkins import Jenkins

from .logger import logger


class JenkinsTools():
    """ 用于jenkins相关操作, 支持token
    
    Args:
        user (str): 用户名
        token (str): 用户密码, 建议使用token
        server (str): jenkins服务器地址
    """

    def __init__(self, user: str, token: str, server: str):
        self.jenkins = Jenkins(baseurl=server, username=user, password=token, timeout=10)

    def build_job(self, job_name: str, params: Optional[dict] = None, poll: int = 20, bg=False, ccu=True) -> tuple:
        """ 调用执行job, 返回任务执行的状态信息
        
        Args: 
            job_name (str): jenkins的job名称
            params (Optional[dict]): 用于参数化构建, 键值与job变量取交集生效
            poll (int): 任务状态轮询周期, 默认为20s
            bg (bool): 后台执行,直接返回, 默认为False
            ccu (bool): 执行并发构建, 默认为True
        Returns: 
            tuple: bg=False, ``(结果状态, 日志URL, 日志数据)``; bg=True, ``(job名称, 任务ID)``
        """

        build_num = self.jenkins[job_name].get_next_build_number()
        self.jenkins.build_job(job_name, params=params)

        # 是否并发构建
        if not ccu:
            while self.jenkins[job_name].is_queued_or_running():
                logger.debug('顺序执行, 5.2秒后重试')
                time.sleep(5.2)

        # 等待任务启动
        while True:
            try:
                last_number = self.jenkins[job_name].get_last_buildnumber()
                if int(last_number) >= int(build_num):
                    logger.debug('当前任务号已更新: 当前#%s 期望#%s', last_number, build_num)
                    break
                else:
                    logger.debug('当前任务号未更新, 2.5秒后重试: #%s', last_number)
                    time.sleep(2.5)
            except Exception as err:
                logger.debug('未知异常, 5.2秒后重试: %s', err)
                time.sleep(5.2)

        # 后台执行, 直接返回
        if bg:
            return (job_name, build_num)

        # 等待任务执行
        while True:
            build_status, build_url, build_log = self.get_status(job_name, build_num)

            if build_status is None:
                logger.debug('任务执行中, %s秒后重试...', poll)
                time.sleep(poll)
            else:
                return (build_status, build_url, build_log)

    def get_status(self, job_name: str, build_num: int) -> tuple:
        """ 返回任务执行的状态信息
        
        Args: 
            job_name (str): jenkins的job名称
            build_num (int): job的任务ID
        Returns: 
            tuple: ``(结果状态, 日志URL, 日志数据)``
        """
        try:
            build_task = self.jenkins[job_name].get_build(int(build_num))
        except Exception as err:
            logger.debug('任务获取失败, 返回None, 异常信息: {} {}'.format(job_name, err))
            return (None, None, None)

        build_status = build_task.get_status()
        build_url = build_task.get_build_url() + 'console'
        build_log = None

        if build_status is not None:
            build_log = build_task.get_console().encode('ISO-8859-1', errors='replace')
            encoding = chardet.detect(build_log)['encoding'] or 'utf-8'  # 自动解码失败时默认使用utf-8解码
            build_log = build_log.decode(encoding, errors='replace')

            logger.debug('任务执行状态: %s 任务地址: %s', build_status, build_url)
            logger.debug('任务执行日志: %s', build_log)

        return (build_status, build_url, build_log)

    def has_job(self, job_name: str) -> bool:
        """ 返回任务执行的状态信息
        
        Args: 
            job_name (str): jenkins的job名称
        Returns: 
            bool: 是否存在
        """

        return self.jenkins.has_job(job_name)
