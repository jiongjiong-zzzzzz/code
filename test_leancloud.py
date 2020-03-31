#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 10:41
# @Author  : ZhangZhao
# @Site    : 
# @File    : test_leancloud.py
# @Software: PyCharm
import leancloud
import logging
logging.basicConfig(level=logging.DEBUG)
leancloud.init("ADOxnCBKMMQJPNUQPxayJnc9-gzGzoHsz", master_key="rdBaOm5m6jeoVHYgT7BDjoME")


TestObject = leancloud.Object.extend('SmsCode')
test_object = TestObject()
test_object.set('smscode', "【饿了么】您的验证码是411831，在5分钟内有效。如非本人操作请忽略本短信。")

test_object.save()