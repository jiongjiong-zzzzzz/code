# -*- coding: utf-8 -*-



from logger import Logger
import pathlib
import sys
import os
import random

APP_NAME = 'elme'

DEBUG = True

CITY_CODE_DICT = {'广州市': '440100', '宜宾市': '511500', '巴彦淖尔盟': '152800', '桂林市': '450300', '安阳市': '410500', '白山市': '220600', '丽水市': '331100', '恩施土家族苗族自治州': '422800', '吉林市': '220200', '肇庆市': '441200', '上海市': '310000', '日喀则市': '540200', '运城市': '140800', '鹤壁市': '410600', '石家庄市': '130100', '安庆市': '340800', '东营市': '370500', '乌海市': '150300', '娄底市': '431300', '玉溪市': '530400', '梅州市': '441400', '湖州市': '330500', '克孜勒苏柯尔克孜自治州': '653000', '齐齐哈尔市': '230200', '铜陵市': '340700', '中山市': '442000', '株洲市': '430200', '重庆市': '500000', '秦皇岛市': '130300', '景德镇市': '360200', '昭通市': '530600', '临夏回族自治州': '622900', '威海市': '371000', '长春市': '220100', '周口市': '411600', '韶关市': '440200', '嘉兴市': '330400', '许昌市': '411000', '安顺市': '520400', '宝鸡市': '610300', '南阳市': '411300', '新乡市': '410700', '庆阳市': '621000', '洛阳市': '410300', '广元市': '510800', '绥化市': '231200', '海东市': '630200', '晋城市': '140500', '资阳市': '512000', '鄂尔多斯市': '150600', '锦州市': '210700', '舟山市': '330900', '营口市': '210800', '济南市': '370100', '丽江市': '530700', '鄂州市': '420700', '潍坊市': '370700', '阳江市': '441700', '巴音郭楞蒙古自治州': '652800', '凉山彝族自治州': '513400', '襄阳市': '420600', '信阳市': '411500', '眉山市': '511400', '平凉市': '620800', '湘潭市': '430300', '荆州市': '421000', '佛山市': '440600', '白城市': '220800', '九江市': '360400', '三明市': '350400', '郑州市': '410100', '东川市': '530200', '鸡西市': '230300', '常州市': '320400', '巢湖市': '341400', '西双版纳傣族自治州': '532800', '柳州市': '450200', '咸宁市': '421200', '合肥市': '340100', '晋中市': '140700', '拉萨市': '540100', '菏泽市': '371700', '长治市': '140400', '濮阳市': '410900', '宜春市': '360900', '驻马店市': '411700', '定西市': '621100', '随州市': '421300', '辽阳市': '211000', '克拉玛依市': '650200', '宿迁市': '321300', '宁波市': '330200', '沈阳市': '210100', '石河子市': '650300', '芜湖市': '340200', '崇左市': '451400', '上饶市': '361100', '德宏傣族景颇族自治州': '533100', '济宁市': '370800', '邯郸市': '130400', '莆田市': '350300', '遂宁市': '510900', '茂名市': '440900', '唐山市': '130200', '邵阳市': '430500', '迪庆藏族自治州': '533400', '清远市': '441800', '佳木斯市': '230800', '忻州市': '140900', '常德市': '430700', '商丘市': '411400', '昆明市': '530100', '抚州市': '361000', '钦州市': '450700', '天水市': '620500', '镇江市': '321100', '鹤岗市': '230400', '昌吉回族自治州': '652300', '大连市': '210200', '辽源市': '220400', '贵阳市': '520100', '毕节市': '520500', '铜仁市': '520600', '焦作市': '410800', '海口市': '460100', '新余市': '360500', '南宁市': '450100', '荆门市': '420800', '滨州市': '371600', '绵阳市': '510700', '甘南藏族自治州': '623000', '无锡市': '320200', '黄南藏族自治州': '632300', '台湾省': '710000', '云浮市': '445300', '阜阳市': '341200', '雅安市': '511800', '三沙市': '460300', '亳州市': '341600', '双鸭山市': '230500', '赣州市': '360700', '天津市': '120000', '通辽市': '150500', '青岛市': '370200', '宿州市': '341300', '湛江市': '440800', '伊犁哈萨克自治州': '654000', '鞍山市': '210300', '黄冈市': '421100', '普洱市': '530800', '达州市': '511700', '临沂市': '371300', '商洛市': '611000', '伊春市': '230700', '福州市': '350100', '成都市': '510100', '攀枝花市': '510400', '铜川市': '610200', '临汾市': '141000', '开封市': '410200', '梧州市': '450400', '中卫市': '640500', '温州市': '330300', '三门峡市': '411200', '百色市': '451000', '泰州市': '321200', '汕头市': '440500', '揭阳市': '445200', '呼伦贝尔市': '150700', '松原市': '220700', '本溪市': '210500', '葫芦岛市': '211400', '兴安盟': '152200', '贺州市': '451100', '南充市': '511300', '曲靖市': '530300', '呼伦贝尔盟': '152100', '徐州市': '320300', '吴忠市': '640300', '张家口市': '130700', '盐城市': '320900', '黑河市': '231100', '永州市': '431100', '承德市': '130800', '岳阳市': '430600', '玉林市': '450900', '衡阳市': '430400', '江门市': '440700', '宜昌市': '420500', '扬州市': '321000', '黔南布依族苗族自治州': '522700', '河池市': '451200', '连云港市': '320700', '武汉市': '420100', '马鞍山市': '340500', '石嘴山市': '640200', '东莞市': '441900', '平顶山市': '410400', '海南藏族自治州': '632500', '张家界市': '430800', '哲里木盟': '152300', '阿坝藏族羌族自治州': '513200', '珠海市': '440400', '滁州市': '341100', '遵义市': '520300', '陇南市': '621200', '朔州市': '140600', '潮州市': '445100', '绍兴市': '330600', '阜新市': '210900', '通化市': '220500', '邢台市': '130500', '内江市': '511000', '安康市': '610900', '德州市': '371400', '盘锦市': '211100', '白银市': '620400', '巴彦淖尔市': '150800', '澳门特别行政区': '820000', '金华市': '330700', '德阳市': '510600', '香港特别行政区': '810000', '淄博市': '370300', '衡水市': '131100', '十堰市': '420300', '北海市': '450500', '贵港市': '450800', '朝阳市': '211300', '沧州市': '130900', '来宾市': '451300', '海北藏族自治州': '632200', '阿拉善盟': '152900', '蚌埠市': '340300', '日照市': '371100', '六盘水市': '520200', '南平市': '350700', '自治区直辖县级行政区划': '659000', '牡丹江市': '231000', '文山壮族苗族自治州': '532600', '吕梁市': '141100', '汉中市': '612300', '酒泉市': '620900', '海南行政区': '442100', '呼和浩特市': '150100', '北京市': '110000', '大庆市': '230600', '西安市': '610100', '南通市': '320600', '台州市': '331000', '大理白族自治州': '532900', '汕尾市': '441500', '锡林郭勒盟': '152500', '昭乌达盟': '152400', '淮南市': '340400', '四平市': '220300', '保定市': '130600', '七台河市': '230900', '杭州市': '330100', '深圳市': '440300', '泉州市': '350500', '怀化市': '431200', '萍乡市': '360300', '鹰潭市': '360600', '湘西土家族苗族自治州': '433100', '龙岩市': '350800', '赤峰市': '150400', '铁岭市': '211200', '乐山市': '511100', '三亚市': '460200', '乌鲁木齐市': '650100', '漯河市': '411100', '吉安市': '360800', '长沙市': '430100', '淮北市': '340600', '宁德市': '350900', '廊坊市': '131000', '太原市': '140100', '泰安市': '370900', '保山市': '530500', '银川市': '640100', '巴中市': '511900', '伊克昭盟': '152700', '渭南市': '610500', '莱芜市': '371200', '孝感市': '420900', '黄山市': '341000', '张掖市': '620700', '延安市': '610600', '西宁市': '630100', '黔西南布依族苗族自治州': '522300', '自贡市': '510300', '金昌市': '620300', '惠州市': '441300', '咸阳市': '610400', '楚雄彝族自治州': '532300', '玉树藏族自治州': '632700', '抚顺市': '210400', '博尔塔拉蒙古自治州': '652700', '广安市': '511600', '固原市': '640400', '兰州市': '620100', '南昌市': '360100', '武威市': '620600', '六安市': '341500', '淮安市': '320800', '衢州市': '330800', '哈尔滨市': '230100', '南京市': '320100', '聊城市': '371500', '果洛藏族自治州': '632600', '榆林市': '610800', '沙市市': '420400', '海西蒙古族藏族自治州': '632800', '大同市': '140200', '防城港市': '450600', '郴州市': '431000', '益阳市': '432300', '乌兰察布盟': '152600', '苏州市': '320500', '怒江傈僳族自治州': '533300', '漳州市': '350600', '乌兰察布市': '150900', '河源市': '441600', '黄石市': '420200', '烟台市': '370600', '甘孜藏族自治州': '513300', '黔东南苗族侗族自治州': '522600', '池州市': '341700', '红河哈尼族彝族自治州': '532500', '嘉峪关市': '620200', '泸州市': '510500', '丹东市': '210600', '阳泉市': '140300', '宣城市': '341800', '枣庄市': '370400', '厦门市': '350200', '临沧市': '530900', '包头市': '150200'}

CODE_CITY_DICT = {'410700': '新乡市', '430500': '邵阳市', '140200': '大同市', '230400': '鹤岗市', '210700': '锦州市', '510100': '成都市', '610200': '铜川市', '510800': '广元市', '340200': '芜湖市', '632200': '海北藏族自治州', '450700': '钦州市', '150200': '包头市', '652400': '伊犁哈萨克自治州', '150900': '乌兰察布市', '430300': '湘潭市', '130100': '石家庄市', '310000': '上海市', '640500': '中卫市', '152400': '昭乌达盟', '430400': '衡阳市', '530100': '昆明市', '441400': '梅州市', '520300': '遵义市', '530300': '曲靖市', '140400': '长治市', '341800': '宣城市', '231200': '绥化市', '152900': '阿拉善盟', '370300': '淄博市', '140900': '忻州市', '361100': '上饶市', '653000': '克孜勒苏柯尔克孜自治州', '341000': '黄山市', '450300': '桂林市', '320900': '盐城市', '420100': '武汉市', '370100': '济南市', '420600': '襄阳市', '710000': '台湾省', '513200': '阿坝藏族羌族自治州', '611000': '商洛市', '440600': '佛山市', '450200': '柳州市', '513400': '凉山彝族自治州', '430100': '长沙市', '330700': '金华市', '340900': '黄山市', '421000': '荆州市', '230600': '大庆市', '533100': '德宏傣族景颇族自治州', '650100': '乌鲁木齐市', '370200': '青岛市', '640100': '银川市', '330300': '温州市', '522300': '黔西南布依族苗族自治州', '341400': '巢湖市', '445300': '云浮市', '230200': '齐齐哈尔市', '411700': '驻马店市', '433100': '湘西土家族苗族自治州', '211300': '朝阳市', '630200': '海东市', '620400': '白银市', '130300': '秦皇岛市', '511600': '广安市', '370400': '枣庄市', '360600': '鹰潭市', '360200': '景德镇市', '432300': '益阳市', '451100': '贺州市', '410500': '安阳市', '610500': '渭南市', '510900': '遂宁市', '321100': '镇江市', '532300': '楚雄彝族自治州', '511500': '宜宾市', '130600': '保定市', '350400': '三明市', '511000': '内江市', '130700': '张家口市', '451200': '河池市', '620500': '天水市', '350200': '厦门市', '340300': '蚌埠市', '411200': '三门峡市', '152300': '哲里木盟', '371000': '威海市', '330600': '绍兴市', '330800': '衢州市', '371200': '莱芜市', '440100': '广州市', '530800': '普洱市', '620300': '金昌市', '330100': '杭州市', '360700': '赣州市', '654000': '伊犁哈萨克自治州', '420200': '黄石市', '140100': '太原市', '511100': '乐山市', '341600': '亳州市', '210600': '丹东市', '410800': '焦作市', '371600': '滨州市', '320700': '连云港市', '370900': '泰安市', '620800': '平凉市', '440400': '珠海市', '350900': '宁德市', '411500': '信阳市', '370500': '东营市', '150700': '呼伦贝尔市', '510300': '自贡市', '371300': '临沂市', '360900': '宜春市', '150600': '鄂尔多斯市', '640200': '石嘴山市', '440800': '湛江市', '411400': '商丘市', '320400': '常州市', '530600': '昭通市', '340400': '淮南市', '610300': '宝鸡市', '420900': '孝感市', '513300': '甘孜藏族自治州', '500000': '重庆市', '230700': '伊春市', '532800': '西双版纳傣族自治州', '420400': '沙市市', '410600': '鹤壁市', '630100': '西宁市', '441300': '惠州市', '431100': '永州市', '430900': '益阳市', '211400': '葫芦岛市', '650200': '克拉玛依市', '450600': '防城港市', '330400': '嘉兴市', '140800': '运城市', '210400': '抚顺市', '230100': '哈尔滨市', '441000': '海口市', '230900': '七台河市', '370800': '济宁市', '820000': '澳门特别行政区', '361000': '抚州市', '152800': '巴彦淖尔盟', '210100': '沈阳市', '411600': '周口市', '210500': '本溪市', '530200': '东川市', '512000': '资阳市', '445200': '揭阳市', '431300': '娄底市', '371400': '德州市', '659000': '自治区直辖县级行政区划', '610400': '咸阳市', '623000': '甘南藏族自治州', '370700': '潍坊市', '231100': '黑河市', '810000': '香港特别行政区', '441800': '清远市', '445100': '潮州市', '632300': '黄南藏族自治州', '652700': '博尔塔拉蒙古自治州', '321200': '泰州市', '130500': '邢台市', '640400': '固原市', '640300': '吴忠市', '130200': '唐山市', '610100': '西安市', '620900': '酒泉市', '621200': '陇南市', '330900': '舟山市', '320800': '淮安市', '360300': '萍乡市', '150100': '呼和浩特市', '350700': '南平市', '421200': '咸宁市', '410300': '洛阳市', '450400': '梧州市', '520600': '铜仁市', '360400': '九江市', '520400': '安顺市', '150400': '赤峰市', '211000': '辽阳市', '520200': '六盘水市', '141100': '吕梁市', '632600': '果洛藏族自治州', '220800': '白城市', '440200': '韶关市', '210800': '营口市', '530500': '保山市', '220700': '松原市', '451300': '来宾市', '421300': '随州市', '321300': '宿迁市', '320600': '南通市', '431200': '怀化市', '450800': '贵港市', '530900': '临沧市', '620200': '嘉峪关市', '350500': '泉州市', '350300': '莆田市', '520500': '毕节市', '350800': '龙岩市', '610700': '汉中市', '410200': '开封市', '411100': '漯河市', '211100': '盘锦市', '370600': '烟台市', '210300': '鞍山市', '632500': '海南藏族自治州', '340600': '淮北市', '532600': '文山壮族苗族自治州', '430600': '岳阳市', '451400': '崇左市', '152600': '乌兰察布盟', '540200': '日喀则市', '120000': '天津市', '220300': '四平市', '532500': '红河哈尼族彝族自治州', '620600': '武威市', '150300': '乌海市', '341700': '池州市', '152200': '兴安盟', '612300': '汉中市', '360100': '南昌市', '441500': '汕尾市', '152700': '伊克昭盟', '621100': '定西市', '442000': '中山市', '320300': '徐州市', '211200': '铁岭市', '460200': '三亚市', '220500': '通化市', '460300': '三沙市', '442100': '海南行政区', '141000': '临汾市', '533300': '怒江傈僳族自治州', '350100': '福州市', '321000': '扬州市', '371700': '菏泽市', '622900': '临夏回族自治州', '411300': '南阳市', '130800': '承德市', '441700': '阳江市', '330200': '宁波市', '320500': '苏州市', '210200': '大连市', '340500': '马鞍山市', '140700': '晋中市', '451000': '百色市', '231000': '牡丹江市', '522700': '黔南布依族苗族自治州', '340100': '合肥市', '420700': '鄂州市', '410400': '平顶山市', '230500': '双鸭山市', '360800': '吉安市', '130400': '邯郸市', '522600': '黔东南苗族侗族自治州', '620100': '兰州市', '331000': '台州市', '621000': '庆阳市', '420800': '荆门市', '341200': '阜阳市', '341100': '滁州市', '230800': '佳木斯市', '320100': '南京市', '150800': '巴彦淖尔市', '520100': '贵阳市', '430700': '常德市', '533400': '迪庆藏族自治州', '371500': '聊城市', '460100': '海口市', '511700': '达州市', '540100': '拉萨市', '420300': '十堰市', '510500': '泸州市', '441600': '河源市', '152100': '呼伦贝尔盟', '421100': '黄冈市', '450900': '玉林市', '632800': '海西蒙古族藏族自治州', '371100': '日照市', '110000': '北京市', '410100': '郑州市', '430800': '张家界市', '610600': '延安市', '441200': '肇庆市', '152500': '锡林郭勒盟', '340800': '安庆市', '140500': '晋城市', '441900': '东莞市', '650300': '石河子市', '610900': '安康市', '511800': '雅安市', '320200': '无锡市', '220400': '辽源市', '440500': '汕头市', '331100': '丽水市', '360500': '新余市', '340700': '铜陵市', '532900': '大理白族自治州', '341300': '宿州市', '130900': '沧州市', '620700': '张掖市', '230300': '鸡西市', '140600': '朔州市', '430200': '株洲市', '410900': '濮阳市', '632700': '玉树藏族自治州', '450500': '北海市', '140300': '阳泉市', '510400': '攀枝花市', '511900': '巴中市', '431000': '郴州市', '440700': '江门市', '511400': '眉山市', '652800': '巴音郭楞蒙古自治州', '420500': '宜昌市', '411000': '许昌市', '652300': '昌吉回族自治州', '440900': '茂名市', '450100': '南宁市', '511300': '南充市', '422800': '恩施土家族苗族自治州', '131100': '衡水市', '341500': '六安市', '440300': '深圳市', '530400': '玉溪市', '220200': '吉林市', '510600': '德阳市', '150500': '通辽市', '350600': '漳州市', '442200': '三亚市', '610800': '榆林市', '530700': '丽江市', '220600': '白山市', '131000': '廊坊市', '330500': '湖州市', '210900': '阜新市', '220100': '长春市', '510700': '绵阳市'}

CATEGORY = {'910': {0: '全部', 101792: '饺子馄饨', 100839: '快餐便当', 100840: '汉堡薯条', 101785: '意面披萨', 101786: '包子粥店', 100842: '米粉面馆', 101615: '麻辣烫冒菜', 101791: '川湘菜', 100841: '地方菜系', 101979: '炸鸡炸串', 100944: '特色小吃', 101790: '夹馍饼类', 101980: '鸭脖卤味', 100843: '日料寿司', 101788: '韩式料理', 100845: '香锅干锅', 101789: '火锅串串', 100844: '龙虾烧烤', 102145: '轻食沙拉', 102463: '暖胃粉丝汤', 102464: '东南亚菜'}}

TABLE_CREATE = '''
    CREATE TABLE IF NOT EXISTS "tbl_meituan_shoplist" (
    "id"  INTEGER PRIMARY KEY AUTOINCREMENT,
    "shop_name"  TEXT,
    "shop_pic"  TEXT,
    "latitude"  TEXT,
    "longitude"  TEXT,
    "address"  TEXT,
    "month_sales"  TEXT,
    "score"  TEXT,
    "type_icon"  TEXT,
    "ship_fee"  TEXT,
    "min_price"  TEXT,
    "average_price"  TEXT,
    "first_category"  TEXT,
    "second_category"  TEXT,
    "third_category"  TEXT,
    "trade_area"  TEXT,
    "ship_time"  TEXT,
    "city_code"  TEXT,
    "city_name"  TEXT,
    "remarks"  TEXT
    );
    '''


def log_instance():
    logger_param = {
        'computername': os.name,
        'appname': APP_NAME
    }
    log_folder = '%s/Log/' % pathlib.Path(sys.argv[0]).parent.parent.__str__()
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_name = log_folder + APP_NAME + '.log'

    return Logger(log_name, **logger_param)


log = log_instance()