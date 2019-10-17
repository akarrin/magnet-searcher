# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 17:49
# @Author  : Akarrin
# @Github  : https://github.com/akarrin
# @FileName: config.py
# @Software: PyCharm

import configparser
from pathlib import Path
from pkg_resources import Requirement, resource_filename

# 优先取项目project的配置文件内容
try:
    pkg_config_name = resource_filename(Requirement.parse("magnet-searcher"), "config.ini")
except:
    pkg_config_name = "config.ini"
config = configparser.ConfigParser()
config.read(pkg_config_name)
project_config_name = config.get('PROJECT PATH', 'config_path', fallback=False)
if project_config_name:
    try:
        config.read(project_config_name)
        readable_config_name = project_config_name
    except:
        readable_config_name = pkg_config_name
        pass
else:
    readable_config_name = pkg_config_name

PROXIES = {
    'http': config.get('PROXIES', 'http', fallback=None),
    'https': config.get('PROXIES', 'https', fallback=None),
}

REQUEST_TIME_OUT = config.getint('TIME OUT', 'request_time_out', fallback=None)

FAKE_HEADERS = {
    'Accept': config.get('FAKE HEADERS', 'Accept', fallback=None),
    'Accept-Charset': config.get('FAKE HEADERS', 'Accept-Charset', fallback=None),
    'Accept-Encoding': config.get('FAKE HEADERS', 'Accept-Encoding', fallback=None),
    'Accept-Language': config.get('FAKE HEADERS', 'Accept-Language', fallback=None),
    'User-Agent': config.get('FAKE HEADERS', 'User-Agent', fallback=None),
    'Referrer': config.get('FAKE HEADERS', 'Referrer', fallback=None),
}

OUTPUT_PATH = Path.home() / 'Desktop'  # 默认目录为桌面

DEBUG = config.getboolean('DEBUG', 'DEBUG', fallback=False)