#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @File: mini_toolbox/dingtalk.py
# @Date: 2024-03-23 22:22:09
# @Desc: 用于钉钉群消息通知

__all__ = ['DingTalk']

import hmac
import json
import time
from base64 import b64encode
from hashlib import sha256
from typing import Optional, Union

import requests

from .logger import logger


class DingTalk():
    """ 用于钉钉群消息通知, 仅支持text模式, 详见 `钉钉官方文档`_
    
    Args: 
        token (str): Webhook中的access_token
        secret (Optional[str]): 加签模式的密钥, 可选, 默认为关键字模式
        user_dict (Optional[dict]): 导入 ``{'用户名':'手机号'}`` 键值对, 用于在at_users中直接选择用户名
        ding_url (str): 钉钉官方api接口的url前缀(不含token)或者公司私用接口
        
    .. _钉钉官方文档:
        https://open.dingtalk.com/document/group/custom-robot-access
    """

    def __init__(self,
                 token: str,
                 secret: Optional[str] = None,
                 user_dict: Optional[dict] = None,
                 ding_url: str = 'https://oapi.dingtalk.com/robot/send?access_token='):
        self.token = token or ''
        self.secret = secret or ''
        self.user_dict = user_dict or {}
        self.ding_url = ding_url

        self.headers = {
            'Content-Type': 'application/json',
            'Charset': 'UTF-8',
        }

    def _gen_sign(self, secret: Optional[str]) -> str:
        """" 生成钉钉签名, 实现详见 `官方签名文档`_
        
        Args:
            secret (Optional[str]): 加签模式的密钥, 可选, 默认为关键字模式
        
        Returns:
            str: 返回加签的url字符串
        
        .. _官方签名文档:
            https://open.dingtalk.com/document/group/customize-robot-security-settings
        """

        if not secret:
            return ''

        timestamp = str(round(time.time() * 1000))
        sign = '{}\n{}'.format(timestamp, secret)
        b_sign = sign.encode('utf-8')
        b_secret = secret.encode('utf-8')
        sign = b64encode(hmac.new(b_secret, b_sign, digestmod=sha256).digest()).decode('utf-8')

        return '&timestamp={}&sign={}'.format(timestamp, sign)

    def _trans_users(self, users: Union[list, str] = []):
        """  仅内部调用, 转换用户至手机号列表 """

        dst_users = []
        if isinstance(users, str):
            users = users.split()

        for user in users:
            if user in self.user_dict:
                dst_users.append(self.user_dict[user])
            else:
                dst_users.append(user)
        return dst_users

    def send(self, content: Optional[str] = None, at_users: Union[list, str] = [], at_all: bool = False) -> dict:
        """ 发送钉钉消息
        
        Args: 
            content (Optional[str]): 消息正文, 默认为 ``'None'``, 支持 ``\\n\\t`` 等扩展字符
            at_users (Union[list, str]): 用于@指定人员, 填写手机号, str会自动 ``split()``\
            为列表, 可以配合user_dict使用
            at_all (bool): 是否@所有人, 默认为False
            
        Returns: 
            dict: 返回api的响应体信息, 如: {'errcode': 0, 'errmsg': 'ok'}
        """

        url = self.ding_url + self.token + self._gen_sign(self.secret)
        payload = {
            "msgtype": "text",
            "text": {
                "content": str(content)
            },
            "at": {
                "atMobiles": self._trans_users(at_users),
                "isAtAll": at_all,
            },
        }

        rst = requests.post(url, headers=self.headers, json=payload)
        rst_code = rst.status_code
        rst_content = json.loads(rst.content.decode('utf-8'))

        logger.debug('url: {}, headers: {}, payload: {}'.format(url, self.headers, payload))
        logger.debug('rst_code: {}, content: {}'.format(rst_code, rst_content))
        return rst_content
