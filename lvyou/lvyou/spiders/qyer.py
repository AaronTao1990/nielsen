# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from utils.htmlutils import remove_tags
import json
import re

class QyerQYSpider(scrapy.Spider):
    name = 'qyer_qiongyou'

    jinlang_api = (
        (u' 亚洲', u'亚洲专题', u'http://guide.qyer.com/taste-of-south-east-asia/', u'吃东南亚'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/bangkok/', u'曼谷'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/chiang-mai/', u'清迈'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/phuket/', u'普吉岛'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/ko-samui-and-ko-tao/', u'苏梅岛与涛岛'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/chiang-mai-cafe/', u'清迈咖啡馆'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/taste-of-thailand/', u'泰国美食'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/krabi-and-ko-lanta/', u'甲米与兰塔岛'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/ayutthaya-and-kanchanaburi/', u'大城与北碧'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/sukhothai/', u'素可泰'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/hua-hin/', u'华欣'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/pai/', u'拜县'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/chiang-rai/', u'清莱'),
        (u' 亚洲', u'泰国', u'http://guide.qyer.com/pattaya-and-ko-samet-and-ko-chang/', u'芭堤雅、沙美岛与象岛'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/hong-kong/', u'香港'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/macau/', u'澳门'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/taipei/', u'台北'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/cycling-in-taiwan/', u'骑行台湾'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/eastern-taiwan/', u'台湾东部'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/taste-of-hong-kong/', u'香港美食'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/tainan/', u'台南'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/shopping-in-hk/', u'香港购物'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/taste-of-taiwan/', u'台湾美食'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/kaohsiung/', u'高雄'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/offshore-islands/', u'台湾离岛'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/kenting/', u'垦丁'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/taste-of-macau/', u'澳门美食'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/hong-kong-disneyland/', u'香港迪士尼乐园'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/taiwan/', u'台湾'),
        (u' 亚洲', u'港澳台', u'http://guide.qyer.com/hong-kong-offshore-islands-trekking/', u'香港离岛徒步'),
        (u' 亚洲', u'柬埔寨', u'http://guide.qyer.com/angkor-wat/', u'吴哥窟'),
        (u' 亚洲', u'柬埔寨', u'http://guide.qyer.com/phnom-penh/', u'金边'),
        (u' 亚洲', u'柬埔寨', u'http://guide.qyer.com/cambodia%27s-south-coast/', u'柬埔寨南部海岸'),
        (u' 亚洲', u'不丹', u'http://guide.qyer.com/bhutan/', u'不丹'),
        (u' 亚洲', u'菲律宾', u'http://guide.qyer.com/boracay/', u'长滩岛'),
        (u' 亚洲', u'菲律宾', u'http://guide.qyer.com/bohol/', u'薄荷岛'),
        (u' 亚洲', u'印度尼西亚', u'http://guide.qyer.com/bali/', u'巴厘岛'),
        (u' 亚洲', u'印度尼西亚', u'http://guide.qyer.com/lombok/', u'龙目岛'),
        (u' 亚洲', u'印度尼西亚', u'http://guide.qyer.com/jakarta/', u'雅加达'),
        (u' 亚洲', u'印度尼西亚', u'http://guide.qyer.com/surabaya/', u'泗水'),
        (u' 亚洲', u'印度尼西亚', u'http://guide.qyer.com/yogyakarta/', u'日惹'),
        (u' 亚洲', u'阿联酋', u'http://guide.qyer.com/dubai/', u'迪拜'),
        (u' 亚洲', u'阿联酋', u'http://guide.qyer.com/abu-dhabi/', u'阿布扎比'),
        (u' 亚洲', u'尼泊尔', u'http://guide.qyer.com/kathmandu/', u'加德满都'),
        (u' 亚洲', u'尼泊尔', u'http://guide.qyer.com/pokhara/', u'博卡拉'),
        (u' 亚洲', u'尼泊尔', u'http://guide.qyer.com/everest-trekking/', u'尼泊尔珠峰地区徒步'),
        (u' 亚洲', u'尼泊尔', u'http://guide.qyer.com/annapurna-trekking/', u'安娜普尔纳地区徒步'),
        (u' 亚洲', u'越南', u'http://guide.qyer.com/hanoi/', u'河内'),
        (u' 亚洲', u'越南', u'http://guide.qyer.com/ho-chi-minh-city/', u'胡志明市'),
        (u' 亚洲', u'越南', u'http://guide.qyer.com/mui-ne/', u'美奈'),
        (u' 亚洲', u'越南', u'http://guide.qyer.com/da-lat/', u'大叻'),
        (u' 亚洲', u'越南', u'http://guide.qyer.com/hoi-an/', u'会安'),
        (u' 亚洲', u'越南', u'http://guide.qyer.com/nha-trang/', u'芽庄'),
        (u' 亚洲', u'越南', u'http://guide.qyer.com/ha-long-bay/', u'下龙湾'),
        (u' 亚洲', u'越南', u'http://guide.qyer.com/hue/', u'顺化'),
        (u' 亚洲', u'越南', u'http://guide.qyer.com/da-nang/', u'岘港'),
        (u' 亚洲', u'巴基斯坦', u'http://guide.qyer.com/islamabad/', u'伊斯兰堡'),
        (u' 亚洲', u'马来西亚', u'http://guide.qyer.com/kuala-lumpur/', u'吉隆坡'),
        (u' 亚洲', u'马来西亚', u'http://guide.qyer.com/sabah/', u'沙巴'),
        (u' 亚洲', u'马来西亚', u'http://guide.qyer.com/malacca/', u'马六甲'),
        (u' 亚洲', u'马来西亚', u'http://guide.qyer.com/redang/', u'热浪岛'),
        (u' 亚洲', u'马来西亚', u'http://guide.qyer.com/penang/', u'槟城'),
        (u' 亚洲', u'马来西亚', u'http://guide.qyer.com/langkawi/', u'兰卡威'),
        (u' 亚洲', u'马来西亚', u'http://guide.qyer.com/sarawak/', u'沙捞越'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/kyoto/', u'京都'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/tokyo/', u'东京'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/osaka-and-nagoya/', u'大阪与名古屋'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/hokkaido/', u'北海道'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/taste-of-tokyo/', u'东京美食'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/japanese-architecture/', u'日本建筑'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/tokyo-acg/', u'东京动漫'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/okinawa/', u'冲绳'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/around-tokyo/', u'东京周边'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/taste-of-japan/', u'日本美食'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/nikko/', u'日光'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/ogasawara-and-izu-islands/', u'小笠原与伊豆群岛'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/taste-of-hokkaido/', u'北海道美食'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/nara-and-uji/', u'奈良与宇治'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/skiing-hokkaido/', u'北海道滑雪'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/museums-in-tokyo/', u'东京博物馆'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/taste-of-tohoku-and-north-kanto/', u'日本东北及北关东美食'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/aomori/', u'青森'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/seto-naikai/', u'濑户内海'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/hokkaido-onsen/', u'北海道温泉'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/kobe/', u'神户'),
        (u' 亚洲', u'日本', u'http://guide.qyer.com/hokkaido-railway/', u'北海道铁路'),
        (u' 亚洲', u'老挝', u'http://guide.qyer.com/luang-prabang/', u'琅勃拉邦'),
        (u' 亚洲', u'老挝', u'http://guide.qyer.com/northern-laos/', u'老挝北部'),
        (u' 亚洲', u'印度', u'http://guide.qyer.com/mumbai/', u'孟买'),
        (u' 亚洲', u'印度', u'http://guide.qyer.com/varanasi/', u'瓦拉纳西'),
        (u' 亚洲', u'印度', u'http://guide.qyer.com/jaipur/', u'斋普尔'),
        (u' 亚洲', u'印度', u'http://guide.qyer.com/delhi/', u'德里'),
        (u' 亚洲', u'印度', u'http://guide.qyer.com/darjeeling/', u'大吉岭'),
        (u' 亚洲', u'印度', u'http://guide.qyer.com/taj-mahal-agra/', u'泰姬陵-阿格拉'),
        (u' 亚洲', u'印度', u'http://guide.qyer.com/jaisalmer/', u'杰伊瑟尔梅尔'),
        (u' 亚洲', u'新加坡', u'http://guide.qyer.com/singapore/', u'新加坡'),
        (u' 亚洲', u'新加坡', u'http://guide.qyer.com/taste-of-singapore/', u'新加坡美食'),
        (u' 亚洲', u'新加坡', u'http://guide.qyer.com/shopping-in-singapore/', u'新加坡购物'),
        (u' 亚洲', u'马尔代夫', u'http://guide.qyer.com/maldives/', u'马尔代夫'),
        (u' 亚洲', u'马尔代夫', u'http://guide.qyer.com/maldives-hotels/', u'马尔代夫酒店'),
        (u' 亚洲', u'韩国', u'http://guide.qyer.com/jeju/', u'济州岛'),
        (u' 亚洲', u'韩国', u'http://guide.qyer.com/seoul/', u'首尔'),
        (u' 亚洲', u'韩国', u'http://guide.qyer.com/shopping-in-seoul/', u'首尔购物'),
        (u' 亚洲', u'韩国', u'http://guide.qyer.com/taste-of-seoul/', u'首尔美食'),
        (u' 亚洲', u'韩国', u'http://guide.qyer.com/busan/', u'釜山'),
        (u' 亚洲', u'韩国', u'http://guide.qyer.com/incheon/', u'仁川'),
        (u' 亚洲', u'韩国', u'http://guide.qyer.com/gyeongju/', u'庆州'),
        (u' 亚洲', u'缅甸', u'http://guide.qyer.com/bagan/', u'蒲甘'),
        (u' 亚洲', u'缅甸', u'http://guide.qyer.com/yangon/', u'仰光'),
        (u' 亚洲', u'缅甸', u'http://guide.qyer.com/mandalay/', u'曼德勒'),
        (u' 亚洲', u'斯里兰卡', u'http://guide.qyer.com/sri-lanka/', u'斯里兰卡'),
        (u' 亚洲', u'伊朗', u'http://guide.qyer.com/iran/', u'伊朗'),
        (u' 亚洲', u'黎巴嫩', u'http://guide.qyer.com/lebanon/', u'黎巴嫩'),
        (u' 亚洲', u'以色列', u'http://guide.qyer.com/tel-aviv/', u'特拉维夫'),
        (u' 亚洲', u'文莱', u'http://guide.qyer.com/brunei/', u'文莱'),
        (u' 亚洲', u'朝鲜', u'http://guide.qyer.com/north-korea/', u'朝鲜'),
        (u'欧洲', u'欧洲专题', u'http://guide.qyer.com/europe-railway/', u'欧洲铁路'),
        (u'欧洲', u'欧洲专题', u'http://guide.qyer.com/europe/', u'第一次去欧洲'),
        (u'欧洲', u'欧洲专题', u'http://guide.qyer.com/uefa-euro-2016/', u'2016欧洲杯'),
        (u'欧洲', u'荷兰', u'http://guide.qyer.com/amsterdam/', u'阿姆斯特丹'),
        (u'欧洲', u'荷兰', u'http://guide.qyer.com/amsterdam-airport-schiphol/', u'阿姆斯特丹史基浦机场'),
        (u'欧洲', u'荷兰', u'http://guide.qyer.com/netherlands/', u'荷兰'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/paris/', u'巴黎'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/avignon-provence/', u'阿维尼翁-普罗旺斯'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/shopping-in-paris/', u'巴黎购物'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/marseille/', u'马赛'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/paris-sweet/', u'巴黎甜品'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/taste-of-france/', u'法国美食'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/driving-in-france/', u'法国自驾'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/lyon/', u'里昂'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/normandy-and-brittany/', u'诺曼底与布列塔尼'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/cote-d-azur/', u'南法蔚蓝海岸'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/vin-de-france/', u'法国葡萄酒'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/loire-valley/', u'卢瓦尔河谷'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/france/', u'法国'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/skiing-french-alps/', u'法国阿尔卑斯滑雪'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/french-alps/', u'法国阿尔卑斯'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/brittany-north-coast/', u'布列塔尼北海岸'),
        (u'欧洲', u'法国', u'http://guide.qyer.com/brittany-south-coast/', u'布列塔尼南海岸'),
        (u'欧洲', u'西班牙', u'http://guide.qyer.com/barcelona/', u'巴塞罗那'),
        (u'欧洲', u'西班牙', u'http://guide.qyer.com/madrid/', u'马德里'),
        (u'欧洲', u'西班牙', u'http://guide.qyer.com/seville/', u'塞维利亚'),
        (u'欧洲', u'西班牙', u'http://guide.qyer.com/andalusia/', u'安达卢西亚'),
        (u'欧洲', u'西班牙', u'http://guide.qyer.com/valencia/', u'瓦伦西亚'),
        (u'欧洲', u'西班牙', u'http://guide.qyer.com/taste-of-barcelona/', u'巴塞罗那美食'),
        (u'欧洲', u'西班牙', u'http://guide.qyer.com/madrid-football/', u'马德里球迷指南'),
        (u'欧洲', u'西班牙', u'http://guide.qyer.com/fc-barcelona/', u'巴萨球迷指南'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/munich/', u'慕尼黑'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/hamburg/', u'汉堡'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/heidelberg/', u'海德堡'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/berlin/', u'柏林'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/cologne/', u'科隆'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/bavarian-towns/', u'巴伐利亚小镇'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/frankfurt/', u'法兰克福'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/driving-in-germany/', u'德国自驾'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/germany/', u'德国'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/germany-football/', u'德国足球'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/german-alps/', u'德国阿尔卑斯'),
        (u'欧洲', u'德国', u'http://guide.qyer.com/nuremberg/', u'纽伦堡'),
        (u'欧洲', u'波兰', u'http://guide.qyer.com/euro-2012-poland/', u'2012欧洲杯-波兰'),
        (u'欧洲', u'波兰', u'http://guide.qyer.com/krakow/', u'克拉科夫'),
        (u'欧洲', u'乌克兰', u'http://guide.qyer.com/ukraine/', u'乌克兰'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/rome/', u'罗马'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/florence/', u'佛罗伦萨'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/tuscany/', u'托斯卡纳'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/venice/', u'威尼斯'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/milan/', u'米兰'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/italian-architecture/', u'意大利建筑'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/bologna/', u'博洛尼亚'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/outlets-in-italy/', u'意大利奥特莱斯'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/italy-railway/', u'意大利铁路'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/taste-of-italy/', u'意大利美食'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/cinque-terre/', u'五渔村'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/italy/', u'意大利'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/naples/', u'那不勒斯'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/italy-football/', u'意大利足球'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/italian-wine/', u'意大利葡萄酒'),
        (u'欧洲', u'意大利', u'http://guide.qyer.com/sicily/', u'西西里岛'),
        (u'欧洲', u'土耳其', u'http://guide.qyer.com/istanbul/', u'伊斯坦布尔'),
        (u'欧洲', u'土耳其', u'http://guide.qyer.com/cappadocia/', u'卡帕多西亚'),
        (u'欧洲', u'土耳其', u'http://guide.qyer.com/taste-of-turkey/', u'土耳其美食'),
        (u'欧洲', u'土耳其', u'http://guide.qyer.com/turkey/', u'土耳其'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/london/', u'伦敦'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/lake-district/', u'英国湖区'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/around-london/', u'伦敦周边'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/edinburgh/', u'爱丁堡'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/scotland-and-northern-ireland/', u'苏格兰与北爱尔兰'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/premier-league/', u'英格兰足球超级联赛'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/muggles%27guide/', u'《哈利·波特》影迷指南'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/shopping-in-london/', u'伦敦购物'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/uk-railway/', u'英国铁路'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/manchester/', u'曼彻斯特'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/york/', u'约克'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/birmingham/', u'伯明翰'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/cotswolds/', u'科茨沃尔德'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/uk-castles-and-stately-homes/', u'英国古堡与庄园'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/museums-in-london/', u'伦敦博物馆'),
        (u'欧洲', u'英国', u'http://guide.qyer.com/northern-england/', u'北英格兰'),
        (u'欧洲', u'瑞士', u'http://guide.qyer.com/zurich/', u'苏黎世'),
        (u'欧洲', u'瑞士', u'http://guide.qyer.com/lake-leman/', u'莱芒湖'),
        (u'欧洲', u'瑞士', u'http://guide.qyer.com/switzerland/', u'瑞士'),
        (u'欧洲', u'葡萄牙', u'http://guide.qyer.com/lisbon/', u'里斯本'),
        (u'欧洲', u'葡萄牙', u'http://guide.qyer.com/porto/', u'波尔图'),
        (u'欧洲', u'挪威', u'http://guide.qyer.com/norwegian-fjords/', u'挪威峡湾'),
        (u'欧洲', u'挪威', u'http://guide.qyer.com/oslo/', u'奥斯陆'),
        (u'欧洲', u'捷克', u'http://guide.qyer.com/prague/', u'布拉格'),
        (u'欧洲', u'捷克', u'http://guide.qyer.com/czechic-towns/', u'捷克小镇'),
        (u'欧洲', u'希腊', u'http://guide.qyer.com/santorini/', u'圣托里尼岛'),
        (u'欧洲', u'希腊', u'http://guide.qyer.com/athens/', u'雅典'),
        (u'欧洲', u'瑞典', u'http://guide.qyer.com/stockholm/', u'斯德哥尔摩'),
        (u'欧洲', u'奥地利', u'http://guide.qyer.com/vienna/', u'维也纳'),
        (u'欧洲', u'奥地利', u'http://guide.qyer.com/salzburg/', u'萨尔茨堡'),
        (u'欧洲', u'比利时', u'http://guide.qyer.com/belgium/', u'比利时'),
        (u'欧洲', u'匈牙利', u'http://guide.qyer.com/budapest/', u'布达佩斯'),
        (u'欧洲', u'爱尔兰', u'http://guide.qyer.com/dublin/', u'都柏林'),
        (u'欧洲', u'爱尔兰', u'http://guide.qyer.com/ireland/', u'爱尔兰'),
        (u'欧洲', u'马耳他', u'http://guide.qyer.com/malta/', u'马耳他'),
        (u'欧洲', u'丹麦', u'http://guide.qyer.com/copenhagen/', u'哥本哈根'),
        (u'欧洲', u'丹麦', u'http://guide.qyer.com/funen-odense/', u'安徒生故乡 菲英岛 欧登塞'),
        (u'欧洲', u'俄罗斯', u'http://guide.qyer.com/saint-petersburg/', u'圣彼得堡'),
        (u'欧洲', u'俄罗斯', u'http://guide.qyer.com/moscow/', u'莫斯科'),
        (u'欧洲', u'俄罗斯', u'http://guide.qyer.com/kamchatka/', u'堪察加半岛'),
        (u'欧洲', u'俄罗斯', u'http://guide.qyer.com/trans-siberian-railway/', u'西伯利亚铁路'),
        (u'欧洲', u'俄罗斯', u'http://guide.qyer.com/lake-baikal/', u'贝加尔湖'),
        (u'欧洲', u'芬兰', u'http://guide.qyer.com/helsinki/', u'赫尔辛基'),
        (u'欧洲', u'卢森堡', u'http://guide.qyer.com/luxembourg/', u'卢森堡'),
        (u'欧洲', u'塞尔维亚', u'http://guide.qyer.com/belgrade/', u'贝尔格莱德'),
        (u'欧洲', u'冰岛', u'http://guide.qyer.com/iceland/', u'冰岛'),
        (u'北美洲', u'北美洲专题', u'http://guide.qyer.com/driving-in-the-usa/', u'美国自驾'),
        (u'北美洲', u'北美洲专题', u'http://guide.qyer.com/route-66/', u'美国66号公路'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/washington-d-c/', u'华盛顿'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/new-york/', u'纽约'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/los-angeles/', u'洛杉矶'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/miami/', u'迈阿密'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/south-florida/', u'南佛罗里达'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/yellowstone/', u'黄石国家公园'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/boston/', u'波士顿'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/las-vegas/', u'拉斯维加斯'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/orlando/', u'奥兰多'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/chicago/', u'芝加哥'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/san-francisco/', u'旧金山'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/seattle/', u'西雅图'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/philadelphia/', u'费城'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/museums-in-washington%2Cd.c/', u'华盛顿博物馆'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/yosemite-national-park/', u'优胜美地国家公园'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/museums-in-nyc/', u'纽约博物馆'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/pacific-crest-trail/', u'太平洋山脊小径'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/taste-of-nyc/', u'纽约美食'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/san-diego/', u'圣迭戈'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/new-mexico/', u'新墨西哥州'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/grand-canyon-national-park/', u'大峡谷国家公园'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/mesa-verde-national-park/', u'梅萨维德国家公园'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/arches-and-canyonlands-national-parks/', u'拱门与峡谷地国家公园'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/zion-national-park/', u'锡安国家公园'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/orange-county/', u'橙县'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/bryce-canyon-and-capitol-reef-national-parks/', u'布莱斯峡谷与圆顶礁国家公园'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/hawaii/', u'夏威夷'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/michigan/', u'密歇根州'),
        (u'北美洲', u'美国', u'http://guide.qyer.com/sequoia-and-kings-canyon-national-parks/', u'红杉与国王峡谷国家公园'),
        (u'北美洲', u'加拿大', u'http://guide.qyer.com/toronto/', u'多伦多'),
        (u'北美洲', u'加拿大', u'http://guide.qyer.com/vancouver/', u'温哥华'),
        (u'北美洲', u'加拿大', u'http://guide.qyer.com/montreal/', u'蒙特利尔'),
        (u'北美洲', u'加拿大', u'http://guide.qyer.com/banff-and-jasper-national-parks/', u'班夫与贾斯珀国家公园'),
        (u'北美洲', u'加拿大', u'http://guide.qyer.com/edmonton/', u'埃德蒙顿'),
        (u'北美洲', u'加拿大', u'http://guide.qyer.com/calgary/', u'卡尔加里'),
        (u'北美洲', u'加拿大', u'http://guide.qyer.com/ottawa/', u'渥太华'),
        (u'北美洲', u'古巴', u'http://guide.qyer.com/havana/', u'哈瓦那'),
        (u'北美洲', u'墨西哥', u'http://guide.qyer.com/mexico-city/', u'墨西哥城'),
        (u'北美洲', u'哥斯达黎加', u'http://guide.qyer.com/costa-rica/', u'哥斯达黎加'),
        (u'南美洲', u'巴西', u'http://guide.qyer.com/rio-de-janeiro/', u'里约热内卢'),
        (u'南美洲', u'巴西', u'http://guide.qyer.com/sao-paulo/', u'圣保罗'),
        (u'南美洲', u'巴西', u'http://guide.qyer.com/foz-do-iguacu/', u'巴西伊瓜苏'),
        (u'南美洲', u'巴西', u'http://guide.qyer.com/amazonia-brasileira/', u'巴西亚马逊'),
        (u'南美洲', u'巴西', u'http://guide.qyer.com/salvador/', u'萨尔瓦多'),
        (u'南美洲', u'秘鲁', u'http://guide.qyer.com/machu-picchu-and-cuzco/', u'马丘比丘与库斯科'),
        (u'南美洲', u'阿根廷', u'http://guide.qyer.com/buenos-aires/', u'布宜诺斯艾利斯'),
        (u'南美洲', u'阿根廷', u'http://guide.qyer.com/puerto-iguazu/', u'阿根廷伊瓜苏'),
        (u'南美洲', u'玻利维亚', u'http://guide.qyer.com/bolivia/', u'玻利维亚'),
        (u'南美洲', u'智利', u'http://guide.qyer.com/santiago/', u'圣地亚哥'),
        (u'南美洲', u'智利', u'http://guide.qyer.com/torres-del-paine-national-park/', u'百内国家公园'),
        (u'南美洲', u'智利', u'http://guide.qyer.com/valparaiso-and-vina-del-mar/', u'瓦尔帕莱索与比尼亚德尔马'),
        (u'南美洲', u'智利', u'http://guide.qyer.com/isla-de-pascua/', u'复活节岛'),
        (u'南美洲', u'厄瓜多尔', u'http://guide.qyer.com/galapagos-islands/', u'加拉帕戈斯群岛'),
        (u'南美洲', u'哥伦比亚', u'http://guide.qyer.com/colombia/', u'哥伦比亚'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/sydney/', u'悉尼'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/melbourne/', u'墨尔本'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/gold-coast/', u'澳大利亚黄金海岸'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/tasmania/', u'塔斯马尼亚'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/great-ocean-road/', u'大洋路'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/perth/', u'珀斯'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/northern-territory/', u'北领地'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/canberra/', u'堪培拉'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/adelaide/', u'阿德莱德'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/brisbane/', u'布里斯班'),
        (u'大洋洲', u'澳大利亚', u'http://guide.qyer.com/great-barrier-reef/', u'大堡礁'),
        (u'大洋洲', u'新西兰', u'http://guide.qyer.com/driving-in-nz/', u'新西兰自驾'),
        (u'大洋洲', u'新西兰', u'http://guide.qyer.com/queenstown/', u'皇后镇'),
        (u'大洋洲', u'新西兰', u'http://guide.qyer.com/cycling-in-nz/', u'骑行新西兰'),
        (u'大洋洲', u'新西兰', u'http://guide.qyer.com/auckland/', u'奥克兰'),
        (u'大洋洲', u'新西兰', u'http://guide.qyer.com/south-island/', u'新西兰南岛'),
        (u'大洋洲', u'新西兰', u'http://guide.qyer.com/wildlife-in-nz/', u'新西兰动物之旅'),
        (u'大洋洲', u'新西兰', u'http://guide.qyer.com/new-zealand-trekking/', u'新西兰徒步'),
        (u'大洋洲', u'新西兰', u'http://guide.qyer.com/christchurch/', u'基督城'),
        (u'大洋洲', u'帕劳', u'http://guide.qyer.com/palau/', u'帕劳'),
        (u'大洋洲', u'关岛', u'http://guide.qyer.com/guam/', u'关岛'),
        (u'大洋洲', u'斐济', u'http://guide.qyer.com/fiji/', u'斐济'),
        (u'非洲', u'埃及', u'http://guide.qyer.com/cairo/', u'开罗'),
        (u'非洲', u'埃及', u'http://guide.qyer.com/egypt/', u'埃及'),
        (u'非洲', u'留尼汪', u'http://guide.qyer.com/reunion/', u'法属留尼汪岛'),
        (u'非洲', u'南非', u'http://guide.qyer.com/cape-town/', u'开普敦'),
        (u'非洲', u'南非', u'http://guide.qyer.com/rovos-rail/', u'非洲之傲列车'),
        (u'非洲', u'塞舌尔', u'http://guide.qyer.com/seychelles/', u'塞舌尔'),
        (u'南极洲', u'南极', u'http://guide.qyer.com/ushuaia-to-antarctica/', u'乌斯怀亚到南极'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/cruises/', u'邮轮'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/packing-list/', u'出行装备'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/plug-the-world/', u'旅行插座汇总'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/jetstar-airways/', u'捷星航空'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/travel-health/', u'旅行健康'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/for-girls/', u'单身女孩上路'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/travel-photography/', u'旅行摄影'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/global-blue/', u'环球蓝联退税'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/frozen-zone/', u'严寒地带生存'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/travel-with-parents/', u'带父母旅行'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/for-beginners/', u'第一次出境旅行'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/unionpay-in-southeast-asia/', u'东南亚银联'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/american-express-global-travel-card/', u'美国运通电子旅行支票'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/airasia/', u'亚洲航空'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/the-global-blue-card/', u'环球蓝联卡'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/airbnb/', u'Airbnb旅居指南'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/travel-with-baby/', u'带孩子旅行(0-3岁)'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/travel-skin-care/', u'旅行护肤指南'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/language-travel/', u'海外游学'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/travel-by-bike/', u'自行车旅行'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/global-marathon/', u'环球马拉松'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/travel-with-dji/', u'大疆航拍旅行'),
        (u'南极洲', u'专题', u'http://guide.qyer.com/king-power/', u'泰国王权免税店购物指南'),
    )


    qiongyour_api = ('http://guide.qyer.com/index.php', 17)

    POST_HEADERS = {
        'Host' : 'guide.qyer.com',
        'Accept' : 'application/json, text/javascript, */*; q=0.01',
        'Origin' : 'http://guide.qyer.com',
        'X-Requested-With' : 'XMLHttpRequest',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Referer' : 'http://guide.qyer.com/',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def start_requests(self):
        for api in self.jinlang_api:
            meta = {
                'main_class' : api[0],
                'second_class' : api[1],
                'url' : api[2],
                'title' : api[3],
            }
            yield Request(api[2], meta=meta, callback=self.parse_detail)

    #def start_requests(self):
    #    for page in range(self.qiongyour_api[1]):
    #        formdata = {
    #            'action' : 'ajaxgpage',
    #            'page' : str(page+1),
    #            'overway' : ''
    #        }
    #        yield FormRequest(self.qiongyour_api[0], formdata=formdata, headers=self.POST_HEADERS, callback=self.parse_qiongyou)

    #def parse_qiongyou(self, response):
    #    try:
    #        data = json.loads(response.body_as_unicode())
    #    except Exception:
    #        self.logger.error('invalid result for url : %s' % response.url)
    #        return
    #    else:
    #        if data.get('error_code') != 0:
    #            self.logger.error('invalid result for url : %s' % response.url)
    #            return
    #        html = data.get('data')
    #        selector = Selector(text=html)
    #        for qiongyou in selector.xpath('//li[@class="gui_jnlist_item"]'):
    #            url = qiongyou.xpath('./p[@class="gui_jnlist_item_tit"]/a/@href').extract_first()
    #            yield Request(url, meta={'url':url}, callback=self.parse_detail)

    def parse_detail(self, response):
        meta=response.meta
        selector = Selector(response)
        data_str = ''.join(selector.xpath('//div[@class="gui_info_text"]/node()').extract())
        match_result = re.match(u'^.*名称：</span>(?P<name>.*)<br.*?所属分类：</span>(?P<category>.*?)<br.*?更新时间：</span>(?P<date>.*?)<br.*?下载次数：</span><em class="number">(?P<download_count>.*?)</em.*$', data_str, re.DOTALL)
        if not match_result:
            self.logger.error('invalid result')
            return
        data = match_result.groupdict()
        name = data.get('name')
        date = data.get('date') + ' 00:00:00'
        download_count = data.get('download_count')

        if not name or not date or not download_count:
            self.logger.error('invalid result')
            return
        result = {
            'name' : name,
            'date' : date,
            'download_count' : download_count,
            'url' : response.meta['url'],
            'main_class' : meta['main_class'],
            'second_class' : meta['second_class'],
        }
        self.logger.info('qyer qiongyou : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))


class QyerBBSSpider(scrapy.Spider):
    name = 'qyer_bbs'

    custom_settings = {
        'DOWNLOAD_TIMEOUT' : 10,
        'DOWNLOAD_DELAY' : 0.3
    }

    bbs_api = (
        (u'欧洲', u'环游欧洲', u'http://bbs.qyer.com/forum-112-1-1-%d.html?#gotonav'),
        (u'欧洲', u'法国/摩纳哥', u'http://bbs.qyer.com/forum-14-1-%d.html?#gotonav'),
        (u'欧洲', u'德国', u'http://bbs.qyer.com/forum-12-1-%d.html?#gotonav'),
        (u'欧洲', u'瑞士/列支敦士登', u'http://bbs.qyer.com/forum-15-1-%d.html?#gotonav'),
        (u'欧洲', u'奥地利', u'http://bbs.qyer.com/forum-19-1-%d.html?#gotonav'),
        (u'欧洲', u'捷克/斯洛伐克/匈牙利', u'http://bbs.qyer.com/forum-24-1-%d.html?#gotonav'),
        (u'欧洲', u'西班牙/葡萄牙/安道尔', u'http://bbs.qyer.com/forum-18-1-%d.html?#gotonav'),
        (u'欧洲', u'希腊/塞浦路斯', u'http://bbs.qyer.com/forum-26-1-%d.html?#gotonav'),
        (u'欧洲', u'意大利/梵蒂冈/圣马力诺/马耳他', u'http://bbs.qyer.com/forum-13-1-%d.html?#gotonav'),
        (u'欧洲', u'英国/爱尔兰', u'http://bbs.qyer.com/forum-16-1-%d.html?#gotonav'),
        (u'欧洲', u'荷兰/比利时/卢森堡', u'http://bbs.qyer.com/forum-17-1-%d.html?#gotonav'),
        (u'欧洲', u'波兰/立陶宛/拉脱维亚/爱沙尼亚', u'http://bbs.qyer.com/forum-161-1-%d.html?#gotonav'),
        (u'欧洲', u'挪威/瑞典/芬兰/丹麦/冰岛', u'http://bbs.qyer.com/forum-25-1-%d.html?#gotonav'),
        (u'欧洲', u'俄罗斯/乌克兰/白俄罗斯', u'http://bbs.qyer.com/forum-158-1-%d.html?#gotonav'),
        (u'欧洲', u'外高加索三国', u'http://bbs.qyer.com/forum-160-1-%d.html?#gotonav'),
        (u'欧洲', u'土耳其', u'http://bbs.qyer.com/forum-162-1-%d.html?#gotonav'),
        (u'欧洲', u'东南欧地区', u'http://bbs.qyer.com/forum-159-1-%d.html?#gotonav'),
        (u'美洲', u'美国', u'http://bbs.qyer.com/forum-53-1-%d.html?#gotonav'),
        (u'美洲', u'加拿大', u'http://bbs.qyer.com/forum-54-1-%d.html?#gotonav'),
        (u'美洲', u'中美', u'http://bbs.qyer.com/forum-168-1-%d.html?#gotonav'),
        (u'美洲', u'南美/南极', u'http://bbs.qyer.com/forum-55-1-%d.html?#gotonav'),
        (u'大洋洲', u'澳大利亚', u'http://bbs.qyer.com/forum-56-1-%d.html?#gotonav'),
        (u'大洋洲', u'新西兰', u'http://bbs.qyer.com/forum-83-1-%d.html?#gotonav'),
        (u'大洋洲', u'太平洋海岛', u'http://bbs.qyer.com/forum-178-1-%d.html?#gotonav'),
        (u'非洲', u'北非', u'http://bbs.qyer.com/forum-86-1-%d.html?#gotonav'),
        (u'非洲', u'东非', u'http://bbs.qyer.com/forum-173-1-%d.html?#gotonav'),
        (u'非洲', u'非洲海岛', u'http://bbs.qyer.com/forum-174-1-%d.html?#gotonav'),
        (u'非洲', u'非洲其他', u'http://bbs.qyer.com/forum-60-1-%d.html?#gotonav'),
        (u'亚洲', u'环游亚洲', u'http://bbs.qyer.com/forum-58-1-%d.html?#gotonav'),
        (u'亚洲', u'日本', u'http://bbs.qyer.com/forum-57-1-%d.html?#gotonav'),
        (u'亚洲', u'韩国/朝鲜', u'http://bbs.qyer.com/forum-156-1-%d.html?#gotonav'),
        (u'亚洲', u'台湾', u'http://bbs.qyer.com/forum-52-1-%d.html?#gotonav'),
        (u'亚洲', u'香港/澳门', u'http://bbs.qyer.com/forum-163-1-%d.html?#gotonav'),
        (u'亚洲', u'泰国', u'http://bbs.qyer.com/forum-106-1-%d.html?#gotonav'),
        (u'亚洲', u'马来西亚/文莱', u'http://bbs.qyer.com/forum-108-1-%d.html?#gotonav'),
        (u'亚洲', u'新加坡', u'http://bbs.qyer.com/forum-164-1-%d.html?#gotonav'),
        (u'亚洲', u'菲律宾', u'http://bbs.qyer.com/forum-110-1-%d.html?#gotonav'),
        (u'亚洲', u'柬埔寨', u'http://bbs.qyer.com/forum-175-1-%d.html?#gotonav'),
        (u'亚洲', u'越南', u'http://bbs.qyer.com/forum-107-1-%d.html?#gotonav'),
        (u'亚洲', u'老挝', u'http://bbs.qyer.com/forum-176-1-%d.html?#gotonav'),
        (u'亚洲', u'缅甸', u'http://bbs.qyer.com/forum-177-1-%d.html?#gotonav'),
        (u'亚洲', u'尼泊尔', u'http://bbs.qyer.com/forum-102-1-%d.html?#gotonav'),
        (u'亚洲', u'不丹', u'http://bbs.qyer.com/forum-166-1-%d.html?#gotonav'),
        (u'亚洲', u'印度尼西亚/东帝汶', u'http://bbs.qyer.com/forum-111-1-%d.html?#gotonav'),
        (u'亚洲', u'马尔代夫', u'http://bbs.qyer.com/forum-104-1-%d.html?#gotonav'),
        (u'亚洲', u'斯里兰卡', u'http://bbs.qyer.com/forum-165-1-%d.html?#gotonav'),
        (u'亚洲', u'印度/孟加拉', u'http://bbs.qyer.com/forum-103-1-%d.html?#gotonav'),
        (u'亚洲', u'伊朗', u'http://bbs.qyer.com/forum-59-1-%d.html?#gotonav'),
        (u'亚洲', u'巴基斯坦/阿富汗', u'http://bbs.qyer.com/forum-169-1-%d.html?#gotonav'),
        (u'亚洲', u'阿联酋/卡塔尔', u'http://bbs.qyer.com/forum-171-1-%d.html?#gotonav'),
        (u'亚洲', u'以色列', u'http://bbs.qyer.com/forum-170-1-%d.html?#gotonav'),
        (u'亚洲', u'西亚及其他', u'http://bbs.qyer.com/forum-172-1-%d.html?#gotonav'),
        (u'亚洲', u'中亚各国', u'http://bbs.qyer.com/forum-105-1-%d.html?#gotonav'),
        (u'亚洲', u'蒙古', u'http://bbs.qyer.com/forum-167-1-%d.html?#gotonav'),
        (u'亚洲', u'中国内地', u'http://bbs.qyer.com/forum-51-1-%d.html?#gotonav'),
    )


    HEADERS = {
        'Host' : 'bbs.qyer.com',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def start_requests(self):
        for gonglue_item in self.bbs_api:
            meta = {}
            meta['main_class'] = gonglue_item[0]
            meta['second_class'] = gonglue_item[1]
            meta['api'] = gonglue_item[2]
            meta['list_first_page'] = True
            yield Request(gonglue_item[2] % 1, meta=meta, headers=self.HEADERS, dont_filter=True, callback=self.parse_list)

    def parse_list(self, response):
        meta = response.meta.copy()
        selector = Selector(response)
        for tiezi in selector.xpath('//ul[@id="list-id"]/li'):
            title = tiezi.xpath('.//dt[@class="title fontYaHei"]/a[@class="txt"]/text()').extract_first()
            author = tiezi.xpath('.//dd[@class="data"]/a[1]/text()').extract_first()
            date = tiezi.xpath('.//dd[@class="data"]/span[@class="date"]/text()').extract_first()
            view_count = tiezi.xpath('.//dd[@class="data"]/span[@class="poi"]/text()').extract_first()
            comment_count = tiezi.xpath('.//dd[@class="data"]/span[@class="reply"]/text()').extract_first()
            like_count = tiezi.xpath('.//dd[@class="data"]/span[@class="like"]/text()').extract_first()
            url = tiezi.xpath('.//dt[@class="title fontYaHei"]/a[@class="txt"]/@href').extract_first()

            self.logger.debug('title : %s, author : %s, date : %s, url : %s' % (title, author, date, url))
            if not title or not author or not date or not url:
                continue
            date += ' 00:00:00'
            data = {
                'host' : 'qyer',
                'main_class' : meta['main_class'],
                'second_class' : meta['second_class'],
                'title' : title,
                'author' : author,
                'date' : date,
                'view_count' : view_count,
                'comment_count' : comment_count,
                'like_count' : like_count,
                'url' : url
            }
            pages = int(like_count)/15 + 1
            self.logger.info('comment pages : %s' % pages)
            for page in range(pages):
                api = url.replace('-1.html', '-%d.html' % (page+1))
                yield Request(api, meta={'data':data, 'page' : page+1}, headers=self.HEADERS, dont_filter=True, callback=self.parse_content)

        # deal with pages
        pages = selector.xpath('//div[@class="ui_page"]/a[last()-1]/@data-page').extract_first()
        self.logger.info('list pages : %s' % pages)
        if not pages:
            pages = 1
            del meta['list_first_page']
            for page in range(int(pages)-1):
                yield Request(meta['api'] % (page+2), meta=meta, headers=self.HEADERS, callback=self.parse_list)

    def parse_content(self, response):
        data = response.meta['data']
        selector = Selector(response)
        replies = []
        for post in selector.xpath('//div[@class="bbs_detail_list"]/div[@class="bbs_detail_item"]'):
            date = post.xpath('./div[@class="bbs_detail_title clearfix"]/p[@class="texts"]/text()').extract_first()
            content = ''.join(post.xpath('./div[@class="bbs_detail_content"]/node()').extract())
            author = post.xpath('./div[@class="bbs_detail_title clearfix"]/h3[@class="titles"]/a/text()').extract_first()
            floor = post.xpath('./div[@class="bbs_detail_title clearfix"]/a[last()]/text()').extract_first()
            if not date or not content or not floor:
                continue
            date = date.replace(u'发表于 ', '') + ':00'
            floor = str(int(floor.replace(u'楼', '')) -1)
            content = remove_tags(content)
            content = re.sub(r'\s*\n\s*', '', content)
            replies.append({
                'date' : date,
                'content' : remove_tags(content).replace('\r\n', ''),
                'author' : author,
                'floor' : floor
            })

            result = data.copy()
            result.update({
                'content' : content,
                'floor' : floor,
            })
            if floor == '0':
                self.logger.info('qyer bbs: %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
            else:
                result.update({
                    'view_count' : 0,
                    'comment_count' : 0,
                    'like_count' : 0
                })
                self.logger.info('qyer bbs: %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
