#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 11:01
# @Author  : ZhangZhao
# @Site    : 
# @File    : query_lean.py
# @Software: PyCharm
import leancloud
import logging
logging.basicConfig(level=logging.DEBUG)
leancloud.init("ADOxnCBKMMQJPNUQPxayJnc9-gzGzoHsz", master_key="rdBaOm5m6jeoVHYgT7BDjoME")
SmsCode = leancloud.Object.extend('SmsCode')
query = SmsCode.query
while True:
    try:
        todo  = query.first()#获取对象
    except Exception:
        logging.info('还未获取到验证码')
        continue
    #获取验证码
    smscode = todo.get('smscode')
    #对象id
    objectId = todo.id

    print(smscode)
    print(objectId)