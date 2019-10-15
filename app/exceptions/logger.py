# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 14:32
# @Author  : Akarrin
# @Github  : https://github.com/akarrin
# @FileName: logger.py
# @Software: PyCharm

import logging
from app.config import DEBUG
from pkg_resources import Requirement, resource_filename
import configparser
from ..config import readable_config_name

# 优先取项目project作为log输出目录
config = configparser.ConfigParser()
config.read(readable_config_name)

log_output_path = config.get('PROJECT PATH', 'log_path', fallback='magnet_searcher.log')


def logger(level: str, message: str, debug=DEBUG):
    if debug:
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
        logging.basicConfig(filename=log_output_path, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
        if level == 'debug':
            logging.debug(message)
        if level == 'info':
            logging.info(message)
        if level == 'warning':
            logging.warning(message)
        if level == 'error':
            logging.error(message)
        if level == 'critical':
            logging.critical(message)
        if level == 'exception':
            logging.exception(message)
