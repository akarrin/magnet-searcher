# -*- coding:utf-8 -*-
from pathlib import Path
import re


def output_magnet(magnet_list, output_path):
    '''
    把magnet资源列表导出到output_path
    :param magnet_list:
    :param output_path:
    :return:
    '''
    path = Path(output_path)
    if path.suffix in ['.txt', '.csv']:  # 校验是否以.txt和.csv作为后缀
        with path.open("w", encoding='utf-8') as f:
            for a_magnet in magnet_list:
                title = a_magnet.get('title')
                magnet = a_magnet.get('magnet')
                size = a_magnet.get('size')
                create_date = a_magnet.get('create_date')
                popular = a_magnet.get('popular')
                source_name = a_magnet.get('source_name')
                f.write(f'名称      {title}\n')
                f.write(f'磁链      {magnet}\n')
                f.write(f'大小      {size}\n')
                f.write(f'日期      {create_date}\n')
                f.write(f'热度      {popular}\n')
                f.write(f'来源      {source_name}\n')
                f.write('-' * 100 + '\n')
    else:
        raise IOError


def format_file_name(name):
    # 以搜索的关键词作为文件名时,去除windows文件路径中不允许使用的符号
    return re.sub('\?|/|\||:|"|<|>|\*|\\\\', '', name)
