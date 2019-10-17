# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 11:48
# @Author  : Akarrin
# @Github  : https://github.com/akarrin
# @FileName: setup.py
# @Software: PyCharm

from setuptools import setup, find_packages

import configparser
from pathlib import Path

# 获取安装路径并写到config.ini
root_path = Path.cwd()
config_path = str(root_path / 'config.ini')
rules_path = str(root_path / 'rules.json')
log_path = str(root_path / 'magnet_searcher.log')
config = configparser.ConfigParser()
config.read('config.ini')
if not config.has_section('PROJECT PATH'):
    config.add_section('PROJECT PATH')
config.set('PROJECT PATH', 'config_path', config_path)
config.set('PROJECT PATH', 'rules_path', rules_path)
config.set('PROJECT PATH', 'log_path', log_path)
with open('config.ini', 'w') as configfile:
    config.write(configfile)

setup(
    name='magnet-searcher',
    version='1.0',
    packages=find_packages(),
    description='command line magnet searcher tool',
    author='Akarrin',
    install_requires=["requests", "lxml", "Click", "Pysocks", "configparser", "arrow"],
    url='https://github.com/akarrin/magnet-searcher',
    py_modules=["magnet_search"],
    data_files=[('.', ['config.ini', 'rules.json'])],
    entry_points={
        'console_scripts': ['magnet-searcher=magnet_search:run']
    },
)
