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
#'cookie': 'cna=/cZNFOeZtjQCAWonlMe4QoEC; ubt_ssid=b7cnro1ha1y3ws5qf7eimtczgelfd4ot_2020-02-24; ut_ubt_ssid=pa5i1celw3kfgmsw4pg06an7olfryd05_2020-02-24; _utrace=74260f88589a6898256d006a96b4b26c_2020-02-24; track_id=1582517627|d60570b76a3a1a3337bf4e872a7202e306616d8fc214923cf0|f2a7aee14d4c8d3d68902520581c5dee; tzyy=4b64ae0f3a32d6746b22a89f11b90785; t=f80c68ccf82b7a264265277f4bd6462b; ZDS=1.0|1584096286|zD0qowhxB/0D6Hiy2fVgMUOb0T+bQgiQGTf+q1PbH3CDdUSlxjGQRrAhe5S2AjZWwLhvY+1i/p7Tl2Ji/sQrSw==; t_eleuc4=id4=0%40BA%2FvuHCrrRkeMKtZ%2BjVdIUueZiCRzcvNc1r0Bw%3D%3D; munb=2204442047886; SID=wh2QNq7nKlxPLhm19l9He8GM7oBGUA7fwWjQ29; USERID=125974608; UTUSER=125974608; x5check_ele=j8I1NO0aScKjnrh78CNKj29wd33Wcpjyz%2BYB85m7tEs%3D; isg=BM7Ole2rHEmilqhFVzqJIGXOH6SQT5JJZrsR3PgW_VGMW2-1YN7CWUFSl4c3w4ph; l=dBIaHrbPQhQocPK0BOfNVcuTV1_tqIdb8sPr_WLWwICPO_5B598OWZ4xaOL6CnGVn6zMR37nEPh2BJYHnyCInxv9-INOUmttedTh.',
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

