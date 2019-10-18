# -*- coding:utf-8 -*-
import re
import arrow
from arrow.locales import ChineseCNLocale
from app.exceptions.error import FormatError


def get_original_magnet(cook_magnet: str):
    """
    把爬取到的未经处理的magnet字符串转化为格式化的原始magnet字符串
    :param cook_magnet: 获取到的magnet字符串
    :return: 格式化的原始magnet字符串
    """
    if 'magnet:?xt=urn:btih:' in cook_magnet:
        is_find_magnet = re.search(r'magnet:\?xt=urn:btih:\w{40}|magnet:\?xt=urn:btih:\w{32}', cook_magnet)
    else:
        is_find_magnet = re.search(r'\w{40}|\w{32}', cook_magnet)
    if is_find_magnet:
        original_magnet = is_find_magnet.group()
        if 'magnet:?xt=urn:btih:' not in original_magnet:
            original_magnet = 'magnet:?xt=urn:btih:' + original_magnet
        return original_magnet
    else:
        raise FormatError('can not format magnet string when getting original magnet.')


def format_size(cook_size: str) -> (str, float):
    """
    把爬取到的未经处理的size字符串转化为格式化的形式，并转化为mb以供后续比较大小
    :param cook_size: 爬取到的未经处理的size字符串
    :return: 格式化的size形式, 数值MB
    """
    size_info = re.sub(u'[\u4e00-\u9fa5]|\s', '', cook_size)
    is_find_size = re.search(r'(\d+\.*\d*)(\w*)', size_info)
    if is_find_size:
        size_num, size_capacity = is_find_size.groups()
        if size_num:
            if size_capacity.lower() in ['m', 'mb']:
                size_as_mb = float(size_num)
            elif size_capacity.lower() in ['g', 'gb']:
                size_as_mb = float(size_num) * 1024
            else:
                raise FormatError('capacity unit not in m, mb, g, gb when formatting size capacity.')
        else:
            raise FormatError('regex pattern not getting num when formatting size.')
    else:
        raise FormatError('regex pattern return nothing when formatting size.')
    return size_info, size_as_mb


def format_date(cook_date: str):
    """
     把爬取到的未经处理的date字符串转化为可读性更高的字符串，并转化为格式化日期以供后续比较大小
    :param cook_date: 爬取到的未经处理的日期字符串
    :return: 可读性更高的日期字符串，格式化的日期
    """
    is_find_format_date = re.search(r'(\d{4})\D*(\d{1,2})*\D*(\d*)', cook_date)
    if is_find_format_date:
        useful_date = list(filter(None, list(is_find_format_date.groups())))
        date_format_shape = "-".join(useful_date)
        if len(useful_date) == 1:
            local_time = arrow.get(date_format_shape, "YYYY")
        elif len(useful_date) == 2:
            local_time = arrow.get(date_format_shape, "YYYY-M")
        else:
            local_time = arrow.get(date_format_shape, "YYYY-M-D")
    else:
        is_find_date_info = re.search(r'(\d+\.*\d*)(\D+)', cook_date)
        if is_find_date_info:
            date_num, date_unit = is_find_date_info.groups()
            is_find_date_unit = re.search(
                r'(秒|刚|现|now|sec|s)|(分|min|m)|(时|hour|h)|(天|day)|(星期|周|week)|(月|mon)|(年|year)',
                date_unit.lower())
            if is_find_date_unit:
                date_units = is_find_date_unit.groups()
                sec, minute, hour, day, week, month, year = [float(date_num) if date_unit else 0 for date_unit in
                                                             date_units]
                local_time = arrow.now().shift(seconds=-sec, minutes=-minute, hours=-hour, days=-day, weeks=-week,
                                               months=-month, years=-year)
            else:
                raise FormatError('can not find date unit when formatting date info.')
        else:
            raise FormatError('regex pattern not getting date info when formatting date.')
    utc_time = local_time.to('utc')
    local_time_as_str = local_time.format("YYYY-MM-DD HH:mm:ss")

    # 因为arrow包0.15.2版本中文适配问题,需要在locales.py中第797行增加week、weeks的key和值，否则周会报错
    ChineseCNLocale.timeframes.setdefault('week', '1周')
    ChineseCNLocale.timeframes.setdefault('weeks', '{0}周')
    human_readable_date = utc_time.humanize(locale='zh')
    return human_readable_date, local_time_as_str


def format_popular(cook_popular_index: str):
    is_find_popular = re.search(r'\d+', cook_popular_index)
    if is_find_popular:
        return is_find_popular.group()
    else:
        raise FormatError('regex pattern not getting popular info when formatting popular.')
