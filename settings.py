#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/26 14:16
# @Author  : ZhangZhao
# @Site    : 
# @File    : settings.py
# @Software: PyCharm

'''
mongdb集合
'''

IP = '127.0.0.1'
PORT = 27017

DB = 'latlon'
#储存店铺数据的集合
SHOP_DATA = 'hangzhouData_4_1_1'
#储存cookie信息的集合
COOKIE = 'cookies'
#储存经纬度的集合
CITY_POINT  = 'city_point_4_1'
#城市名称
CITY = '杭州'

'''
REDIS
'''

#去重set集合
REDIS_SHOP_NAME = 'hangzhou_shop_id_4_1'
#url去重
REDIS_SHOP_URL = 'hangzhou_shop_url_4_1'
#
REDIS_CATEGORY = 'hangzhou_category_4_1'


data = {
  "timeout": 15000,
  "requests": {
    "restaurant": {
      "method": "GET",
      "url": "/shopping/restaurant/{}?extras[]=activities&extras[]=flavors&extras[]=albums&extras[]=videos&extras[]=coupon&extras[]=qualification&latitude=39.862940926104784&longitude=116.29824567586184",
      "ex_r": "{}",
      "ex_dc": "{}",
      "ex_d": "{}"
    },
    "menu": {
      "method": "GET",
      "url": "/shopping/v2/menu?restaurant_id=E9292171348932016877",
      "ex_r": "{}",
      "ex_dc": "{}",
      "ex_d": "{}"
    },
    "coupon_info": {
      "method": "GET",
      "url": "/shopping/v1/restaurants/E9292171348932016877/exclusive_hongbao/overview?latitude=39.862940926104784&longitude=116.29824567586184"
    },
    "metadata": {
      "method": "GET",
      "url": "/shopping/v1/restaurants/E9292171348932016877/metadata"
    },
    "showcase": {
      "method": "GET",
      "url": "/shopping/v2/restaurants/E9292171348932016877/quality_combo"
    },
    "popups": {
      "method": "GET",
      "url": "/promotion/v1/users/564234162/restaurants/E9292171348932016877/popups"
    },
    "discount_helper": {
      "method": "GET",
      "url": "/shopping/v1/discount_helper_status?shop_id=E9292171348932016877&latitude=39.862940926104784&longitude=116.29824567586184"
    },
    "tie_in_sale": {
      "method": "GET",
      "url": "/shopping/v1/restaurants/E9292171348932016877/tie_in_sale?latitude=39.862940926104784&longitude=116.29824567586184&city_id=3"
    },
    "member_card": {
      "method": "GET",
      "url": "/shopping/v1/restaurant/E9292171348932016877/member_card"
    },
    "rebuy_info": {
      "method": "GET",
      "url": "/bos/v1/users/564234162/restaurants/E9292171348932016877/rebuy?geohash=wx4dy2vf3wc3"
    },
    "bought_foods2": {
      "method": "GET",
      "url": "/shopping/v1/restaurants/E9292171348932016877/bought_skus?user_id=564234162"
    },
    "coupon_popup": {
      "method": "GET",
      "url": "/member/v2/users/564234162/supervip/popup?source=3"
    },
    "favor": {
      "method": "GET",
      "url": "/ugc/v1/user/564234162/favor/restaurant/check?restaurant_id=E9292171348932016877"
    },
    "delivery_info": {
      "method": "GET",
      "url": "/shopping/v1/restaurant/E9292171348932016877/delivery?latitude=39.862940926104784&longitude=116.29824567586184"
    },
    "rating": {
      "method": "GET",
      "url": "/ugc/v3/restaurants/E9292171348932016877/ratings/scores?latitude=39.862940926104784&longitude=116.29824567586184"
    }
  }
}

