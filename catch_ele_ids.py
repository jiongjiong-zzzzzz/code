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
import redis_operating
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
        self.r = redis_operating.UrlDB()
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
                                            {'$set': {'status': '0'}}, )
    '''
    从point表获取所有的经纬度，返回一个集合
    '''
    def getLatlon(self):
        LatLng = self.couser_point.find(
            {'status': '1','city':self.CITY},no_cursor_timeout=True)
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

    def little_count(self,lat, lng, city_id,categorys,index,count,province,city):
        self.check = 0
        while True:
            if self.check == 1:
                break
            offset = index * 20
            self.session.cookies = self.get_cookie_fromMongo()
            resp = self.ele.get_restaurants_all_id(lat, lng, city_id, 5, categorys, offset, self.session)
            if resp is None:
                break
            elif resp.get('message'):
                self.up_status()
                log.error('请求异常，换手机号，重新登录')
                continue
            try:
                if resp['has_next'] is False:
                    self.check = 1

            except:
                print(resp)
                input("has_next读取出错，需要检查原因：")
            '''
            请求出错
            '''
            log.info('经纬度：[{}],[{}]，第{}页,该页有[{}]个店铺，一共[{}]个店铺'.format(lat, lng, index,
                                                                      len(resp['items']), count))
            for item in resp['items']:
                restaurant = item['restaurant']
                # 省
                restaurant['province'] = province
                # 市
                restaurant['city'] = city
                # 店铺id
                restaurant_id = restaurant['id']
                # 抓取日期
                restaurant['date'] = str(self.today)
                #log.info('店铺名称：{}'.format(restaurant['name']))
                shop_lat_lon = restaurant['name'] + '/' + str(restaurant['latitude']) + '/' + str(
                    restaurant['longitude'])
                Flag = self.r.has(shop_lat_lon)

                if Flag:
                    resp_ = self.ele.get_shop_restaurants(lat, lng, restaurant_id, self.session)
                    print(resp_)
                    # 商家地址
                    restaurant['shop_address'] = resp_['address']
                    # 商家电话
                    restaurant['phone'] = resp_['phone']
                    self.shop_Data(restaurant)
                else:
                    continue

            index += 1
            time.sleep(1)

    def catch_data(self,items):
        for item in items:
            '''
            参数赋值
            '''
            lat, lng, city_id, city, province, index = item['latitude'], item['longitude'], item['city_id'], item[
                'city'], item['province'], 0
            '''
            获取品类id，ids为包含店铺数量较大的品类id组成的列表，categorys为店铺数量小于13的品类id组成的url参数
            '''
            ids, count, categorys = self.ele.get_ids(lat, lng, city_id)

            log.info('该经纬度共有[{}]家店铺'.format(count))
            if count > 400:
                for id in ids:
                    self.check,index = 0,0
                    while True:
                        if self.check:
                            break
                        # 页数
                        offset = index * 20
                        # 获取cookie
                        self.session.cookies = self.get_cookie_fromMongo()
                        # 发起请求
                        resp = self.ele.get_restaurants_guangzhou(lat, lng, city_id, 5, id, offset, self.session)

                        if not resp :
                            '''
                            返回None，说明此id已经爬过了，直接break抓下一个id 可能会漏掉一部分店铺（假如此id有10店铺，但爬到第八页程序停止，下一次就不会爬剩下的两页）

                            可优化，当爬虫程序退出之前，可记录经纬度爬到了第几个id的第几页，下次读取状态直接爬

                            但大部分店铺是重复爬取的，未爬到的店铺数量可忽略不计
                            '''
                            break

                        '''如果有‘message’说明请求异常'''
                        if resp.get('message'):
                            self.up_status()
                            log.error('请求异常，换手机号，重新登录')
                            continue
                        '''如果有‘has_next’属性为False，说明已经爬完，没有下一页了'''
                        try:
                            if resp['has_next'] is False:
                                self.check = 1
                                log.info('该品类id附近店铺已经抓取完毕，换下一个id')
                        except:
                            print(resp)
                            input("has_next读取出错，需要检查原因：")

                        log.info('经纬度：[{}],[{}]，品类id:[{}]，第{}页,该页有[{}]个店铺，一共[{}]个店铺'.format(lat, lng, id, index,
                                                                                            len(resp['items']), count))
                        '''解析店铺数据'''
                        for item in resp['items']:
                            restaurant = item['restaurant']
                            '''省,市'''
                            restaurant['province'],restaurant['city'],restaurant['status']= province,city,0
                            restaurant_id = restaurant['id']
                            #log.info('店铺名称：{}'.format(restaurant['name']))
                            '''店铺id'''
                            #restaurant_id = restaurant['id']
                            # 抓取日期
                            restaurant['date'] = str(self.today)
                            '''组合店铺名称，经纬度三个属性，存到redis用于去重'''
                            shop_lat_lon = restaurant['name'] + '/' + str(restaurant['latitude']) + '/' + str(
                                restaurant['longitude'])
                            '''
                            去重操作，set集合，返回1，说明插入字段，返回0说明已经存在无需插入
                            '''
                            Flag = self.r.has(shop_lat_lon)
                            if Flag:
                                '''
                                将数据插入mongodb
                                '''
                                self.shop_Data(restaurant)
                                resp_ = self.ele.get_shop_restaurants(lat, lng,restaurant_id,self.session)
                                print(resp_)
                                #商家地址
                                restaurant['shop_address'] = resp_['address']
                                #商家电话
                                restaurant['phone'] = resp_['phone']
                            else:
                                '''
                                说明返回的是0，即字段已存在，为重复数据
                                '''
                                continue
                        '''
                        页数+1
                        '''
                        index += 1
                        time.sleep(1)
                if categorys:
                    index = 0
                    self.little_count(lat, lng, city_id, categorys, index, count, province, city)
            elif categorys:
                self.little_count(lat, lng, city_id, categorys, index, count, province, city)
            self.lat_status(lat, lng)
            log.info('该经纬度附近店铺已经抓取完毕，换下一个经纬度')

    def get_longitude_latitude(self):
        '''
        : 获取从mongdb存储的经纬度坐标
        :return:items:
        :rtype:
        '''
        items = self.getLatlon()
        self.ele.change_device()
        self.catch_data(items)

    def main(self):
        self.get_longitude_latitude()


if __name__ == '__main__':
    eleme = catchEle()
    eleme.main()

