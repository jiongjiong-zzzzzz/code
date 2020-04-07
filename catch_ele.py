# -*- coding: utf-8 -*-
'''

从mongo获取cookie

抓取数据

'''

from config import log
import eleme
import time
import requests
import redis_operating
import datetime
import mongodb_operation as op

class catchEle(object):
    def __init__(self):
        self.ele = eleme.ElemeApp()
        self.session = requests.session()
        self.r = redis_operating.UrlDB()
        self._id = ''
        self.today = datetime.date.today()
        self.check = 0
        self.mo = op.operation()


    def little_count(self,lat, lng, city_id, categorys, index, count, province, city):
        self.check = 0
        while True:
            if self.check == 1:
                break
            offset = index * 20
            self.session.cookies = self.mo.get_cookie_fromMongo()
            resp = self.ele.get_restaurants_all_id(lat, lng, city_id, 5, categorys, offset, self.session)
            if resp is None:
                break
            elif resp.get('message'):
                self.mo.up_status()
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
                    time.sleep(2)
                    resp_ = self.ele.get_shop_restaurants(lat, lng, restaurant_id, self.session)
                    # 商家地址
                    #restaurant['shop_address'] = resp_['address']
                    # 商家电话
                    #restaurant['phone'] = resp_['phone']
                    restaurant['restaurants'] = resp_
                    self.mo.shop_Data(restaurant)
                else:
                    continue

            index += 1
            time.sleep(1)

    def data(self,items):
        for item in items:
            '''
            参数赋值
            '''
            lat, lng, city_id, city, province, index = item['latitude'], item['longitude'], item['city_id'], item[
                'city'], item['l_province'], 0
            '''
            获取品类id，ids为包含店铺数量较大的品类id组成的列表，categorys为店铺数量小于13的品类id组成的url参数
            '''
            ids, count, categorys = self.ele.get_ids_dict(lat, lng, city_id)

            log.info('该经纬度共有[{}]家店铺'.format(count))
            # if count > 400:
            for name,id in ids.items():
                    log.info('[{}],[{}]'.format(id,name))
                    self.check,index = 0,0
                    while True:
                        if self.check:
                            break
                        # 页数
                        offset = index * 20
                        # 获取cookie
                        self.session.cookies = self.mo.get_cookie_fromMongo()
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
                            self.mo.up_status()
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
                            restaurant['categorys']= []
                            restaurant_id = restaurant['id']
                            log.info('店铺名称：{}，品类名称：{}'.format(restaurant['name'],name))
                            '''店铺id'''
                            #restaurant_id = restaurant['id']
                            # 抓取日期
                            restaurant['date'] = str(self.today)
                            '''组合店铺名称，经纬度三个属性，存到redis用于去重'''
                            shop_lat_lon = restaurant['name'] + '/' + str(restaurant['latitude']) + '/' + str(
                                restaurant['longitude'])
                            shuo_category_id = shop_lat_lon+ '/'+ str(name)
                            '''
                            去重操作，set集合，返回1，说明插入字段，返回0说明已经存在无需插入
                            '''
                            Flag = self.r.has(shop_lat_lon)
                            if Flag:
                                restaurant['shop_lat_lon'] = shop_lat_lon

                                restaurant['categorys'].append(name)
                                self.r.has_category(shuo_category_id)


                                '''
                                将数据插入mongodb
                                
                                '''
                                # 获取cookie
                                #self.session.cookies = self.mo.get_cookie_fromMongo()
                                time.sleep(2)
                                #resp_ = self.ele.get_shop_restaurants(lat, lng,restaurant_id,self.session)

                                resp_ = self.ele.get_shop_mini(restaurant_id)
                                if resp_ is None:
                                    log.error('爬取店铺出错')
                                restaurant['restaurants'] = resp_
                                self.mo.shop_Data(restaurant)
                            else:
                                Flag = self.r.has_category(shuo_category_id)
                                if Flag:
                                    self.mo.up_status_categorys(shop_lat_lon,name)
                                '''
                                说明返回的是0，即字段已存在，为重复数据
                                '''
                                continue
                        '''
                        页数+1
                        '''
                        index += 1
                        time.sleep(0.5)
            if categorys:
                    index = 0
                    self.little_count(lat, lng, city_id, categorys, index, count, province, city)
            # elif categorys:
            #     self.little_count(lat, lng, city_id, categorys, index, count, province, city)
            self.mo.lat_status(lat, lng)
            log.info(f'{lat},{lng}该经纬度附近店铺已经抓取完毕，换下一个经纬度')

    def data_thread(self, item):

            '''
            参数赋值
            '''
            lat, lng, city_id, city, province, index = item['latitude'], item['longitude'], item['city_id'], item[
                'city'], item['l_province'], 0
            '''
            获取品类id，ids为包含店铺数量较大的品类id组成的列表，categorys为店铺数量小于13的品类id组成的url参数
            '''
            ids, count, categorys = self.ele.get_ids_dict(lat, lng, city_id)

            log.info('该经纬度共有[{}]家店铺'.format(count))
            # if count > 400:
            for name, id in ids.items():
                log.info('[{}],[{}]'.format(id, name))
                self.check, index = 0, 0
                while True:
                    if self.check:
                        break
                    # 页数
                    offset = index * 20
                    # 获取cookie
                    self.session.cookies = self.mo.get_cookie_fromMongo()
                    # 发起请求
                    resp = self.ele.get_restaurants_guangzhou(lat, lng, city_id, 5, id, offset, self.session)

                    if not resp:
                        '''
                        返回None，说明此id已经爬过了，直接break抓下一个id 可能会漏掉一部分店铺（假如此id有10店铺，但爬到第八页程序停止，下一次就不会爬剩下的两页）

                        可优化，当爬虫程序退出之前，可记录经纬度爬到了第几个id的第几页，下次读取状态直接爬

                        但大部分店铺是重复爬取的，未爬到的店铺数量可忽略不计
                        '''
                        break

                    '''如果有‘message’说明请求异常'''
                    if resp.get('message'):
                        self.mo.up_status()
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
                        restaurant['province'], restaurant['city'], restaurant['status'] = province, city, 0
                        restaurant['categorys'] = []
                        restaurant_id = restaurant['id']
                        log.info('店铺名称：{}，品类名称：{}'.format(restaurant['name'], name))
                        '''店铺id'''
                        # restaurant_id = restaurant['id']
                        # 抓取日期
                        restaurant['date'] = str(self.today)
                        '''组合店铺名称，经纬度三个属性，存到redis用于去重'''
                        shop_lat_lon = restaurant['name'] + '/' + str(restaurant['latitude']) + '/' + str(
                            restaurant['longitude'])
                        shuo_category_id = shop_lat_lon + '/' + str(name)
                        '''
                        去重操作，set集合，返回1，说明插入字段，返回0说明已经存在无需插入
                        '''
                        Flag = self.r.has(shop_lat_lon)
                        if Flag:
                            restaurant['shop_lat_lon'] = shop_lat_lon

                            restaurant['categorys'].append(name)
                            self.r.has_category(shuo_category_id)

                            '''
                            将数据插入mongodb

                            '''
                            # 获取cookie
                            #self.session.cookies = self.mo.get_cookie_fromMongo()
                            time.sleep(1)
                            #resp_ = self.ele.get_shop_restaurants(lat, lng, restaurant_id, self.session)
                            resp_ = self.ele.get_shop_mini(restaurant_id)

                            if resp_ is None:
                                log.error('爬取店铺出错')
                            restaurant['restaurants'] = resp_
                            self.mo.shop_Data(restaurant)
                        else:
                            Flag = self.r.has_category(shuo_category_id)
                            if Flag:
                                self.mo.up_status_categorys(shop_lat_lon, name)
                            '''
                            说明返回的是0，即字段已存在，为重复数据
                            '''
                            continue
                    '''
                    页数+1
                    '''
                    index += 1
                    time.sleep(0.5)
            if categorys:
                index = 0
                self.little_count(lat, lng, city_id, categorys, index, count, province, city)
            # elif categorys:
            #     self.little_count(lat, lng, city_id, categorys, index, count, province, city)
            self.mo.lat_status(lat, lng)
            log.info('该经纬度附近店铺已经抓取完毕，换下一个经纬度')

    def get_longitude_latitude(self):
        '''
        : 获取从mongdb存储的经纬度坐标
        '''
        items = self.mo.getLatlon()
        self.ele.change_device()
        self.data(items)

    def main(self):
        self.get_longitude_latitude()


if __name__ == '__main__':
    eleme = catchEle()
    eleme.main()

