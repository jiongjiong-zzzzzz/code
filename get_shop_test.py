# -*- coding: utf-8 -*-
'''

从mongo获取cookie

抓取数据

'''

from config import log
import eleme
import time
import pymongo
import requests
import random
import redis_
import datetime
import settings
class catchEle(object):
    def __init__(self):
        self.ele = eleme.ElemeApp()
        connection = pymongo.MongoClient('127.0.0.1', 27017)
        SHOP_DATA = settings.SHOP_DATA
        COOKIE = settings.COOKIE
        CITY_POINT = settings.CITY_POINT
        self.CITY = settings.CITY
        self.db = connection.latlon
        self.couser_data = self.db[SHOP_DATA]
        self.couser_cookie = self.db[COOKIE]
        self.couser_point = self.db[CITY_POINT]

        self.session = requests.session()
        self.r = redis_.UrlDB()
        self._id = ''
        self.today = datetime.date.today()
        self.check = 0
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
        random_cookie = self.db.cookies.find({'status': 'success'})[random_index]
        cookie = random_cookie['cookie']
        self._id = random_cookie['_id']
        self.change_cookie_usageCount(random_cookie['count'])
        cookieJar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
        return cookieJar
    '''
    记录cookie使用次数
    '''
    def change_cookie_usageCount (self,count):
        count  += 1
        self.couser_cookie.find_one_and_update({'_id': self._id},
                                            {'$set': {'count':count}}, )

    '''
    修改mongo cookie状态
    '''
    def up_status(self):
        log.error('cookie被封：')
        self.couser_cookie.find_one_and_update({'_id': self._id},
                                                        {'$set': {'status': 'error'}}, )
    '''
    修改经纬度状态
    '''
    def lat_status(self,lat,lng):
        self.couser_point.find_one_and_update(
            {"latitude" : lat,"longitude" : lng},
                                            {'$set': {'status': '1'}}, )
    '''
    从point表获取所有的经纬度，返回一个集合
    '''
    def getLatlon(self):
        LatLng = self.couser_data.find(
            {'status': '0'},no_cursor_timeout=True)
        return LatLng

    '''
    将店铺原始数据存入mongodb，保存待用
    '''
    def shop_Data(self, shop_details):
        self.couser_data.insert_one(shop_details)



    def catch_data(self,items):
        for item in items:
            '''
            参数赋值
            '''
            shop_id = item['id']
            lat,lng = '',''
            self.session.cookies = self.get_cookie_fromMongo()
            try:
                resp = self.ele.get_shop_restaurants(lat, lng,shop_id,self.session)
                print(resp)
            except:
                print(resp)
            address = resp['address']
            # #商家电话
            phone = resp['phone']

            print(phone,address)

    def get_data(self):
        '''
        : 获取从mongdb存储的经纬度坐标
        :return:items:
        :rtype: '''
        items = self.getLatlon()
        self.ele.change_device()
        self.catch_data(items)

    def main(self):
        self.get_data()


if __name__ == '__main__':
    eleme = catchEle()
    eleme.main()

