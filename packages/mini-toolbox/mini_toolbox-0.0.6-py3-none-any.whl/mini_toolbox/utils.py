#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @File: mini_toolbox/utils.py
# @Date: 2024-03-19 10:42:12
# @Desc: 实用系统工具
""" 实用系统工具 """

__all__ = [
    'get_os', 'time_flag', 'exec_cmd', 'path_type', 'is_none', 'split_path', 'path_join', 'rm_file', 'mkdirs',
    'copy_file', 'move_file', 'gen_path', 'search_file', 'dict2obj', 'split_str', 'url_join', 'format_bool',
    'format_none', 'set_or_not', 'judge_errs', 'get_obj_value', 'chunk_str', 'comp_ver', 'time_delta', 'file_time',
    'pushd'
]

import os
import re
import sys
import json
import time
import shutil
import operator
import platform
import contextlib
import subprocess
from typing import Any, Optional, Union


def get_os() -> str:
    """ 获取操作系统类型
    
    Returns: 
        str: 操作系统类型 ``win|unix``
    """

    if platform.system().find('Windows') != -1:
        return 'win'
    else:
        return 'unix'


def time_flag() -> str:
    """ 获取当前时间的格式化输出

    Returns: 
        str: 当前时间 "%Y-%m-%d %H:%M:%S"
    """

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def exec_cmd(cmd: Union[str, list],
             shell: bool = True,
             live: bool = False,
             input: Optional[str] = None,
             timeout: Optional[int] = None,
             encoding: Optional[str] = None) -> Any:
    """ 调用系统指令, 返回指令输出, 不建议执行复杂指令

    Args: 
        cmd (Union[str, list]): 待执行指令
        shell (bool): 是否使用系统shell执行, 默认为True, 如果cmd为列表, 需要置为False
        live (bool): 是否实时输出, 默认为False, 如果为True, 则返回值中标准输出和错误输出为None
        input (Optional[str]): 指令执行时交互输入, 如 ``'keyword\\n'``, 不建议使用
        timeout (Optional[int]): 指令执行超时时间, 默认不限制, 建议使用
        encoding (Optional[str]): 输出编码, 默认根据系统判断: win(gbk)/unix(utf-8), 建议默认
    
    Returns: 
        tuple: 执行结果(状态码, 标准输出, 错误输出)
        
    Raises: 
        TimeoutExpired: 超时情况抛出异常, 中断程序
    """

    encoding = encoding or 'gbk' if get_os() == 'win' else 'utf-8'
    pipe = subprocess.PIPE

    if live:
        ps = subprocess.Popen(cmd, shell=shell, encoding=encoding, stdin=pipe, stdout=sys.stdout, stderr=sys.stderr)
    else:
        ps = subprocess.Popen(cmd, shell=shell, encoding=encoding, stdin=pipe, stdout=pipe, stderr=pipe)

    try:
        stdout, stderr = ps.communicate(input, timeout)
    except subprocess.TimeoutExpired:
        ps.kill()
        raise
    return ps.returncode, (stdout or '').strip(), (stderr or '').strip()


def path_type(path: str) -> str:
    """ 获取路径类型, 返回字符类型: link/file/dir/'' """

    _func = {
        'link': os.path.islink,
        'dir': os.path.isdir,
        'file': os.path.isfile,
    }

    for key, value in _func.items():
        if value(path) == True:
            return key
    return None


def is_none(param: Any) -> bool:
    """ 校验入参是否为空, 空返回True, 非空返回False """

    if not param:
        return True
    if isinstance(param, str):
        if not param.strip():
            return True
    if isinstance(param, list):
        if not list(filter(None, [str(x).strip() for x in param])):
            return True
    return False


def split_path(path: str) -> tuple:
    """ 拆分路径, 返回目录和文件名 """

    path = './' if path == '.' or path.strip() == '' else path
    dir, file = os.path.split(path)
    file = '' if file == '.' else file
    dir = '.' if dir == '' else dir
    return dir, file


def path_join(path: str, *args: str, sep: str = os.path.sep) -> str:
    """ 合并路径, 原版'/'开头前的参数全部丢弃改为不丢弃 """

    for rel in filter(None, args):
        rel = str(rel).lstrip('/' + sep)
        path += sep + rel
    return path


def url_join(path: str, *args: str) -> str:
    """ 合并url路径"""

    return path_join(path, *args, sep='/')


@contextlib.contextmanager
def pushd(new_dir: str) -> None:
    """ 用于pushd指定目录, 通过with语句调用, with结束后隐式popd """

    prev_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(prev_dir)


def _onerror(func, path, exc_info):
    """ 仅内部调用, shutil.rmtree 的权限异常处理, 用法: shutil.rmtree(path, onerror=onerror) """

    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


def rm_file(path: str) -> None:
    """ 删除文件路径, 仅支持处理三种文件类型: dir/file/link 
    
    Warning:
        递归删除很危险, 请慎重
    """

    file_type = path_type(path)
    if file_type in ['file', 'link']:
        os.remove(path)
    elif file_type in ['dir']:
        shutil.rmtree(path, onerror=_onerror)


def mkdirs(path: str, is_file: bool = True, mkdir: bool = True, remake: bool = False) -> tuple:
    """ 递归创建文件夹, 并返回目录路径
    
    Args: 
        path (str): 路径
        is_file (bool): 是否为文件路径, 默认为True,
        mkdir (bool): 是否创建目录, 默认True
        remake (bool): 是否重建目录, 默认False
        
    Returns: 
        tuple: 目录相对路径, 目录绝对路径
    """

    dir = os.path.dirname(path) if is_file else path
    dir = '.' if not dir else dir

    if remake:
        rm_file(path)

    if mkdir:
        os.makedirs(dir, exist_ok=True)

    return dir, os.path.abspath(dir)


def copy_file(src: str, dst: str, force: bool = True) -> None:
    """ 拷贝单文件路径, 源目路径类型需要一致, 仅支持处理三种文件类型: dir/file/link """

    # 如果存在: 强制更新或跳过
    if path_type(dst):
        if force:
            rm_file(dst)
        else:
            return

    # 拷贝文件
    mkdirs(dst, is_file=True)
    src_type = path_type(src)
    if src_type == 'link':
        linkto = os.readlink(src)
        os.symlink(linkto, dst)
    elif src_type == 'file':
        shutil.copy(src, dst)
    elif src_type == 'dir':
        shutil.copytree(src, dst)


def move_file(src: str, dst: str, force: bool = True) -> None:
    """ 移动单文件路径, 源目路径类型需要一致, 仅支持处理三种文件类型: dir/file/link """

    # 如果存在: 强制更新或跳过
    if path_type(dst):
        if force:
            rm_file(dst)
        else:
            return

    # 移动文件
    shutil.move(src, dst)


def gen_path(path: str, only_file: bool = False, base_dir: str = '.') -> list:
    """ 按序递归生成有序且唯一的子路径列表

    Args: 
        path (str): 待分析的路径
        only_file (bool): 仅返回文件路径, 默认False
        base_dir (str): 基准路径, 优先切换至该路径, 默认'.'
        
    Returns: 
        list: 返回全部的子路径列表
    """

    if path.strip() == '':
        path = '.'

    _type = path_type(path)
    if not _type:
        return []
    if _type in ['file', 'link']:
        return [path]

    dst = []
    with pushd(base_dir):
        for root, dirs, files in os.walk(path):
            if not files and not dirs:
                if not only_file:
                    dst.append(root)
            for tf in files:
                dst.append(os.path.join(root, tf))

    return dst


def search_file(path: str, regex: str) -> list:
    """ 递归搜索路径中正则匹配的文件名并返回搜索结果相对路径列表

    Args: 
        path (str): 待搜索路径
        regex (str): 正则表达式
        
    Returns: 
        list: 返回搜索结果列表
    """

    dst_list = []
    for tp in gen_path('.', only_file=True, base_dir=path):
        td, tf = split_path(tp)
        if re.match(regex, tf):
            dst_list.append(tp[2:])  # remove prefix ./ or .\

    return dst_list


class _Dict2Obj():
    """ 仅允许内部调用: dict2obj返回对象类型 """

    def __init__(self, dict_):
        self.update(dict_)

    def update(self, dict_):
        if type(dict_) == type(self):
            dict_ = dict_.__dict__
        self.__dict__.update(dict_)


def dict2obj(data: dict) -> _Dict2Obj:
    """ 将字典数据转化为对象 """

    if not isinstance(data, dict):
        data = {}

    return json.loads(json.dumps(data), object_hook=_Dict2Obj)


def split_str(s: str, sep: str = ',') -> list:
    """ 拆分字符串, 返回原序去重去空列表 """

    tmp = list(filter(None, [x.strip() for x in str(s).split(sep)] if s else []))
    return sorted(set(tmp), key=tmp.index)


def format_bool(s: str) -> bool:
    """ 将true/false字符串转化为bool类型 """

    return True if str(s).lower() == 'true' else False


def format_none(v: Any, rst: bool = None) -> Any:
    """ 格式化空数据 """

    return v if v else rst


def set_or_not(obj: object, key: str, value: Any) -> None:
    """ 如果值不为None, 则更新对象的属性值 """

    if value is not None:
        setattr(obj, key, value)


def judge_errs(*args) -> list:
    """ 用于条件判断, 返回msg列表: (condition, msg, Optional(break(bool)), """

    errs = []
    for item in args:
        if item[0]:
            errs.append(item[1])
            if item[-1] == True:
                break
    return errs


def get_obj_value(obj: object, path: str, default: Any = None) -> Any:
    """ 获取对象path的值, 如果不存在, 返回默认值 """

    try:
        for key in path.split('.'):
            obj = getattr(obj, key)
        return obj
    except:
        return default


def chunk_str(src: str, size: int, sep: str = ',') -> list:
    """ 按指定大小拆分指定分隔符的字符串

    Args: 
        src (str): 待拆分的字符串
        size (int): 子字符串大小
        sep (str): 分隔符, 默认','
        
    Returns: 
        list: 返回拆分后的字符串列表
    """

    src, dst = split_str(src, sep=sep), []
    for item in [src[x:x + size] for x in range(0, len(src), size)]:
        dst.append(sep.join([str(x) for x in item]))
    return dst


def comp_ver(ver_a: str, ver_b: str, flag: str = '<') -> bool:
    """ 用于比较标准数字版本号, 版本号可以以'Vv'开头, '.’分隔, 不支持存在字母 """

    ver_a = [int(x) for x in filter(None, ver_a.strip().lstrip('Vv').split('.'))]
    ver_b = [int(x) for x in filter(None, ver_b.strip().lstrip('Vv').split('.'))]
    flag_map = {'<': 'lt', '>': 'gt', '<=': 'le', '>=': 'ge', '!=': 'ne', '==': 'eq'}
    return getattr(operator, flag_map[flag])(ver_a, ver_b)


def time_delta(days: int, time_str: str = '', time_format: str = '%Y-%m-%d') -> str:
    """ 用于简单的日期天数加减, 支持传入指定日期 """

    _time = time.mktime(time.strptime(time_str, time_format)) if time_str else time.time()
    return time.strftime(time_format, time.localtime(_time + 60 * 60 * 24 * days))


def file_time(path: str, time_format: str = '%Y%m%d%H%M%S') -> str:
    """ 获取文件的最后修改时间戳 """

    flag = os.path.getmtime(path) if path_type(path) == 'file' else 0
    return time.strftime(time_format, time.localtime(flag))


def get_eol(file_path: str, encoding: str = 'utf-8') -> str:
    """ 获取文本文件的换行符, 默认为'\n' """

    with open(file_path, 'r', encoding=encoding, newline='') as fp:
        origin = fp.readline()
    with open(file_path, 'r', encoding=encoding) as fp:
        trans = fp.readline()
    return origin[len(trans) - 1:] if trans and (origin != trans) else '\n'
