# -*- coding:utf-8 -*-

import re
def get_resolution(title):
    '''
    通过正则匹配从title中获取视频的分辨率
    :param title: 资源的标题
    :return: 格式化的分辨率字符串
    '''
    resolution_pattern = re.compile('480|720|1080|1920|2k|4k|标清|高清|超清|原画')
    resolution = re.search(resolution_pattern, title.lower())  # 中文以每个单字作为关键字
    if resolution:
        if resolution.group().isdigit():  # 纯数字字符串后面加"P"
            return resolution.group() + 'P'
        else:
            return resolution.group()
    else:
        return
