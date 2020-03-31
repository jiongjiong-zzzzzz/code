#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/17 17:23
# @Author  : ZhangZhao
# @Site    : 
# @File    : sub_categories.py
# @Software: PyCharm
import requests
header = {
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'max-age=0',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
}
resp = requests.get('https://restapi.ele.me/shopping/v2/restaurant/category?latitude=22.519534&city_id=1&longitude=113.899811')
items = resp.json()
ids = {}
category = []
categorys = ''
count = 0
for item in items:
    if item['name'] == '全部商家':
        count = item['count']
        continue
    filter = ['厨房生鲜','水果','医药健康','鲜花绿植','商店超市']
    if item['name']  in filter:
        continue
    infos  = item['sub_categories']
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
                print(info['id'], info['name'], info['count'])
                name = info['name']
                ids[f'{name}'] = info['id']
    else:
        for info in infos:
                if '全部' in info['name']:
                    continue
                    if info['count'] < 400:
                        ids.append(info['id'])
                        break
                elif info['count'] == 0:
                    continue
                elif info['count'] != 0:
                    if info['name'] in category:
                        continue
                    category.append(info['name'])
                    print(info['id'], info['name'], info['count'])

                    if info['count'] < 14 :
                        categorys = categorys + 'restaurant_category_ids%5B%5D={}&'.format(info['id'])
                        continue
                    name = info['name']
                    ids[f'{name}'] = info['id']
if count < 400:
    for id in ids:
        categorys  = categorys + 'restaurant_category_ids%5B%5D={}&'.format(id)
print(count)
print(categorys)

print(len(ids),ids)

