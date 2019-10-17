# -*- coding:utf-8 -*-

from app.magnet.collect_magnet import collect_magnet, choose_source
from app.const import *
from app.tools.hight_light_keyword import highlight_keyword
from app.tools.get_resolution import get_resolution
from app.tools.output_magnet import output_magnet, format_file_name
from app.tools.sort_magnet_result import sort_magnet_result
import click
from app.config import OUTPUT_PATH
import io
from pathlib import Path
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

selective_source = '、'.join(choose_source())


@click.command()
@click.option('-k', '--keyword', prompt="搜索的关键词, 必填", required=True, help=">> 搜索的关键词, 必填")
@click.argument('extras', nargs=-1)
@click.option('-c', '--count', help=">> 搜索的数量, 跳过则搜索15条", default=15, required=False)
@click.option('-s', '--sort', help=">> 搜索的排序，可选size、hot、date，跳过则选择默认排序", default='', required=False)
@click.option('--source', help=f">> 搜索的优先来源, 可选{selective_source}，跳过则选择默认的优先来源", default='', required=False)
def run(keyword, count, sort, source, extras=''):
    magnet_search_order(keyword, count, sort, source, extras)


def magnet_search_order(keyword, count, sort, source, extras=''):
    keyword = keyword + ' '.join(str(extra) for extra in extras)
    require_count = int(count)
    sorted_by = format_sort_para(sort)
    try:
        magnet_list = collect_magnet(keyword=keyword, require_count=require_count, sorted_by=sorted_by,
                                     first_search_source=source)
        if magnet_list:
            sort_magnet_result(magnet_result=magnet_list, sort_key=sorted_by, is_reverse=True)
            for magnet_flag, a_magnet in enumerate(magnet_list):
                fg = ['cyan', 'magenta'][magnet_flag % 2]
                prettify_echo(magnet_dict=a_magnet, fg=fg, keyword=keyword)
            click.echo(f'\n需要{require_count}条资源，找到了{len(magnet_list)}条')
            new_search_order(count=count, sort=sort, source=source, origin_keyword=keyword, magnet_list=magnet_list)
        else:
            click.echo(f'\n没有找到资源，请更换关键词后重新查找')
            final_input = click.prompt("\n\n请重新输入搜索的关键词, 或按Ctrl+C退出")
            magnet_search_order(final_input, count, sort, source)

    except (EOFError, KeyboardInterrupt):
        click.echo('用户主动中断')
        sys.exit(0)


def new_search_order(count, sort, source, origin_keyword=None, magnet_list=None):
    if magnet_list:
        new_search_keyword = click.prompt("\n\n请输入搜索的关键词，或输入O+Enter导出搜索结果, 或按Ctrl+C退出")
        if new_search_keyword.lower() == 'o':
            output_order(magnet_list, origin_keyword)
            new_search_order(count=count, sort=sort, source=source)
        else:
            magnet_search_order(new_search_keyword, count, sort, source)
    else:
        new_search_keyword = click.prompt("\n\n请输入搜索的关键词, 或按Ctrl+C退出")
        magnet_search_order(new_search_keyword, count, sort, source)


def output_order(magnet_list, keyword):
    path_input = click.prompt(
        "\n\n请输入导出路径，支持txt及csv格式，如'/home/usr/Desktop/output.txt', 或输入D+Enter键直接导出到默认位置")
    if path_input.lower() == 'd':
        file_name = format_file_name(keyword)
        path = Path(OUTPUT_PATH) / file_name
        try:
            output_path = path.with_suffix('.txt')
            output_magnet(magnet_list, output_path)
            click.echo(f'\n成功导出至{output_path}')
        except IOError:
            click.echo('config文件配置的默认导出路径有误，请检查')
    else:
        path = Path(path_input)
        try:
            output_magnet(magnet_list, path)
            click.echo(f'\n成功导出至{path}')
        except IOError:
            click.echo('导出路径有误,请重新输入')
            output_order(magnet_list, keyword)


def format_sort_para(sort):
    if sort == '' or sort == 'default':
        sorted_by = SORTED_BY_DEFAULT
    elif sort == 'size':
        sorted_by = SORTED_BY_SIZE
    elif sort == 'hot' or sort == 'pop' or sort == 'popular':
        sorted_by = SORTED_BY_POPULAR
    elif sort == 'date' or sort == 'time':
        sorted_by = SORTED_BY_DATE
    else:
        sorted_by = SORTED_BY_DEFAULT
    return sorted_by


def prettify_echo(magnet_dict, fg, keyword):
    title = magnet_dict.get('title')
    magnet = magnet_dict.get('magnet')
    size = magnet_dict.get('size')
    create_date = magnet_dict.get('create_date')
    popular = magnet_dict.get('popular')
    source_name = magnet_dict.get('source_name')
    click.secho('-' * 70)
    click.secho('名称      ', fg=fg, nl='', bold=True)
    resolution = get_resolution(title)
    if resolution:
        resolution = ' ' + resolution + ' '
        click.secho(resolution, bg='green', fg='white', nl='')
        click.secho('  ', nl='')
    for highlight_part in highlight_keyword(keyword=keyword, sentence=title):
        if highlight_part.get('is_highlight') == 1:
            click.secho(highlight_part.get('text'), fg='red', nl='')
        elif highlight_part.get('is_highlight') == 0:
            click.secho(highlight_part.get('text'), nl='')
    click.echo('')
    click.secho('磁链      ', fg=fg, nl='', bold=True)
    click.secho(magnet)
    click.secho('大小      ', fg=fg, nl='', bold=True)
    click.secho(size)
    click.secho('日期      ', fg=fg, nl='', bold=True)
    click.secho(create_date)
    click.secho('热度      ', fg=fg, nl='', bold=True)
    click.secho(popular)
    click.secho('来源      ', fg=fg, nl='', bold=True)
    click.secho(source_name)


if __name__ == '__main__':
    run()