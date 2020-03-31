#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/23 18:48
# @Author  : ZhangZhao
# @Site    : 
# @File    : items.py
# @Software: PyCharm
#原始数据
                                #shop_detail['restaurant'] = restaurant
                                #抓取日期
                                # shop_detail['date'] = str(self.today)
                                # #省
                                # shop_detail['province'] = province
                                # #市
                                # shop_detail['city'] = city
                                # #店铺id
                                # shop_detail['restaurant_id'] = restaurant_id
                                # #authentic_id
                                # try:
                                #     shop_detail['authentic_id'] = restaurant['authentic_id']
                                # except:
                                #     shop_detail['authentic_id'] = ''
                                # # brand_id
                                # try:
                                #     shop_detail['brand_id'] = restaurant['brand_id']
                                # except:
                                #     shop_detail['brand_id'] = ''
                                # #店铺logo
                                # try:
                                #     shop_detail['restaurant_image'] = restaurant['image_path']
                                # except:
                                #     shop_detail['restaurant_image']= ''
                                # #经纬度
                                # try:
                                #     shop_detail['latitude'] = restaurant['latitude']
                                # except:
                                #     shop_detail['latitude'] = ''
                                # try:
                                #     shop_detail['longitude'] = restaurant['longitude']
                                # except:
                                #     shop_detail['longitude'] = ''
                                #
                                # #店铺名称
                                # try:
                                #     shop_detail['shop_name'] = restaurant['name']
                                # except:
                                #     shop_detail['shop_name'] = ''
                                # #门店评分
                                # try:
                                #     shop_detail['rating'] = restaurant['rating']
                                # except:
                                #     shop_detail['rating'] = ''
                                # # 是否新店
                                # try:
                                #     shop_detail['is_new'] = restaurant['is_new']
                                # except:
                                #     shop_detail['is_new'] = ''
                                # # 是否新店
                                # try:
                                #     shop_detail['is_premium'] = restaurant['is_premium']
                                # except:
                                #     shop_detail['is_premium'] = ''
                                # #is_star
                                # try:
                                #     shop_detail['is_star'] = restaurant['is_star']
                                # except:
                                #     shop_detail['is_star'] = ''
                                # # is_valid
                                # try:
                                #     shop_detail['is_valid'] = restaurant['is_valid']
                                # except:
                                #     shop_detail['is_valid']= ''
                                # # type
                                # try:
                                #     shop_detail['type'] = restaurant['type']
                                # except:
                                #     shop_detail['type'] = ''
                                # #配送类型
                                # try:
                                #     send =  restaurant['delivery_mode']
                                #     if send is None:
                                #         shop_detail['delivery_mode'] = ''
                                #     else:shop_detail['delivery_mode'] = restaurant['delivery_mode']['text']
                                # except:
                                #     shop_detail['delivery_mode'] = ''
                                # #起送价格
                                # try:
                                #     shop_detail['float_minimum_order_amount'] = restaurant['float_minimum_order_amount']
                                # except:
                                #     shop_detail['float_minimum_order_amount'] = ''
                                # #营业时间
                                # try:
                                #     shop_detail['opening_hours'] = restaurant['opening_hours'][0]
                                # except:
                                #     shop_detail['opening_hours'] = ''
                                # #品牌类型
                                # try:
                                #     shop_detail['folding_restaurant_brand'] = restaurant['folding_restaurant_brand']
                                # except:
                                #     shop_detail['folding_restaurant_brand'] = ''
                                # #商品类型
                                # try:
                                #     flavors = []
                                #     for each in restaurant['flavors']:
                                #         description = each['name']
                                #         flavors.append(description)
                                #     shop_detail['flavors'] = flavors
                                # except:
                                #     shop_detail['flavors'] = ''
                                # try:
                                #     shop_detail['rating_count'] = restaurant['rating_count']
                                # except:
                                #     shop_detail['rating_count'] = ''
                                # #月销量
                                # try:
                                #     shop_detail['recent_order_num'] = restaurant['recent_order_num']
                                # except:
                                #     shop_detail['recent_order_num'] = ''
                                # try:
                                #     shop_detail['business_info'] = eval(restaurant['business_info'])['recent_order_num_display']
                                # except:
                                #     shop_detail['business_info'] = ''
                                # #评论数
                                # try:
                                #     shop_detail['rating_count'] = restaurant['rating_count']
                                # except:
                                #     shop_detail['rating_count'] = ''
                                # #公告
                                # try:
                                #     shop_detail['promotion_info'] = restaurant['promotion_info']
                                # except:
                                #     shop_detail['promotion_info'] = ''
                                # #配送费
                                # try:
                                #     shop_detail['float_delivery_fee'] = restaurant['float_delivery_fee']
                                # except:
                                #     shop_detail['float_delivery_fee'] = ''
                                # try:
                                #     recommend_reasons = []
                                #     for each in restaurant['recommend_reasons']:
                                #         reason = each['reason'][0]['text']
                                #         recommend_reasons.append(reason)
                                #     shop_detail['recommend_reasons'] = recommend_reasons
                                # except:
                                #     shop_detail['recommend_reasons'] = ''
                                # try:
                                #
                                #     descriptions = []
                                #     for each in restaurant['activities']:
                                #         description = each['description']
                                #         descriptions.append(description)
                                #     shop_detail['activities'] = descriptions
                                # except:
                                #     shop_detail['activities'] = ''


                                # resp_ = self.ele.get_shop_restaurants(lat, lng,restaurant_id,self.session)
                                # #商家地址
                                # shop_detail['shop_address'] = resp_['address']
                                # #商家电话
                                # shop_detail['phone'] = resp_['phone']

                                # #获取商家活动信息
                                # descriptions = []
                                # for each in resp_['activities']:
                                #     description = each['description']
                                #     descriptions.append(description)
                                # activities = '/'.join(descriptions)
                                # shop_detail['activities']  = activities
                                # #获取商家image
                                # try:
                                #     images = []
                                #     for each in resp_['albums']:
                                #         cover_image_hash = each['cover_image_hash']
                                #         images.append(cover_image_hash)
                                #     image = '/'.join(images)
                                #     shop_detail['images'] = image
                                # except:
                                #     print('无详情image')
                                #print(shop_detail)
                                # self.shop_Details(shop_detail)