#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 18:42
# @Author  : ZhangZhao
# @Site    : 
# @File    : abuyun.py
# @Software: PyCharm
# ! -*- encoding:utf-8 -*-

import requests

# 要访问的目标页面
targetUrl = "http://test.abuyun.com"
# targetUrl = "http://proxy.abuyun.com/switch-ip"
# targetUrl = "http://proxy.abuyun.com/current-ip"

# 代理服务器
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HM2JUEKN11WD27CD"
proxyPass = "533BB05637237280"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}
def get_proxies():
    return proxies

