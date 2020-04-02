#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 18:44
# @Author  : ZhangZhao
# @Site    : 
# @File    : test_abuyun.py
# @Software: PyCharm
import abuyun
import requests
# proxies = abuyun.get_proxies()
# targetUrl = "http://test.abuyun.com"
# for i in range(5):
#     resp = requests.get(targetUrl, proxies=proxies)
#     print(resp.text)


class abuyunaaa:
    def __init__(self):
        self.proxy = abuyun.get_proxies()

    def test(self):
        targetUrl = "http://test.abuyun.com"
        for i in range(5):
            resp = requests.get(targetUrl, proxies=self.proxy)
            print(resp.text)

if __name__ == '__main__':
    abuyunaaa().test()