import eleme
import base64
import requests
import time,redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)
shop_id = r.srandmember('id')

def save_img(data):
    data_byte = base64.b64decode(data)
    with open('captcha.png', 'wb+') as f:
        f.write(data_byte)
ele = eleme.ElemeApp()
ele.change_device()
lat, lng = '30.7', '121.288'


def test_c(session):
    print('测试')
    resp,resp_json = ele.get_restaurants_test(lat, lng, '2', '5', 0, session)
    if resp != 200:
        print(resp_json)
        print('请求失败：'+str(resp))
        return False
    print('测试cookie成功访问一次')
    time.sleep(1)
    resp_, resp_json = ele.get_restaurants_test(lat, lng, '2', '5', 0, session)
    #resp_ ,resp_json= ele.get_shop_restaurants_test(lat, lng,shop_id,session)

    if resp_ != 200:
        print(resp_json)
        print('请求失败：' + str(resp_))
        return False
    print('测试cookie成功访问两次，存入mongodb，待用')
    return True

