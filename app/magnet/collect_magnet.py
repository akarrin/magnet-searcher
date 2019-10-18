from app.config import PROXIES
from app.rules import rules
from .get_magnet import get_magnet
from ..exceptions.error import HttpError
from ..exceptions.logger import logger
from app.const import *
from requests.exceptions import SSLError, Timeout


def collect_magnet(keyword: str, require_count: int, sorted_by: int = SORTED_BY_DEFAULT,
                   first_search_source: str = None) -> list:
    '''
    从rules中获取source及相应规则,按顺序或指定source完成资源获取
    :param keyword: 查询的关键词
    :param require_count: 需要的资源数量,按magnet去重
    :param sorted_by: 排序规则，可根据大小、日期、热度倒序排序
    :param first_search_source: 指定优先搜索的source,但需要满足choose_source的规则
    :return: 去重的资源list
    '''
    source_list = choose_source(first_search_source)
    got_magnet_count = 0
    magnet_set = set()
    magnet_list = []
    print('')
    for source in source_list:  # 从source列表里按序循环获取资源
        a_source_rule_dict = rules.get(source)
        source_name = a_source_rule_dict.get('source_name')
        page = 1
        print('\r' + ' ' * 100, end='', flush=True)
        print(f"\r正在请求{source_name}...", end='', flush=True)
        while got_magnet_count < require_count:
            try:
                get_magnet_by_source = get_magnet(source=a_source_rule_dict, keyword=keyword, page=page,
                                                  sorted_by=sorted_by)
                for a_result_dict in get_magnet_by_source:
                    magnet = a_result_dict.get('magnet')
                    if magnet == MAGNET_NOT_FOUND:
                        continue
                    if not magnet in magnet_set:  # magnet重复检查
                        magnet_list.append(a_result_dict)
                        got_magnet_count += 1
                        magnet_set.add(magnet)
                    if got_magnet_count == require_count:  # 满足数量需求则结束迭代
                        break
            except HttpError as e:
                print('\r' + ' ' * 100, end='', flush=True)
                print(f'\r{e}', end='', flush=True)
                logger('exception', f'\n{e}')
                break
            except SSLError as e:
                print('\r' + ' ' * 100, end='', flush=True)
                print(f'\rSSL Error, 跳过{source_name}', end='', flush=True)
                logger('exception', f'\n{e}')
                break
            except Timeout as e:
                print('\r' + ' ' * 100, end='', flush=True)
                print(f'\r请求{source_name}超时', end='', flush=True)
                logger('exception', f'\n{e}')
                break
            except IndexError as e:
                print('\r' + ' ' * 100, end='', flush=True)
                print(f'\r{source_name}中没有找到该资源', end='', flush=True)
                logger('exception', f'\n{e}')
                break  # 当前页没有更多数据则结束该source的循环
            except Exception as e:
                logger('exception', f'\n{e}')
                break
            page += 1
        if got_magnet_count == require_count:  # 满足数量需求则结束迭代
            break
    print('\r' + ' ' * 100, end='', flush=True)
    print(f'\r请求完成', end='\n\n', flush=True)
    return magnet_list


def choose_source(first_search_source: str = None):
    source_list = []
    proxy_channel = len(PROXIES)
    for rule_name, rule in rules.items():
        if rule.get('proxy_channel') and not proxy_channel:  # rule需要代理时但没有配置代理地址时舍弃该source
            continue
        elif not rule.get('active'):  # 舍弃active为false的source
            continue
        elif rule_name == first_search_source:  # 插入优先搜索的资源到列表头
            source_list.insert(0, rule_name)
        else:
            source_list.append(rule_name)
    return source_list
