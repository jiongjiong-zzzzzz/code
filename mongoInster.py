# -*- coding: utf-8 -*-


import csv
city_id = {'上海':'1','广州':'4','杭州':'2','南京':'6','北京':'3','成都':'14','深圳':'11'}
with open('guangzhou_city_point_26.csv','r',encoding='utf-8')as csvfile:
    reader_1 = csv.DictReader(csvfile)
    for each  in reader_1:
            latlon = dict(each)
            latlon['city_id'] = city_id[latlon['city']]
            latlon['status'] = '0'

            print(latlon)
            #post.insert_one(latlon)
    csvfile.close()

