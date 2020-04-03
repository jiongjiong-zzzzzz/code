#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 15:55
# @Author  : ZhangZhao
# @Site    : 
# @File    : mongodb_operation.py
# @Software: PyCharm
import settings
import pymongo
import random
from config import log
import requests
class operation:
    def __init__(self):
            connection = pymongo.MongoClient(settings.IP, settings.PORT)
            db                 = connection[settings.DB]
            self.CITY          = settings.CITY
            self.couser_data   = db[settings.SHOP_DATA]
            self.couser_cookie = db[settings.COOKIE]
            self.couser_point  = db[settings.CITY_POINT]

    '''
    从mongo获取读取全部的cookies,随机返回一个cookie
    '''
    def get_cookie_fromMongo(self):
        all_count = self.couser_cookie.find({'status': 'success'}).count()
        if all_count == 0:
            log.error('cookie池为null，需要添加cookie，')
            input('按任意值继续:')
            pass
        random_index = random.randint(0, all_count - 1)
        random_cookie = self.couser_cookie.find({'status': 'success'})[random_index]
        cookie = random_cookie['cookie']
        self._id = random_cookie['_id']
        self.change_cookie_usageCount(random_cookie['count'])
        cookieJar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
        return cookieJar

    '''
       记录cookie使用次数
       '''

    def change_cookie_usageCount(self, count):
        count += 1
        self.couser_cookie.find_one_and_update({'_id': self._id},
                                               {'$set': {'count': count}}, )

    '''
    修改mongo cookie状态
    '''

    def up_status(self):
        log.error('cookie被封：')
        self.couser_cookie.find_one_and_update({'_id': self._id},
                                               {'$set': {'status': 'error'}}, )

    '''
        categorys
    '''

    def up_status_categorys(self,shop_lat_lon,name):
        log.info(f'{shop_lat_lon},{name}')
        try:
            self.couser_data.update_one({'shop_lat_lon': shop_lat_lon},{"$addToSet": {"categorys":name}})
        except:
            log.info(f'没找到数据{shop_lat_lon},{name}')
        # try:
        #     categorys = self.couser_data.find({'shop_lat_lon': shop_lat_lon})[0]['categorys']
        #     print(categorys)
        #     categorys.append(name)
        #     print(categorys)
        # except:
        #     return None
        # self.couser_cookie.find_one_and_update({'shop_lat_lon': shop_lat_lon},
        #                                        {'$set': {'categorys': categorys}},)

    '''
    修改经纬度状态
    '''

    def lat_status(self, lat, lng):
        self.couser_point.find_one_and_update({"latitude": lat, "longitude": lng},
                                              {'$set': {'status': '1'}} )

    '''
    从point表获取所有的经纬度，返回一个集合
    '''

    def getLatlon(self):
        LatLng = self.couser_point.find(
            {'status': '0', 'city': self.CITY}, no_cursor_timeout=True)
        return LatLng

    '''
      将店铺详细信息存入mongodb
      '''
    # def shop_Details(self,shop_details):
    #     self.couser_details.insert_one(shop_details)

    '''
    将店铺原始数据存入mongodb，保存待用
    '''

    def shop_Data(self, shop_details):
        self.couser_data.insert_one(shop_details)
