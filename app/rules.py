# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 10:47
# @Author  : Akarrin
# @Github  : https://github.com/akarrin
# @FileName: rules.py
# @Software: PyCharm

'''
  "btbit": {
    "source_name": "btbit",  # 名称
    "active": false,  # True/False,是否激活,若False使其临时失效
    "base_url": "http://en.btbit.net",  # 搜索源的host
    "query_tail": "/list/{keyword}/{page}-{sorted_by}-0.html",  # 请求url的参数拼接
    "sorted_by": {
      "default": 0,
      "date": 1,
      "size": 2,
      "popular": 3
    },  # 对应排列条件的url参数值
    "proxy_channel": true,  # 是否需要代理,如需要代理但config.py中未设置代理,则直接略过该搜索源
    "judge_result_xpath": "/html/body/div[@class='wrapper']/div[@class='p-wrapper']/div[contains(@class, 'sort-box')]",  # 判断是否有搜索结果的xpath
    "content_list_xpath": "/html/body/div[@class='wrapper']/div[@class='p-wrapper']/div[@class='pbox'][2]/div",  # 搜索结果列表的xpath
    "title_content_xpath": "string(div[@class='title']/h3/a)",  # 标题的xpath,接上content_list_xpath
    "magnet_xpath": "string(div[@class='sbar']/span[1]/a/@href)",  # magnet的xpath,接上content_list_xpath
    "create_date_xpath": "string(div[@class='sbar']/span[3]/b)",  # 资源日期的xpath,接上content_list_xpath,可为空
    "size_xpath": "string(div[@class='sbar']/span[4]/b)",  # 资源大小的xpath,接上content_list_xpath,可为空
    "popular_xpath": "string(div[@class='sbar']/span[6]/b)"  # 资源热度的xpath,接上content_list_xpath,可为空
  }
'''

import json
from pkg_resources import Requirement, resource_filename
import configparser
from .config import readable_config_name


def load_json(path):
    with open(path, "r", encoding='utf-8') as f:
        rules = json.load(f)
    return rules


# 选择可读的config.ini
config = configparser.ConfigParser()
config.read(readable_config_name)
try:
    pkg_rules_path = resource_filename(Requirement.parse("magnet-searcher"), "rules.json")
except:
    pkg_rules_path = "rules.json"
project_rules_path = config.get('PROJECT PATH', 'rules_path', fallback=False)
if project_rules_path:
    try:
        rules = load_json(project_rules_path)
    except:
        rules = load_json(pkg_rules_path)
else:
    rules = load_json(pkg_rules_path)
