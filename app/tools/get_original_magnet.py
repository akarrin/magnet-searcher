# -*- coding:utf-8 -*-
import re


def get_original_magnet(cook_magnet: str):
    '''
    把爬取到的未经处理的magnet字符串转化为格式化的原始magnet字符串
    :param cook_magnet: 获取到的magnet字符串
    :return: 格式化的原始magnet字符串
    '''
    if 'magnet:?xt=urn:btih:' in cook_magnet:
        return re.search(r'magnet:\?xt=urn:btih:\w{40}', cook_magnet).group()
    else:
        # 如果只有40位hash值,则加上magnet:?xt=urn:btih:
        return 'magnet:?xt=urn:btih:' + re.search(r'\w{40}', cook_magnet).group()
