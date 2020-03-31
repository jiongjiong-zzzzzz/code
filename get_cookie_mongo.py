# -*- coding: utf-8 -*-
'''

获取手机号

模拟登录

获取cookie，存入mongo

'''
import wugui
from config import log
import eleme
import time
import base64
import pymongo
import requests
import cookie_test
connection = pymongo.MongoClient('127.0.0.1',27017)
db=connection.latlon
post = db.cookies

ele = eleme.ElemeApp()
lat, lng = '30.292306', '120.044871'
session = requests.session()
def save_img(data):
    data_byte = base64.b64decode(data)
    with open('captcha.png', 'wb+') as f:
        f.write(data_byte)
def mobile_login():
    while True:
        mobile, mobile_token = wugui.get_phone()
        if not mobile:
            log.exception('token requests error.')
            continue
        if not mobile_token:
            log.exception('token requests error.')
            continue
        resp = ele.mobile_send_code(mobile, lat, lng)
        if resp.get('name') == 'NEED_CAPTCHA':
            resp = ele.get_captcha(mobile, lat, lng)
            print(resp)
            captcha_hash = resp.get('captcha_hash')
            img = resp.get('captcha_image')
            save_img(img)
            value = input('captcha:')
            resp = ele.mobile_send_code_captcha(mobile, lat, lng, captcha_hash, value)
            if resp.get('name') == 'CAPTCHA_CODE_ERROR':
                captcha(mobile, resp)
        print(resp)

        if resp.get('message'):
            time.sleep(2)
            # 号码被封，拉黑
            wugui.lahei_Mobile(mobile, mobile_token)
            continue
        elif resp.get('validate_token'):
            return resp, mobile, mobile_token
        else:
            log.exception('token requests error.')
            time.sleep(3)
            continue
def captcha(mobile,resp):
    if resp.get('name') == 'CAPTCHA_CODE_ERROR':
        resp = ele.get_captcha(mobile, lat, lng)
        print(resp)
        captcha_hash = resp.get('captcha_hash')
        img = resp.get('captcha_image')
        save_img(img)
        value = input('captcha:')
        resp = ele.mobile_send_code_captcha(mobile, lat, lng, captcha_hash, value)
        print(resp)
        if resp.get('name') == 'CAPTCHA_CODE_ERROR':
            captcha(mobile, resp)
        return resp

def login(lat, lng):
    while True:
        resp, mobile, mobile_token = mobile_login()
        sms_code = wugui.get_msn(mobile, mobile_token)
        if not sms_code:
            continue
        token = resp.get('validate_token')
        cookie = ele.login_by_mobile(token, sms_code, lat, lng)
        return cookie


while True:
    mongo_cookie = {'status':'success','count':0}
    cookie = login(lat, lng)
    session.cookies = cookie
    check = cookie_test.test_c(session)
    cookies = requests.utils.dict_from_cookiejar(cookie)
    mongo_cookie['cookie'] = cookies
    if check:
        post.insert(mongo_cookie)
        time.sleep(2)
    else:
        continue