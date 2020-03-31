import redis
import settings
class UrlDB:
    '''Use LevelDB to store URLs what have been done(succeed or faile)
    '''
    status_failure = b'0'
    status_success = b'1'

    def __init__(self,):
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
        self.r = redis.Redis(connection_pool=pool)
        self.REDIS_SHOP_NAME = settings.REDIS_SHOP_NAME
        self.REDIS_SHOP_URL = settings.REDIS_SHOP_URL
    def saveId(self,shop_id):
        if isinstance(shop_id, str):
            shop_id = shop_id.encode('utf8')
        try:
            attr = self.r.sadd('id',shop_id)
        except:
            pass

    def has(self, shop_id):

        if isinstance(shop_id, str):
            shop_id = shop_id.encode('utf8')
        try:
            attr = self.r.sadd('guangzhou_shop_id_3_30',shop_id)
            return attr
        except:
            pass
        return False

    def has_url(self, url):

        if isinstance(url, str):
            shop_id = url.encode('utf8')
        try:
            attr = self.r.sadd('guangzhou_shop_url_3_30',shop_id)
            return attr
        except:
            pass
        return False