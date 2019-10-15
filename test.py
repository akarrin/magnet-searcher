# -*- coding: utf-8 -*-
# @Time    : 2019/10/15 12:06
# @Author  : Akarrin
# @Github  : https://github.com/akarrin
# @FileName: test.py
# @Software: PyCharm
from app.magnet.get_magnet import get_magnet
from app.rules import rules

if __name__ == '__main__':
    # print(rules.get('ciliwang'))
    magnets = get_magnet(rules.get('ciliwang'), '上海堡垒', 2, 0)
    for magnet in magnets:
        print(magnet)
