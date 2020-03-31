# -*- coding: utf-8 -*-
import requests
import time
import re
from config import log
import cchardet
import traceback
def encode_h(url):
    resp = requests.get(url)
    encoding = cchardet.detect(resp.content)['encoding']
    html = resp.content.decode(encoding, errors='ignore')
    return html
def get_phone():
    print('即将获取新手机号')
    #url = 'http://180.97.250.76:8000/wgapi/login/username=5726615&password=5726615'
    while True:
        url = 'http://to.banma1024.com/api/do.php?action=loginIn&name=api-68358-rRFuOSO&password=5726615'
        resp_t = encode_h(url)
        try:
            status,token= resp_t.split('|')[0],resp_t.split('|')[1]
        except:
            time.sleep(3)
            print('获取异常：'+resp_t)
            return 0, 0
        #url = 'http://180.97.250.76:8000/wgapi/huoqihao/id=10065&operator=0&Region=0&card=0&phone=&loop=1&token={}'
        url = 'http://to.banma1024.com/api/do.php?action=getPhone&sid=178&token={}&qx=1'
        if int(status) == 1:
            url = url.format(token)
            resp_p = encode_h(url)
            #print(resp_p)
            try:
                status, phone = resp_p.split('|')[0], resp_p.split('|')[1]
                if '请过3秒再重新取号' in phone:
                    print(phone)
                    time.sleep(3)
                    continue
            except:
                time.sleep(2)
                log.exception('获取异常：' + resp_t)
                return 0,0
            if int(status) == 1:
                print('获取新的手机号：',phone)
                return (phone,token)
        else:
            time.sleep(2)
            return 0,0
def get_msn(phone,token):
    print('正在获取短信，等待20s')
    time.sleep(20)
    num = 1
    #url = 'http://180.97.250.76:8000/wgapi/yanzhengma/id=10065&phone={}&t=5726615&token={}'.format(phone,token)
    url = 'http://to.banma1024.com/api/do.php?action=getMessage&sid=178&phone={}&token={}'.format(phone,token)
    while True:
        resp = encode_h(url)
        #print(resp)
        status,msn = resp.split('|')[0],resp.split('|')[1]
        if int(status) == 0:
            time.sleep(5)
            print('已等待{}s，到60s换手机号重新登录'.format(30 + 5 * num))
            if num > 6:
                return False #1表示获取不到短信，需要重新请求
            num  = num + 1
            continue
        if int(status) == 1:
            msn = re.search(r'\d+',msn).group()
            print('验证码为：{}'.format(msn))
            return msn

def lahei_Mobile(phone,token):
    url = 'http://to.banma1024.com/api/do.php?action=addBlacklist&sid=178&phone={}&token={}'.format(phone,token)
    resp = encode_h(url)
    # print(resp)
    status, msn = resp.split('|')[0], resp.split('|')[1]
    if int(status) == 1:
        return True
    else:pass

