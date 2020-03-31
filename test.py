#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/28 10:08
# @Author  : ZhangZhao
# @Site    : 
# @File    : test.py
# @Software: PyCharm

import catch_ele,eleme
import requests
session = requests.session()
catch = catch_ele.catchEle()
ele = eleme.ElemeApp()
session.cookies = catch.get_cookie_fromMongo()
lat, lng = '39.862944949418306', '116.29824567586184'
shopId = 'E9292171348932016877'
resp = ele.get_shop_restaurants(lat, lng,shopId,session)
print(resp)