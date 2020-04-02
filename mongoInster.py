# -*- coding: utf-8 -*-
import pymongo
connection = pymongo.MongoClient('127.0.0.1', 27017)
db         = connection['latlon']
post = db['city_point_4_1']
import csv
city_id = {'上海':'1','广州':'4','杭州':'2','南京':'6','北京':'3','成都':'14','深圳':'11'}
with open('all_point.csv','r',encoding='utf-8')as csvfile:
    reader_1 = csv.DictReader(csvfile)
    for each  in reader_1:
            latlon = dict(each)
            latlon['test'] = []
            latlon['city_id'] = city_id[latlon['city']]
            latlon['status'] = '0'
            latlon['filter'] = '0'
            post.insert_one(latlon)
            print(latlon)
    csvfile.close()
# test  = post.find({"count" : "35",})[0]['test']
# print(test)
# post.update_one({"count" : "35",},{"$addToSet": {'test': '77'}} )
# print(post.find({"count" : "35",})[0]['test'])







