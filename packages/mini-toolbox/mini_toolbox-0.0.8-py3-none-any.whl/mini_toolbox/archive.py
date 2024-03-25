#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @File: mini_toolbox/archive.py
# @Date: 2024-03-23 22:09:20
# @Desc: 解压缩工具, 如zip/unzip/tar
""" 解压缩工具, 如zip/unzip/tar """

__all__ = ['zip', 'unzip', 'tar', 'untar']

import os
import tarfile
import zipfile
from typing import Union, Optional

from .logger import logger
from .utils import mkdirs, is_none, gen_path


def zip(arch_name: str, path_list: Union[list, str]) -> Optional[int]:
    """ 用于压缩列表中指定的路径
    
    Warning: 
        如果路径中存在软链接, 建议使用tar命令压缩
    
    Args: 
        arch_name (str): 压缩至指定文件路径
        path_list (Union[list, str]): 压缩指定的路径, 支持文件路径或目录路径
        
    Returns: 
        Optional[int]: 返回 ``(1|2|None)``, 当arch_name或file_list为空时返回1, \
        当path_list中存在非法路径时返回2, 其它情况返回None
    """

    # 校验入参
    arch_name = arch_name.strip()
    if is_none(arch_name):
        logger.error('存在空入参: arch_name: %s', arch_name)
        return 1

    if is_none(path_list):
        logger.error('存在空入参: path_list: %s', path_list)
        return 1

    if isinstance(path_list, str):
        path_list = path_list.split()

    for path in path_list:
        if not os.path.exists(path):
            logger.error('存在非法路径: %s', path)
            return 2

    # 创建压缩包所在文件夹
    mkdirs(arch_name)

    # 压缩
    with zipfile.ZipFile(arch_name, 'w') as fp:
        for path in path_list:
            for item in gen_path(path):
                logger.debug('正在压缩: %s', item)
                fp.write(item)


def unzip(arch_name: str, to_dir: Optional[str] = None, pwd: Optional[bytes] = None) -> Optional[list]:
    """ 用于解压文件至指定的路径

    Args: 
        arch_name (str): 压缩包路径
        dst_dir (Optional[str]): 解压至指定路径, 默认为当前路径
        pwd (Optional[bytes]): 压缩包密码, 默认为未加密
    
    Returns: 
        Optional[list]: 返回 ``(None|list)``, 当arch_name为空时返回None, 其它情况返回包中文件列表
    """

    # 校验入参
    arch_name = arch_name.strip()
    if is_none(arch_name):
        logger.error('存在空入参: arch_name: %s', arch_name)
        return 1

    if is_none(to_dir):
        to_dir = '.'

    # 创建解压路径
    to_dir = mkdirs(to_dir, is_file=False)[1]

    # 解压
    file_list = []
    with zipfile.ZipFile(arch_name, 'r') as fp:
        fp.setpassword(pwd)
        for item in fp.infolist():
            logger.debug('正在解压: %s', item.filename)
            file_list.append(item.filename)
            fp.extract(item, path=to_dir)
    return file_list


def tar(arch_name: str, path_list: Union[list, str], mode: str = 'gz') -> Optional[int]:
    """ 用于压缩列表中指定的路径
    
    Args: 
        arch_name (str): 压缩至指定文件路径
        path_list (Union[list, str]): 压缩指定的路径, 支持文件路径或目录路径
        mode (str): 压缩模式, 默认为gz, 可选:(None/bz2/xz)
    
    Returns: 
        Optional[int]: 返回 ``(1|2|None)``, 当arch_name或file_list为空时返回1, \
        当path_list中存在非法路径时返回2, 其它情况返回None
    """

    # 校验入参
    arch_name = arch_name.strip()
    if is_none(arch_name):
        logger.error('存在空入参: arch_name: %s', arch_name)
        return 1

    if is_none(path_list):
        logger.error('存在空入参: path_list: %s', path_list)
        return 1

    if isinstance(path_list, str):
        path_list = path_list.split()

    for path in path_list:
        if not os.path.exists(path):
            logger.error('存在非法路径: %s', path)
            return 2

    if is_none(mode) or mode == 'None':
        mode = 'w'
    else:
        mode = 'w:' + mode.strip()

    # 创建压缩包所在文件夹
    mkdirs(arch_name)

    # 压缩
    with tarfile.open(arch_name, mode) as fp:
        for path in path_list:
            logger.debug('正在压缩: %s', path)
            fp.add(path)


def untar(arch_name: str, to_dir: Optional[str] = None, mode: Optional[str] = None) -> Optional[int]:
    """ 用于解压文件至指定的路径

    Args: 
        arch_name (str): 压缩包路径 
        to_dir (Optional[str]): 解压至指定路径, 默认为当前路径 
        mode (Optional[str]): 压缩模式, 默认为自动检测, 可选:(gz/bz2/xz)
        
    Returns: 
        Optional[int]: 返回 ``(1|None)``, 当arch_name为空时返回1
    """

    # 校验入参
    arch_name = arch_name.strip()
    if is_none(arch_name):
        logger.error('存在空入参: arch_name: %s', arch_name)
        return 1

    if is_none(to_dir):
        to_dir = '.'

    if is_none(mode) or mode == 'None':
        mode = 'r'
    else:
        mode = 'r:' + mode.strip()

    # 创建解压路径
    to_dir = mkdirs(to_dir, is_file=False)[1]

    # 解压
    with tarfile.open(arch_name, mode) as fp:
        for item in fp.getnames():
            logger.debug("正在解压: %s", item)
            fp.extract(item, path=to_dir)
