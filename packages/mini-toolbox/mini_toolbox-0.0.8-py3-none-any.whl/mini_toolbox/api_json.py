#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @File: mini_toolbox/api_json.py
# @Date: 2024-03-23 22:07:11
# @Desc: 用于操作免认证的api获取返回json数据
""" 用于操作免认证的api获取返回json数据 """

__all__ = ['api_get', 'api_post']

import requests
from typing import Optional


def api_get(api_url: str, params: Optional[dict] = None) -> dict:
    """ 根据提交信息从免认证接口查询内容并返回json数据

    Args: 
        api_url (str): api接口地址
        params (dict): 参数字典
        
    Returns: 
        dict: 接口返回的json数据
    """

    rsp = requests.get(api_url, params)
    return rsp.json()


def api_post(api_url: str, params: Optional[dict] = None) -> dict:
    """ 根据提交信息向免认证接口提交内容并返回json数据

    Args: 
        api_url (str): api接口地址
        params (dict): 参数字典
        
    Returns: 
        dict: 返回的json数据
    """

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    rsp = requests.post(api_url, json=params, headers=headers)
    return rsp.json()
