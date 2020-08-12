# -*- coding: utf-8 -*-
'''

获取手机号

模拟登录

获取cookie，存入mongo

'''
import pymongo
import requests
import cookie_test
import time
connection = pymongo.MongoClient('127.0.0.1',27017)
db=connection.latlon
post = db.cookies
session = requests.session()

mongo_cookie = {'status':'success','count':0}


moblie = input('mobile:')
mongo_cookie['moblie'] = moblie
cookie = input(f'请输入{moblie}对应的cookie:')
cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
tech_names = {'USERID', 'UTUSER', 'SID', 'x5sec','pizza-rc-ca-result'}
p2 = {key: value for key, value in cookies.items() if key in tech_names}

cookie = requests.utils.cookiejar_from_dict(p2, cookiejar=None, overwrite=True)
session.cookies = cookie
check = cookie_test.test_c(session)

mongo_cookie['cookie'] = p2

if check:
    post.insert_one(mongo_cookie)
    time.sleep(2)
else:
    pass

