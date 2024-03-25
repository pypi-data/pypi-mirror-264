#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @File: mini_toolbox/extra.py
# @Date: 2024-03-23 22:10:49
# @Desc: 扩展工具集
""" 扩展工具集, 统一存放存在内部依赖的工具 """

__all__ = ['catch_exception', 'update_obj', 'gen_deps_seq', 'make_patch', 'dict_sort', 'format_vars', 'edit_file']

import os
import re
import sys

from functools import wraps, partial
from typing import Any, List, Tuple

from .logger import logger
from .config import json_load, json_dump
from .utils import mkdirs, gen_path, path_type, path_join, copy_file, dict2obj
from .hash import md5


def catch_exception(func=None, logger: Any = logger, exit_code: int = None) -> Any:
    """ 异常捕获装饰器 """

    if func is None:
        return partial(catch_exception, logger=logger, exit_code=exit_code)

    @wraps(func)
    def warpper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as err:
            logger.exception(err)

            if exit_code is not None:
                sys.exit(exit_code)

    return warpper


def update_obj(file: str, data: dict) -> object:
    """ 更新json数据文件, 并返回 `_Dict2Obj` 类型对象 """

    if not isinstance(data, dict):
        data = {}

    dst_data = json_load(file) if os.path.exists(file) else data

    if isinstance(dst_data, dict):
        dst_data.update(data)

    json_dump(dst_data, file)
    return dict2obj(dst_data)


def gen_deps_seq(src_deps: list) -> Tuple[List[str], bool]:
    """ 基于模块依赖关系, 生成依赖顺序和环状依赖标识
    
    Args: 
        src_deps (list): 依赖关系列表, '模块A,依赖B,依赖C', 示例: ['A,B,C', 'B,D', 'C', 'E,B']
        
    Returns: 
        Tuple[List[str], bool]: (依赖顺序, 环状依赖标识), 示例: (['C', 'B', 'A', 'E'], False)
    """

    def _split(s: str):
        _s = list(filter(None, [x.strip() for x in str(s).split(',')]))
        return _s[:1], _s[1:]

    def _join(l: list):
        return [y for x in l for y in x]

    split_deps = [_split(x) for x in src_deps]
    src_modules = _join(x[0] for x in split_deps)
    module_deep = dict((y, 1) for y in sorted(set(_join((_join(x) for x in split_deps)))))

    # 更新层级关系, 乱序遍历n遍
    for i in range(0, len(split_deps)):
        for _module, _deps in split_deps:
            if not _module or not _deps:
                continue
            for _dep in _deps:
                if module_deep[_module[0]] <= module_deep[_dep]:
                    module_deep[_module[0]] = module_deep[_dep] + 1

    # 判断是否有环状依赖
    nums = [y for x, y in module_deep.items()]
    CIRC_DEPS = True if nums and sorted(nums)[-1] != len(set(nums)) else False

    # 获得集成顺序
    dst_deps = [x[0] for x in sorted(module_deep.items(), key=lambda x: x[1])]
    dst_deps = [x for x in dst_deps if x in src_modules]  # 只取第一个模块
    return (dst_deps, CIRC_DEPS)


def make_patch(old: str, new: str, patch: str) -> None:
    """ 用于制作补丁, old/new/patch都表示文件夹路径, 其中old/new必须真实存在 """

    # 创建补丁文件夹
    mkdirs(patch, is_file=False)

    # 获取文件列表
    old_list = gen_path('.', base_dir=old)
    new_list = gen_path('.', base_dir=new)

    for item in set(old_list).union(new_list):
        src, dst = None, path_join(patch, item)
        path_old, path_new = path_join(old, item), path_join(new, item)
        type_old, type_new = path_type(path_old), path_type(path_new)

        # 文件独有
        if not type_old:
            src = path_new
        if not type_new:
            src = path_old

        # 文件类型不一致
        if type_old != type_new:
            src = path_new
        else:
            # 文件校验不一致
            if type_new == 'file' and md5(path_old) != md5(path_new):
                src = path_new
            # 链接指向不一致
            if type_new == 'link' and os.readlink(path_old) != os.readlink(path_new):
                src = path_new

        # 拷贝差异文件
        if src:
            copy_file(src, dst)


def dict_sort(data: dict, reverse: bool = False) -> dict:
    """ 返回按键值排序的字典 """

    return {k: v for k, v in sorted(data.items(), key=lambda d: d[0], reverse=reverse)}


def format_vars(data: str, var_dict: dict) -> str:
    """ 用于格式化str模版, 替换{{VARIABLE}} """

    dst = []
    for token in re.split(r'({{.*?}})', data):
        _tmp, _key = token, token[2:-2]
        if token.startswith('{{'):
            _tmp = str(var_dict[_key]) if _key in var_dict else ''
        dst.append(_tmp)
    return ''.join(dst)


def edit_file(file: str, sub_info: list, encoding: str = 'utf-8'):
    """ 按规则修改文本行, sub_info格式: [line_keyword, sub_from, sub_to] """

    line_keyword, sub_from, sub_to = sub_info
    dst_data = []

    with open(file, 'r', encoding=encoding) as fp:
        src_data = fp.readlines()

    for item in src_data:
        if line_keyword in item:
            item = re.sub(sub_from, sub_to, item)
        dst_data.append(item)

    with open(file, 'w', encoding=encoding) as fp:
        for item in dst_data:
            fp.write(item)
