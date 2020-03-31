# -*- coding: utf-8 -*-


import sqlite3
import random
from config import log


class DeviceInfo(object):

    def __init__(self):
        self.tbl_name = 'TBL_PHONE_BASEINFO'
        self.conn = sqlite3.connect('PublicParams.db')
        self.cursor = self.conn.cursor()

    def gen_params(self):
        one_phone = self.get_by_kw()
        one_phone = {k: v for k, v in one_phone}
        return one_phone

    def get_by_kw(self, just_one=True, nocase=False, **kwargs):
        """
        根据指定keyword条件获取手机基本信息
        """
        sql = f'select distinct Id from {self.tbl_name}'
        id_s = self.__sql_select_id(sql)
        id_ = random.choice(id_s)
        one_info = self.__sql_select_all_by_id(id_)
        return one_info

    def __sql_select_id(self, sql):
        """
        内部私有函数，具体查询sql获取内部数据库id
        :param sql: str: sql语句
        :return: list
        """
        try:
            self.cursor.execute(sql)
            values = self.cursor.fetchall()
            return values
        except:
            log.exception('sql_select error.sql:{}'.format(sql))
            return []

    def __sql_select_all_by_id(self, id_):
        """
        内部私有函数，根据数据库ID获取该组数据具体值
        :param id_: str/int: 内部数据库ID
        :return: list
        """
        sql = f'select strKey, strValue from {self.tbl_name} where Id = {id_[0]}'

        try:
            self.cursor.execute(sql)
            values = self.cursor.fetchall()
            return values
        except:
            log.exception(f'sql_select_all_by_id error.id_:{id_}')
            return []


def random_useragent(device_params):
    simulator = 'Dalvik/{}'.format(random.choice(['1.6.0', '2.1.0']))
    android_version = 'Android {}'.format(device_params.get('RELEASE', '9'))
    product = device_params.get('PRODUCT', 'BKL-AL20')
    id_ = device_params.get('ID', 'HUAWEIBKL-AL20')
    return '{} (Linux; U; {}; {} Build/{})'.format(simulator, android_version, product, id_)







if __name__ == '__main__':
    item= DeviceInfo().gen_params()
    print(item)
