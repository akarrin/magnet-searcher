# -*- coding: utf-8 -*-
# @Time    : 2019/10/17 14:27
# @Author  : Akarrin
# @Github  : https://github.com/akarrin
# @FileName: sort_magnet_result.py
# @Software: PyCharm

from app.const import *


def sort_magnet_result(magnet_result: list, sort_key: int, is_reverse: bool = True):
    if sort_key == SORTED_BY_DEFAULT:
        pass
    else:
        if sort_key == SORTED_BY_DATE:
            sort_key_as_str = 'format_create_date'
        elif sort_key == SORTED_BY_SIZE:
            sort_key_as_str = 'size_as_mb'
        elif sort_key == SORTED_BY_POPULAR:
            sort_key_as_str = 'popular'
        magnet_result.sort(key=lambda k: (k.get(sort_key_as_str)), reverse=is_reverse)
