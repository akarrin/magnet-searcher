# -*- coding:utf-8 -*-
import re
import arrow


def get_original_magnet(cook_magnet: str):
    '''
    把爬取到的未经处理的magnet字符串转化为格式化的原始magnet字符串
    :param cook_magnet: 获取到的magnet字符串
    :return: 格式化的原始magnet字符串
    '''
    if 'magnet:?xt=urn:btih:' in cook_magnet:
        return re.search(r'magnet:\?xt=urn:btih:\w{40}|magnet:\?xt=urn:btih:\w{32}', cook_magnet).group()
    else:
        # 如果hash值,则加上magnet:?xt=urn:btih:
        return 'magnet:?xt=urn:btih:' + re.search(r'\w{40}|\w{32}', cook_magnet).group()


def format_size(cook_size: str) -> (str, float):
    '''
    把爬取到的未经处理的size字符串转化为格式化的形式，并转化为mb以供后续比较大小
    :param cook_size: 爬取到的未经处理的size字符串
    :return: 格式化的size形式, 数值MB
    '''
    size_info = re.sub(u'[\u4e00-\u9fa5]|\s', '', cook_size)
    try:
        size_num, size_capacity = re.search(r'(\d+\.*\d*)(\w*)', size_info).groups()
        if size_num:
            if size_capacity.lower() in ['m', 'mb']:
                size_as_mb = float(size_num)
            elif size_capacity.lower() in ['g', 'gb']:
                size_as_mb = float(size_num) * 1024
            else:
                size_as_mb = 0
            return size_info, size_as_mb
        else:
            return size_info, 0
    except AttributeError:
        return size_info, 0


def format_date(cook_date: str):
    '''
     把爬取到的未经处理的date字符串转化为可读性更高的字符串，并转化为格式化日期以供后续比较大小
    :param cook_date: 爬取到的未经处理的日期字符串
    :return: 可读性更高的日期字符串，格式化的日期
    '''
    is_format_date_found = re.search(r'(\d{4})\D*(\d{1,2})*\D*(\d*)', cook_date)
    if is_format_date_found:
        useful_date = list(filter(None, list(is_format_date_found.groups())))
        date_format_shape = "-".join(useful_date)
        if len(useful_date) == 1:
            format_date = arrow.get(date_format_shape, "YYYY").format('YYYY-MM-DD')
        elif len(useful_date) == 2:
            format_date = arrow.get(date_format_shape, "YYYY-M").format('YYYY-MM-DD')
        else:
            format_date = arrow.get(date_format_shape, "YYYY-M-D").format('YYYY-MM-DD')
    else:
        try:
            date_num, date_unit = re.search(r'(\d+)(\D+)', cook_date).groups()
            unit_found = re.search(r'(秒|刚|现|now|sec)|(时|hour)|(天|day)|(周|星期|week)|(月|mon)|(年|year)',
                                   date_unit.lower()).groups()
            sec, hour, day, week, month, year = [float(date_num) if unit else 0 for unit in unit_found]
            format_date = arrow.utcnow().shift(seconds=-sec, hours=-hour, days=-day, weeks=-week, months=-month,
                                               years=-year).format('YYYY-MM-DD')
        except AttributeError:
            format_date = '1900-01-01'
    human_readable_date = arrow.get(format_date, 'YYYY-MM-DD').humanize(
        locale='zh')  # 因为arrow包0.15.2版本中文适配问题,需要在locales.py中第797行增加week、weeks的key和值，否则周会报错
    return human_readable_date, format_date


def format_popular(cook_popular_index: str):
    return re.search(r'\d+', cook_popular_index).group()


if __name__ == "__main__":
    print(format_date('创建时间：2019-10-11'))