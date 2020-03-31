# -*- coding: utf-8 -*-



# from Cryptodome.PublicKey import RSA

import rsa
from Cryptodome.Cipher import AES, DES
from pyDes import des, CBC, PAD_PKCS5
from config import DEBUG, log
from datetime import datetime
import uuid
import random
import string
import time
import base64
import re

def get_proxy(s):
    return None


def gen_now_time_str():
    now_time = datetime.now()
    return '{}-{}-{} {}:{}:{}:{}'.format(
        now_time.year, now_time.month, now_time.day, now_time.hour, now_time.minute, now_time.second, int(now_time.microsecond/1000)
    )


def gen_uuid():
    return str(uuid.uuid4())


def get_timestamp(type=13):
    if type == 13:
        return int(time.time()*1000)
    else:
        return int(time.time())


def base64_encode(data):
    return base64.b64encode(data.encode()).decode()


def gen_random_af(size):
    result = list()
    while True:
        result.append("".join(random.sample("0123456789abcdef", 1)))
        if len(result) >= size:
            break
    return "".join(result)


def rsa_encrypt(data, n, e):
    key = rsa.PublicKey(n, e)
    data_enc = rsa.encrypt(data.encode(), key)
    return base64.b64encode(data_enc)


def sql_format(sql_templte, *args):
    params = []
    for one in args:
        one = str(one)
        one = one.replace("'", "''")
        params.append(one)
    sql = sql_templte.format(*params)
    return sql.replace("'None'", "NULL")


def replace_blank(str_data: str):
    return str_data.replace(' ', '_')


def aes_decrypt(data):
    data = base64.b64decode(data)
    iv = 'thisisdefaultaes'.encode()
    key = 'ele.me.risk.framework.SecurityEntry'.encode()
    decryptor = AES.new(key, AES.MODE_CBC, iv=iv)
    return decryptor.decrypt(data)


def des_decrypt(data):
    data = base64.b64decode(data)
    key = 'kwBq8snI'.encode()
    decryptor = DES.new(key, mode=DES.MODE_CBC, iv=key)
    return decryptor.decrypt(data)


def des_encrypt(data):
    key = 'kwBq8snI'.encode()
    data = data.encode()
    if len(data) % 8 != 0:
        pad = 8 - len(data) % 8
        data += bytes([pad]*pad)
    decryptor = DES.new(key, mode=DES.MODE_CBC, iv=key)
    encrypt_data = decryptor.encrypt(data)
    return base64.b64encode(encrypt_data)


def des_encrypt_2(data):
    key = 'kwBq8snI'.encode('utf8')
    iv = key
    k = des(key, CBC, iv, padmode=PAD_PKCS5)
    encrypt_data = k.encrypt(data.encode('utf8'), padmode=PAD_PKCS5)
    return base64.b64encode(encrypt_data)


if __name__ == '__main__':
    a = '{"A32":[{"x":-0.42870852,"y":0.021555176,"z":9.642349},{"x":-0.42870852,"y":0.0071850587,"z":9.651929},{"x":-0.43349856,"y":0.009580079,"z":9.642349}],"A38":125,"A14":"CA\\u003d\\u003d\\n","A53":"51203","A23":"angler-03.61","A16":100.0,"A21":"Unplugged","A29":1566471120,"A10":"google","A48":"google/angler/angler:6.0.1/MTC20L/3230295:user/release-keys","A8":"MTC20L","A12":"84B7N16411000597","A51":"DP","A25":[],"A56":"1040","A33":8,"A20":"1555200","A4":"armv8l","A18":"Nexus 6P","A26":"1440,2392","A19":560,"A52":"DP","A54":"3.1415926535897932384","A40":1566459838009,"A7":"unknown","A35":{"hashInfo":[],"number":0},"A24":"867686022890006","A34":"unknown","A41":1565688663000,"A3":"3.10.73-g8bac269\\nandroid-build@vpak19.mtv.corp.google.com #1\\nTue Aug 9 18:34:19 UTC 2016","A28":1566471275007,"A36":{"latitude":30.29177116440114,"longitude":120.04594230478068},"A42":1,"A9":"02:00:00:00:00:00","A55":"538183952","A1":"android","A30":{"hashInfo":[{"hash":"384adbfd1bfa8f0b557c0e529ec4592a","ts":21598},{"hash":"2e3f2fd634b736871ef893bea3f5941a","ts":21598}],"number":2},"A11":"WIFI","A15":"","A37":"com.google.android.youtube-com.android.providers.telephony-com.android.sdm.plugins.connmo-com.google.android.googlequicksearchbox-com.android.providers.calendar-com.android.providers.media-com.huawei.entitlement-com.google.android.onetimeinitializer-com.android.wallpapercropper-com.quicinc.cne.CNEService","A22":"6.0.1","A13":"unknown","A43":"1230796800000","A5":"dpsh14eb239ab7194d30ed18c3dcc215c4a1atpu","A44":0,"A6":1,"A2":1566471275354,"A45":1,"A49":"DP","A46":"14148@25608","A39":"com.github.shadowsocks-com.sankuai.meituan-com.bigsing.changer-com.leon.elemehook-zzz.zzzz.fake_alipay-de.robv.android.xposed.installer-me.ele-com.tencent.mm-com.sankuai.meituan.takeoutnew-com.leon.meituansohook","A27":0.0,"A50":"761ED4E10F38A73F506DCF8136778594FC410F05F8C69D7D7C4D0DD56513A7A2","A47":"10.10.23.160","A31":[{"bssid":"00:06:f4:b0:65:a0","rssi":-40,"ssid":"\\"10JQKA\\""}],"A17":[{"bssid":"00:06:f4:b0:65:a0","ssid":"10JQKA"},{"bssid":"30:45:96:e3:21:d3","ssid":"HUAWEI Mate 20 Pro"},{"bssid":"30:b4:9e:09:60:f5","ssid":"Ths_test"}]}'
    print(des_encrypt_2(a))
    print(des_encrypt(a))

    b = '''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'''
    print(des_decrypt(b))
