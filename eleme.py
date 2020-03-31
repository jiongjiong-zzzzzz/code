# -*- coding: utf-8 -*-



from deviceinfo import DeviceInfo, random_useragent
from config import log
import requests
import random
import time
import tool
from copy import copy
from urllib import parse
import base64
import pymongo
import redis_operating
import settings
from fake_useragent import UserAgent
headers = {
    'user-agent': '',
    'cache-control': 'no-cache',
    'x-deviceinfo': '',
    'x-shard': '',
    'x-eleme-requestid': '',
    'random': '',
    'deadpoolcontent': '',
    'deadpool': '',
    'content-type': 'application/json; charset=UTF-8',
    'accept-encoding': 'gzip',
}


class ElemeApp(object):

    def __init__(self, ):
        self.local_60002 = requests.session()
        self.local_60002.keep_alive = True
        self.local_proxy = requests.session()
        self.local_proxy.keep_alive = True
        self.s = requests.session()
        self.headers = headers
        self.dv_params = {}
        self.ua = ''
        self.proxy = None
        self.version = '8.12.0'
        self.r = redis_operating.UrlDB()

    def mobile_send_code(self, mobile, lat, lng):
        url = 'https://restapi.ele.me/eus/login/mobile_send_code'
        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'ex_r': '{}'.format(result[0]),
            'ex_dc': '{}'.format(result[1]),
            'ex_d': '{}'.format(result[2]),
        })

        data = '{"mobile":"%s","latitude":%s,"longitude":%s,"via_audio":false}' % (
            str(mobile), str(lat), str(lng),
        )
        try:
            resp = self.s.post(url, headers=headers, data=data, proxies = self.proxy, timeout=3)
            return resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('mobile_send_code error.')
            return None

    def get_captcha(self, mobile, lat, lng):
        url = 'https://restapi.ele.me/eus/v4/captchas?captcha_str={}'.format(mobile)
        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'ex_r': '{}'.format(result[0]),
            'ex_dc': '{}'.format(result[1]),
            'ex_d': '{}'.format(result[2]),
        })
        headers.pop('content-type')
        try:
            resp = self.s.get(url, headers=headers, proxies=self.proxy, timeout=3)
            return resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('get_captcha error.')
            return None

    def mobile_send_code_captcha(self, mobile, lat, lng, captcha_hash, captcha_value):
        url = 'https://restapi.ele.me/eus/login/mobile_send_code'
        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'ex_r': '{}'.format(result[0]),
            'ex_dc': '{}'.format(result[1]),
            'ex_d': '{}'.format(result[2]),
        })

        data = '{"mobile":"%s","captcha_hash":"%s","captcha_value":"%s","latitude":%s,"longitude":%s,"via_audio":false}' % (
            str(mobile), str(captcha_hash), str(captcha_value), str(lat), str(lng),
        )
        try:
            resp = self.s.post(url, headers=headers, data=data, proxies=self.proxy, timeout=3)
            return resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('mobile_send_code_captcha error.')
            return None

    def login_by_mobile(self, token, sms_code, lat, lng):
        url = 'https://restapi.ele.me/eus/login/login_by_mobile'
        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'ex_r': '{}'.format(result[0]),
            'ex_dc': '{}'.format(result[1]),
            'ex_d': '{}'.format(result[2]),
        })
        data = '{"validate_token":"%s","validate_code":"%s","latitude":%s,"longitude":%s}' % (
            str(token), str(sms_code), str(lat), str(lng),
        )

        try:
            resp = self.s.post(url, headers=headers, data=data, proxies=self.proxy, timeout=3)
            return self.s.cookies
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('login_by_mobile error.')
            return None

    def get_restaurants(self, lat, lng, city_id, order_by, offset):
        url = 'https://restapi.ele.me/shopping/v3/restaurants?extras[]=identification&extras[]=coupon&' \
              'latitude={}&longitude={}&city_id={}&rank_id={}&network_operator=&network=WIFI&order_by={}&' \
              'extra_filters=home&os=Android%2F{}&deivce={}&weather_code=CLEAR_DAY&offset={}&limit=20'.format(
            lat, lng, city_id, tool.gen_random_af(32), order_by, self.dv_params.get('RELEASE'),
            parse.quote(self.dv_params.get('MODEL')), offset
        )
        url = 'https://restapi.ele.me/shopping/v3/restaurants?extras[]=coupon&latitude=31.243828888982534&longitude=121.48247290402651&city_id=1&rank_id=&business_flag=0&restaurant_category_ids%5B%5D=1&offset=0&limit=20'
        url = 'https://restapi.ele.me/shopping/v3/restaurants?extras[]=coupon&latitude=30.725792&longitude=121.268812&city_id=1&rank_id=&business_flag=0&order_by=5&restaurant_category_ids%5B%5D=4&offset=0&limit=20'

        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'ex_r': '{}'.format(result[0]),
            'ex_dc': '{}'.format(result[1]),
            'ex_d': '{}'.format(result[2]),
        })
        try:
            resp = self.s.get(url, headers=headers, proxies=self.proxy, timeout=3)
            return resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('login_by_mobile error.')
            return None
    '''
    供外部调用
    '''
    def get_restaurants_(self, lat, lng, city_id, order_by, offset,seesion):
        url = 'https://restapi.ele.me/shopping/v3/restaurants?extras[]=identification&extras[]=coupon&' \
              'latitude={}&longitude={}&city_id={}&rank_id={}&network_operator=&network=WIFI&order_by={}&' \
              'extra_filters=home&os=Android%2F{}&deivce={}&weather_code=CLEAR_DAY&offset={}&limit=20'.format(
            lat, lng, city_id, tool.gen_random_af(32), order_by, self.dv_params.get('RELEASE'),
            parse.quote(self.dv_params.get('MODEL')), offset
        )
        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'ex_r': '{}'.format(result[0]),
            'ex_dc': '{}'.format(result[1]),
            'ex_d': '{}'.format(result[2]),
        })
        try:
            resp = seesion.get(url, headers=headers, proxies=self.proxy, timeout=3)
            return resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('login_by_mobile error.')
            return None

    '''
       获取ids
    '''

    def get_ids(self, lat, lng, city_id):
        while True:
            ua = self.random_useragent_eleme()
            xdeviceinfo = self.gen_x_deviceinfo()
            headers = {
                'user-agent': ua,
                'x-deviceinfo': xdeviceinfo
            }
            url = 'https://restapi.ele.me/shopping/v2/restaurant/category?latitude={}&city_id={}&longitude={}'.format(lat,city_id,lng)
            try:
                resp = requests.get(url,headers=headers)
            except Exception as e:
                log.error(e)
                time.sleep(5)
                continue



            items = resp.json()
            ids = []
            category = []
            categorys = ''
            count = 0
            for item in items:
                if item['name'] == '全部商家':
                    count = item['count']
                    continue
                filter = ['厨房生鲜', '水果', '医药健康', '鲜花绿植', '商店超市']
                if item['name'] in filter:
                    continue
                infos = item['sub_categories']
                if count < 400:
                    for info in infos:
                        if '全部' in info['name']:
                            continue
                        elif info['count'] == 0:
                            continue
                        elif info['count'] != 0:
                            if info['name'] in category:
                                continue
                            category.append(info['name'])
                            ids.append(info['id'])
                else:
                    for info in infos:
                        if '全部' in info['name']:
                            if info['count'] < 400:
                                ids.append(info['id'])
                                break
                        elif info['count'] == 0:
                            continue
                        elif info['count'] != 0:
                            if info['name'] in category:
                                continue
                            category.append(info['name'])
                            if info['count'] < 14:
                                categorys = categorys + 'restaurant_category_ids%5B%5D={}&'.format(info['id'])
                                continue
                            ids.append(info['id'])
            if count < 400:
                for id in ids:
                    categorys  = categorys + 'restaurant_category_ids%5B%5D={}&'.format(id)

            return ids,count,categorys


    def get_ids_dict(self, lat, lng, city_id):
        '''
        返回字典格式数据
        :return:
        :rtype:
        '''
        while True:
            ua = self.random_useragent_eleme()
            xdeviceinfo = self.gen_x_deviceinfo()
            headers = {
                'user-agent': ua,
                'x-deviceinfo': xdeviceinfo
            }
            url = 'https://restapi.ele.me/shopping/v2/restaurant/category?latitude={}&city_id={}&longitude={}'.format(lat,city_id,lng)
            try:
                resp = requests.get(url,headers=headers)
            except Exception as e:
                log.error(e)
                time.sleep(5)
                continue



            items = resp.json()
            ids = []
            category = []
            categorys = ''
            count = 0
            for item in items:
                if item['name'] == '全部商家':
                    count = item['count']
                    continue
                filter = ['厨房生鲜', '水果', '医药健康', '鲜花绿植', '商店超市']
                if item['name'] in filter:
                    continue
                infos = item['sub_categories']
                for info in infos:
                    if '全部' in info['name']:
                        continue
                    elif info['count'] == 0:
                        continue
                    elif info['count'] != 0:
                        if info['name'] in category:
                            continue
                        category.append(info['name'])
                        print(info['id'], info['name'], info['count'])
                        if info['count'] < 14:
                            categorys = categorys + 'restaurant_category_ids%5B%5D={}&'.format(info['id'])
                            continue
                        name = info['name']
                        ids[f'{name}'] = info['id']

            return ids,count,categorys

    '''
            广州供外部调用
        '''
    def get_restaurants_guangzhou(self, lat, lng, city_id, order_by,id,offset, seesion):
        url = 'https://restapi.ele.me/shopping/v3/restaurants?extras[]=coupon&latitude={}&longitude={}&city_id={}&rank_id=&business_flag=0&order_by={}&restaurant_category_ids%5B%5D={}&offset={}&limit=20'.format(lat,lng,city_id,order_by,id,offset)
        Flag = self.r.has_url(url)
        if not Flag:
            log.info('重复的url')
            return None
        log.info(url)

        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'ex_r': '{}'.format(result[0]),
            'ex_dc': '{}'.format(result[1]),
            'ex_d': '{}'.format(result[2]),
        })
        try:
            resp = seesion.get(url, headers=headers, proxies=self.proxy, timeout=10)
            return resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('login_by_mobile error.')
            return None

    def get_restaurants_all_id(self, lat, lng, city_id, order_by, categorys, offset, seesion):
        url = 'https://restapi.ele.me/shopping/v3/restaurants?extras[]=coupon&latitude={}&longitude={}&city_id={}&rank_id=&business_flag=0&order_by={}&{}offset={}&limit=20'.format(
            lat, lng, city_id, order_by, categorys, offset)
        Flag = self.r.has_url(url)
        if not Flag:
            log.info('重复的url')
            return None
        log.info(url)

        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'ex_r': '{}'.format(result[0]),
            'ex_dc': '{}'.format(result[1]),
            'ex_d': '{}'.format(result[2]),
        })
        try:
            resp = seesion.get(url, headers=headers, proxies=self.proxy, timeout=10)
            return resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('login_by_mobile error.')
            return None
    def get_restaurants_test(self, lat, lng, city_id, order_by, offset,seesion):
        url = 'https://restapi.ele.me/shopping/v3/restaurants?extras[]=identification&extras[]=coupon&' \
              'latitude={}&longitude={}&city_id={}&rank_id={}&network_operator=&network=WIFI&order_by={}&' \
              'extra_filters=home&os=Android%2F{}&deivce={}&weather_code=CLEAR_DAY&offset={}&limit=20'.format(
            lat, lng, city_id, tool.gen_random_af(32), order_by, self.dv_params.get('RELEASE'),
            parse.quote(self.dv_params.get('MODEL')), offset
        )
        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'ex_r': '{}'.format(result[0]),
            'ex_dc': '{}'.format(result[1]),
            'ex_d': '{}'.format(result[2]),
        })
        try:
            resp = seesion.get(url, headers=headers, proxies=self.proxy, timeout=10)
            return resp.status_code,resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('login_by_mobile error.')
            return None
    def get_shop_restaurants(self, lat, lng,shopId,session):
        url = 'https://restapi.ele.me/shopping/restaurant/{}?extras[]=activities&extras[]=flavors&extras[]=albums&extras[]=videos&extras[]=coupon&extras[]=qualification&latitude={}&longitude={}'.format(shopId,lat,lng)
        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'Content-Type': 'application/json;charset = UTF-8',
            'ex_r': '{}'.format(result[0]),
            'ex_dc': '{}'.format(result[1]),
            'ex_d': '{}'.format(result[2]),
        })
        try:
            resp = session.get(url, headers=headers, proxies=self.proxy, timeout=3)
            return resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('login_by_mobile error.')
            return None
    def get_shop_restaurants_menu(self, lat, lng,shopId,session):

        url = '	https://restapi.ele.me/shopping/v2/menu?restaurant_id={}'.format(shopId)

        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'random': '{}'.format(result[0]),
            'deadpoolcontent': '{}'.format(result[1]),
            'deadpool': '{}'.format(result[2]),
        })
        try:
            resp = session.get(url, headers=headers, proxies=self.proxy, timeout=3)
            return resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('login_by_mobile error.')
            return None
    def get_shop_restaurants_test(self, lat, lng,shopId,session):

        url = '	https://restapi.ele.me/shopping/restaurant/{}?extras[]=activities&extras[]=flavors&extras[]=albums&extras[]=videos&extras[]=coupon&extras[]=qualification&latitude={}&longitude={}'.format(shopId,lat,lng)

        headers = copy(self.headers)
        result = self.sneer(url)
        headers.update({
            'x-shard': 'loc={},{}'.format(lng, lat),
            'x-eleme-requestid': '{}|{}'.format(tool.gen_uuid().upper().replace('-', ''), tool.get_timestamp()),
            'random': '{}'.format(result[0]),
            'deadpoolcontent': '{}'.format(result[1]),
            'deadpool': '{}'.format(result[2]),
        })
        try:
            resp = session.get(url, headers=headers, proxies=self.proxy, timeout=3)
            return resp.status_code,resp.json()
        except requests.exceptions.ConnectTimeout:
            self.proxy = tool.get_proxy(self.local_proxy)
            return None
        except:
            log.exception('login_by_mobile error.')
            return None
    def change_device(self):
        self.s = requests.session()
        # self.proxy = tool.get_proxy(self.local_proxy)
        di = DeviceInfo()
        self.dv_params = di.gen_params()
        self.imei = self.dv_params.get('getDeviceId')[:-3] + str(random.randint(100, 999))
        self.hardware_id = tool.gen_random_af(32)
        self.serial = self.dv_params.get('SERIAL')[:-3] + str(random.randint(100, 999))
        self.ua = self.random_useragent_eleme()
        self.xdeviceinfo = self.gen_x_deviceinfo()
        self.headers.update({
            'user-agent': self.ua,
            'x-deviceinfo': self.xdeviceinfo
        })

    def random_useragent_eleme(self):
        kernal_ver = ['3.4.39', '3.10.0', '3.16.1', '3.18.10', '4.4.1']
        return 'Rajax/1 {}/{} Android/{} Display/{} Eleme/{} Channel/moxiu ID/{}; KERNEL_VERSION:{} API_Level:{} Hardware:{}'.format(
            tool.replace_blank(self.dv_params.get('MODEL')), tool.replace_blank(self.dv_params.get('PRODUCT')),
            tool.replace_blank(self.dv_params.get('RELEASE')), tool.replace_blank(self.dv_params.get('DISPLAY')),
            self.version, tool.gen_uuid(), random.choice(kernal_ver) + '-g8bac269',
            tool.replace_blank(self.dv_params.get('SDK_INT')), self.hardware_id
        )

    def gen_x_deviceinfo(self):
        tmpl = 'imei:{} serial:{} android_id:{} brand:{} model:{} macAddress:02_00_00_00_00_00 netType:WIFI simState:1 ' \
               'wifiList:{} haveBluetooth:true track_id: memory:1384 energy_percent:{} first_open:{} last_open:{}' \
               ' net_type:WIFI hardware_id:{}'.format(
                self.imei, self.serial, tool.gen_random_af(16),
                tool.replace_blank(self.dv_params.get('BRAND')), tool.replace_blank(self.dv_params.get('MODEL')),
                '_'.join([tool.gen_random_af(2) for i in range(6)]), random.randint(10, 98),
                tool.get_timestamp(10), tool.get_timestamp(10), self.hardware_id
                )
        return tool.base64_encode(tmpl)

    def sneer(self, param_url):
        uri = parse.urlparse(param_url).path
        if parse.urlparse(param_url).query:
            uri += '?' + parse.urlparse(param_url).query
        url = 'http://127.0.0.1:60002/sneer'
        while True:
            try:
                resp = self.local_60002.post(url, data=uri)
                result = resp.text
                result = result.split(';')
                if len(result) == 3:
                    return result
                log.info('sneer error, continue.{}'.format(result))
            except:
                log.exception('127.0.0.1 requests error.')
                time.sleep(2)
                continue


def save_img(data):
    data_byte = base64.b64decode(data)
    with open('captcha.png', 'wb+') as f:
        f.write(data_byte)


if __name__ == '__main__':
    connection = pymongo.MongoClient('127.0.0.1', 27017)
    db = connection.latlon
    post = db.test_quanbu
    ele = ElemeApp()
    ele.change_device()
    mobile = '17718537723'
    lat, lng = '39.862944949418306', '116.29824567586184'
    resp = ele.mobile_send_code(mobile, lat, lng)
    print(resp)
    if resp.get('name') == 'NEED_CAPTCHA':
        resp = ele.get_captcha(mobile, lat, lng)
        print(resp)
        captcha_hash = resp.get('captcha_hash')
        img = resp.get('captcha_image')
        save_img(img)
        value = input('captcha:')

        resp = ele.mobile_send_code_captcha(mobile, lat, lng, captcha_hash, value)
        print(resp)

    token = resp.get('validate_token')
    sms_code = input('sms_code:')
    resp = ele.login_by_mobile(token, sms_code, lat, lng)

    #print(resp)
    ids = ''
    index = 0
    while True:
        print(index)
        offset = index * 20
        resp = ele.get_restaurants(lat, lng, '2', '5', offset)
        resp = ele.get_shop_restaurants(lat, lng, '3', '5', offset)
        index += 1
        print(resp)
        time.sleep(1)
        post.insert(resp['items'])
