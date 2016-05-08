# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import json
import re

class CtripSpider(scrapy.Spider):
    name = "ctrip_gonglue"

    custom_settings = {
        'DOWNLOAD_DELAY' : 0.3
    }

    gonglue_api = (
        (u'中国', u'北京', 'http://you.ctrip.com/guides/g-d1.html#gl'),
        (u'中国', u'上海', 'http://you.ctrip.com/guides/g-d2.html#gl'),
        (u'中国', u'香港', 'http://you.ctrip.com/guides/g-d38.html#gl'),
        (u'中国', u'澳门', 'http://you.ctrip.com/guides/g-d39.html#gl'),
        (u'中国', u'天津', 'http://you.ctrip.com/guides/g-d154.html#gl'),
        (u'中国', u'重庆', 'http://you.ctrip.com/guides/g-d158.html#gl'),
        (u'中国', u'海南', 'http://you.ctrip.com/guides/g-d100001.html#gl'),
        (u'中国', u'西藏', 'http://you.ctrip.com/guides/g-d100003.html#gl'),
        (u'中国', u'云南', 'http://you.ctrip.com/guides/g-d100007.html#gl'),
        (u'中国', u'四川', 'http://you.ctrip.com/guides/g-d100009.html#gl'),
        (u'中国', u'吉林', 'http://you.ctrip.com/guides/g-d100031.html#gl'),
        (u'中国', u'青海', 'http://you.ctrip.com/guides/g-d100032.html#gl'),
        (u'中国', u'福建', 'http://you.ctrip.com/guides/g-d100038.html#gl'),
        (u'中国', u'山东', 'http://you.ctrip.com/guides/g-d100039.html#gl'),
        (u'中国', u'广东', 'http://you.ctrip.com/guides/g-d100051.html#gl'),
        (u'中国', u'广西', 'http://you.ctrip.com/guides/g-d100052.html#gl'),
        (u'中国', u'湖南', 'http://you.ctrip.com/guides/g-d100053.html#gl'),
        (u'中国', u'江西', 'http://you.ctrip.com/guides/g-d100054.html#gl'),
        (u'中国', u'黑龙江', 'http://you.ctrip.com/guides/g-d100055.html#gl'),
        (u'中国', u'山西', 'http://you.ctrip.com/guides/g-d100056.html#gl'),
        (u'中国', u'陕西', 'http://you.ctrip.com/guides/g-d100057.html#gl'),
        (u'中国', u'河南', 'http://you.ctrip.com/guides/g-d100058.html#gl'),
        (u'中国', u'河北', 'http://you.ctrip.com/guides/g-d100059.html#gl'),
        (u'中国', u'甘肃', 'http://you.ctrip.com/guides/g-d100060.html#gl'),
        (u'中国', u'辽宁', 'http://you.ctrip.com/guides/g-d100061.html#gl'),
        (u'中国', u'内蒙古', 'http://you.ctrip.com/guides/g-d100062.html#gl'),
        (u'中国', u'宁夏', 'http://you.ctrip.com/guides/g-d100063.html#gl'),
        (u'中国', u'浙江', 'http://you.ctrip.com/guides/g-d100065.html#gl'),
        (u'中国', u'江苏', 'http://you.ctrip.com/guides/g-d100066.html#gl'),
        (u'中国', u'湖北', 'http://you.ctrip.com/guides/g-d100067.html#gl'),
        (u'中国', u'安徽', 'http://you.ctrip.com/guides/g-d100068.html#gl'),
        (u'中国', u'台湾', 'http://you.ctrip.com/guides/g-d100076.html#gl'),
        (u'亚洲', '', 'http://you.ctrip.com/guides/g1-d120001-p%d.html#gl', 4),
        (u'欧洲', '', 'http://you.ctrip.com/guides/g1-d120002-p%d.html#gl', 2),
        (u'大洋洲', '', 'http://you.ctrip.com/guides/g1-d120003.html#gl'),
        (u'北美洲', '', 'http://you.ctrip.com/guides/g1-d120004.html#gl'),
        (u'南美洲', '', 'http://you.ctrip.com/guides/g1-d120005.html#gl'),
        (u'非洲', '', 'http://you.ctrip.com/guides/g1-d120006.html#gl')
    )

    gonglue = (
        ('http://you.ctrip.com/guides/g-p%d.html#gl', 6, '国内'),
        ('http://you.ctrip.com/guides/g1-p%d.html#gl', 8, '国际')
    )

    def start_requests(self):
        for gonglue_item in self.gonglue_api:
            meta = {}
            meta['main_class'] = gonglue_item[0]
            meta['second_class'] = gonglue_item[1]
            if len(gonglue_item) == 3:
                yield Request(gonglue_item[2], meta = meta)
            elif len(gonglue_item) == 4:
                for i in range(gonglue_item[3]):
                    yield Request(gonglue_item[2] % (i+1), meta=meta)
            else:
                pass

    def parse(self, response):
        meta = response.meta
        selector = Selector(response)
        for gonglue in selector.xpath('//ul[@id="divGuideBookList"]/li'):
            name = gonglue.xpath('./a/@title').extract_first()
            url = 'http://you.ctrip.com' + gonglue.xpath('./a/@href').extract_first()
            date = gonglue.xpath('./span/text()').extract_first().replace(u'更新', ' 00:00:00')
            download_count = gonglue.xpath('./span/em/text()').extract_first()
            result = {
                'main_class' : meta['main_class'],
                'second_class' : meta['second_class'],
                'gonglue_name' : name,
                'download_count' : download_count,
                'date' : date,
                'url' : url
            }
            #self.logger.info('攻略下载 : %s\t%s\t%s' % (name, download_count, meta['mark']))
            self.logger.info('ctrip gonglue : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))

class CtripYoujiSpider(scrapy.Spider):
    name = 'ctrip_youji'

    custom_settings = {
        'DOWNLOAD_DELAY' : 0.3
    }

    youji_api = (
        (u'亚洲', u'日本', u'', u'http://you.ctrip.com/travels/japan100041/t3-p%d.html'),
        (u'亚洲', u'日本', u'东京', u'http://you.ctrip.com/travels/tokyo294/t3-p%d.html'),
        (u'亚洲', u'日本', u'大阪', u'http://you.ctrip.com/travels/osaka293/t3-p%d.html'),
        (u'亚洲', u'日本', u'京都', u'http://you.ctrip.com/travels/kyoto430/t3-p%d.html'),
        (u'亚洲', u'日本', u'北海道', u'http://you.ctrip.com/travels/hokkaido296/t3-p%d.html'),
        (u'亚洲', u'日本', u'冲绳', u'http://you.ctrip.com/travels/okinawa292/t3-p%d.html'),
        (u'亚洲', u'日本', u'九州', u'http://you.ctrip.com/travels/kyushu291/t3-p%d.html'),
        (u'亚洲', u'日本', u'名古屋', u'http://you.ctrip.com/travels/nagoya2127/t3-p%d.html'),
        (u'亚洲', u'韩国', u'', u'http://you.ctrip.com/travels/southkorea100042/t3-p%d.html'),
        (u'亚洲', u'韩国', u'首尔', u'http://you.ctrip.com/travels/seoul234/t3-p%d.html'),
        (u'亚洲', u'韩国', u'济州岛', u'http://you.ctrip.com/travels/jejuisland297/t3-p%d.html'),
        (u'亚洲', u'韩国', u'江原道', u'http://you.ctrip.com/travels/gangwon1185/t3-p%d.html'),
        (u'亚洲', u'韩国', u'釜山', u'http://you.ctrip.com/travels/busan432/t3-p%d.html'),
        (u'亚洲', u'韩国', u'仁川', u'http://you.ctrip.com/travels/incheon1385/t3-p%d.html'),
        (u'亚洲', u'泰国', u'', u'http://you.ctrip.com/travels/thailand100021/t3-p%d.html'),
        (u'亚洲', u'泰国', u'曼谷', u'http://you.ctrip.com/travels/bangkok191/t3-p%d.html'),
        (u'亚洲', u'泰国', u'普吉岛', u'http://you.ctrip.com/travels/phuket364/t3-p%d.html'),
        (u'亚洲', u'泰国', u'清迈', u'http://you.ctrip.com/travels/chiangmai209/t3-p%d.html'),
        (u'亚洲', u'泰国', u'芭堤雅', u'http://you.ctrip.com/travels/pattaya208/t3-p%d.html'),
        (u'亚洲', u'泰国', u'苏梅岛', u'http://you.ctrip.com/travels/kohsamui566/t3-p%d.html'),
        (u'亚洲', u'马来西亚', u'吉隆坡', u'http://you.ctrip.com/travels/kualalumpur45/t3-p%d.html'),
        (u'亚洲', u'马来西亚', u'沙巴', u'http://you.ctrip.com/travels/sabah538/t3-p%d.html'),
        (u'亚洲', u'新加坡', u'', u'http://you.ctrip.com/travels/singapore53/t3-p%d.html'),
        (u'亚洲', u'柬埔寨', u'', u'http://you.ctrip.com/travels/cambodia100081/t3-p%d.html'),
        (u'亚洲', u'柬埔寨', u'暹粒-吴哥窟', u'http://you.ctrip.com/travels/siemreap599/t3-p%d.html'),
        (u'亚洲', u'菲律宾', u'', u'http://you.ctrip.com/travels/philippines100044/t3-p%d.html'),
        (u'亚洲', u'菲律宾', u'长滩岛', u'http://you.ctrip.com/travels/boracay610/t3-p%d.html'),
        (u'亚洲', u'菲律宾', u'薄荷岛', u'http://you.ctrip.com/travels/boholisland1166/t3-p%d.html'),
        (u'亚洲', u'印度尼西亚', u'', u'http://you.ctrip.com/travels/indonesia100045/t3-p%d.html'),
        (u'亚洲', u'印度尼西亚', u'巴厘岛', u'http://you.ctrip.com/travels/bali438/t3-p%d.html'),
        (u'亚洲', u'马尔代夫', u'', u'http://you.ctrip.com/travels/maldives330/t3-p%d.html'),
        (u'亚洲', u'尼泊尔', u'', u'http://you.ctrip.com/travels/nepal100079/t3-p%d.html'),
        (u'亚洲', u'印度', u'', u'http://you.ctrip.com/travels/india100080/t3-p%d.html'),
        (u'亚洲', u'印度', u'德里', u'http://you.ctrip.com/travels/delhi24685/t3-p%d.html'),
        (u'亚洲', u'印度', u'阿格拉', u'http://you.ctrip.com/travels/agra1026/t3-p%d.html'),
        (u'亚洲', u'斯里兰卡', u'', u'http://you.ctrip.com/travels/srilanka100084/t3-p%d.html'),
        (u'亚洲', u'阿联酋', u'', u'http://you.ctrip.com/travels/unitedarademirates100099/t3-p%d.html'),
        (u'亚洲', u'迪拜', u'', u'http://you.ctrip.com/travels/dubai1062/t3-p%d.html'),
        (u'亚洲', u'阿布扎比', u'', u'http://you.ctrip.com/travels/abudhabi1353/t3-p%d.html'),
        (u'亚洲', u'以色列', u'', u'http://you.ctrip.com/travels/israel100074/t3-p%d.html'),
        (u'亚洲', u'以色列', u'耶路撒冷', u'http://you.ctrip.com/travels/jerusalem552/t3-p%d.html'),
        (u'亚洲', u'伊朗', u'', u'http://you.ctrip.com/travels/iran100123/t3-p%d.html'),
        (u'亚洲', u'伊朗', u'德黑兰', u'http://you.ctrip.com/travels/tehran949/t3-p%d.html'),
        (u'亚洲', u'伊朗', u'设拉子', u'http://you.ctrip.com/travels/shiraz24875/t3-p%d.html'),
        (u'亚洲', u'约旦', u'', u'http://you.ctrip.com/travels/jordan100085/t3-p%d.html'),
        (u'亚洲', u'沙特阿拉伯', u'', u'http://you.ctrip.com/travels/saudiarabia100121/t3-p%d.html'),
        (u'欧洲', u'俄罗斯', u'', u'http://you.ctrip.com/travels/russia100083/t3-p%d.html'),
        (u'欧洲', u'俄罗斯', u'圣彼得堡', u'http://you.ctrip.com/travels/stpetersburg359/t3-p%d.html'),
        (u'欧洲', u'俄罗斯', u'莫斯科', u'http://you.ctrip.com/travels/moscow358/t3-p%d.html'),
        (u'欧洲', u'土耳其', u'', u'http://you.ctrip.com/travels/turkey100073/t3-p%d.html'),
        (u'欧洲', u'土耳其', u'伊斯坦布尔', u'http://you.ctrip.com/travels/istanbul258/t3-p%d.html'),
        (u'欧洲', u'英国', u'', u'http://you.ctrip.com/travels/unitedkingdom20354/t3-p%d.html'),
        (u'欧洲', u'英国', u'伦敦', u'http://you.ctrip.com/travels/london309/t3-p%d.html'),
        (u'欧洲', u'英国', u'剑桥', u'http://you.ctrip.com/travels/cambridge721/t3-p%d.html'),
        (u'欧洲', u'英国', u'爱丁堡', u'http://you.ctrip.com/travels/edinburgh389/t3-p%d.html'),
        (u'欧洲', u'英国', u'巴斯', u'http://you.ctrip.com/travels/bath718/t3-p%d.html'),
        (u'欧洲', u'法国', u'', u'http://you.ctrip.com/travels/france100024/t3-p%d.html'),
        (u'欧洲', u'法国', u'巴黎', u'http://you.ctrip.com/travels/paris308/t3-p%d.html'),
        (u'欧洲', u'法国', u'里昂', u'http://you.ctrip.com/travels/lyon391/t3-p%d.html'),
        (u'欧洲', u'法国', u'普罗旺斯', u'http://you.ctrip.com/travels/provence750/t3-p%d.html'),
        (u'欧洲', u'法国', u'戛纳', u'http://you.ctrip.com/travels/cannes715/t3-p%d.html'),
        (u'欧洲', u'法国', u'波尔多', u'http://you.ctrip.com/travels/bordeaux716/t3-p%d.html'),
        (u'欧洲', u'爱尔兰', u'', u'http://you.ctrip.com/travels/ireland100090/t3-p%d.html'),
        (u'欧洲', u'爱尔兰', u'都柏林', u'http://you.ctrip.com/travels/dublin819/t3-p%d.html'),
        (u'欧洲', u'荷兰', u'', u'http://you.ctrip.com/travels/holland100028/t3-p%d.html'),
        (u'欧洲', u'阿姆斯特丹', u'', u'http://you.ctrip.com/travels/amsterdam299/t3-p%d.html'),
        (u'欧洲', u'比利时', u'', u'http://you.ctrip.com/travels/belgium100023/t3-p%d.html'),
        (u'欧洲', u'比利时', u'布鲁塞尔', u'http://you.ctrip.com/travels/brussels298/t3-p%d.html'),
        (u'欧洲', u'卢森堡', u'', u'http://you.ctrip.com/travels/luxemburg300/t3-p%d.html'),
        (u'欧洲', u'意大利', u'', u'http://you.ctrip.com/travels/italy100026/t3-p%d.html'),
        (u'欧洲', u'罗马', u'', u'http://you.ctrip.com/travels/rome303/t3-p%d.html'),
        (u'欧洲', u'意大利', u'威尼斯', u'http://you.ctrip.com/travels/venice340/t3-p%d.html'),
        (u'欧洲', u'意大利', u'佛罗伦萨', u'http://you.ctrip.com/travels/florence341/t3-p%d.html'),
        (u'欧洲', u'米兰', u'', u'http://you.ctrip.com/travels/milan304/t3-p%d.html'),
        (u'欧洲', u'西班牙', u'', u'http://you.ctrip.com/travels/spain100035/t3-p%d.html'),
        (u'欧洲', u'西班牙', u'马德里', u'http://you.ctrip.com/travels/madrid378/t3-p%d.html'),
        (u'欧洲', u'希腊', u'', u'http://you.ctrip.com/travels/greece100036/t3-p%d.html'),
        (u'欧洲', u'希腊', u'圣托里尼岛', u'http://you.ctrip.com/travels/santorini1998/t3-p%d.html'),
        (u'欧洲', u'希腊', u'雅典', u'http://you.ctrip.com/travels/athens382/t3-p%d.html'),
        (u'欧洲', u'葡萄牙', u'', u'http://you.ctrip.com/travels/portugal100106/t3-p%d.html'),
        (u'欧洲', u'葡萄牙', u'里斯本', u'http://you.ctrip.com/travels/lisbon574/t3-p%d.html'),
        (u'欧洲', u'丹麦', u'', u'http://you.ctrip.com/travels/denmark100069/t3-p%d.html'),
        (u'欧洲', u'丹麦', u'哥本哈根', u'http://you.ctrip.com/travels/copenhagen449/t3-p%d.html'),
        (u'欧洲', u'挪威', u'', u'http://you.ctrip.com/travels/norway100098/t3-p%d.html'),
        (u'欧洲', u'挪威', u'奥斯陆', u'http://you.ctrip.com/travels/oslo450/t3-p%d.html'),
        (u'欧洲', u'瑞典', u'', u'http://you.ctrip.com/travels/sweden100097/t3-p%d.html'),
        (u'欧洲', u'瑞典', u'斯德哥尔摩', u'http://you.ctrip.com/travels/stockholm451/t3-p%d.html'),
        (u'欧洲', u'芬兰', u'', u'http://you.ctrip.com/travels/finland100092/t3-p%d.html'),
        (u'欧洲', u'芬兰', u'赫尔辛基', u'http://you.ctrip.com/travels/helsinki452/t3-p%d.html'),
        (u'欧洲', u'冰岛', u'', u'http://you.ctrip.com/travels/iceland100096/t3-p%d.html'),
        (u'欧洲', u'冰岛', u'雷克雅未克', u'http://you.ctrip.com/travels/reykjavik1044/t3-p%d.html'),
        (u'欧洲', u'德国', u'', u'http://you.ctrip.com/travels/germany100025/t3-p%d.html'),
        (u'欧洲', u'德国', u'柏林', u'http://you.ctrip.com/travels/berlin306/t3-p%d.html'),
        (u'欧洲', u'德国', u'慕尼黑', u'http://you.ctrip.com/travels/munich572/t3-p%d.html'),
        (u'欧洲', u'德国', u'法兰克福', u'http://you.ctrip.com/travels/frankfurt305/t3-p%d.html'),
        (u'欧洲', u'德国', u'科隆', u'http://you.ctrip.com/travels/cologne388/t3-p%d.html'),
        (u'欧洲', u'奥地利', u'', u'http://you.ctrip.com/travels/austria100027/t3-p%d.html'),
        (u'欧洲', u'奥地利', u'维也纳', u'http://you.ctrip.com/travels/vienna439/t3-p%d.html'),
        (u'欧洲', u'捷克', u'', u'http://you.ctrip.com/travels/theczechrepublic100094/t3-p%d.html'),
        (u'欧洲', u'捷克', u'布拉格', u'http://you.ctrip.com/travels/prague822/t3-p%d.html'),
        (u'欧洲', u'捷克', u'克鲁姆洛夫', u'http://you.ctrip.com/travels/ceskykrumlov8532/t3-p%d.html'),
        (u'欧洲', u'瑞士', u'', u'http://you.ctrip.com/travels/switzerland100050/t3-p%d.html'),
        (u'欧洲', u'瑞士', u'琉森', u'http://you.ctrip.com/travels/lucerne644/t3-p%d.html'),
        (u'欧洲', u'瑞士', u'苏黎世', u'http://you.ctrip.com/travels/zurich301/t3-p%d.html'),
        (u'欧洲', u'匈牙利', u'', u'http://you.ctrip.com/travels/hungary100101/t3-p%d.html'),
        (u'欧洲', u'匈牙利', u'布达佩斯', u'http://you.ctrip.com/travels/budapest1109/t3-p%d.html'),
        (u'欧洲', u'波兰', u'', u'http://you.ctrip.com/travels/poland100118/t3-p%d.html'),
        (u'欧洲', u'波兰', u'华沙', u'http://you.ctrip.com/travels/warsaw1261/t3-p%d.html'),
        (u'北美洲', u'美国', u'纽约', u'http://you.ctrip.com/travels/newyork248/t3-p%d.html'),
        (u'北美洲', u'美国', u'洛杉矶', u'http://you.ctrip.com/travels/losangeles250/t3-p%d.html'),
        (u'北美洲', u'美国', u'旧金山', u'http://you.ctrip.com/travels/sanfrancisco249/t3-p%d.html'),
        (u'北美洲', u'美国', u'夏威夷', u'http://you.ctrip.com/travels/hawaii251/t3-p%d.html'),
        (u'北美洲', u'美国', u'拉斯维加斯', u'http://you.ctrip.com/travels/lasvegas252/t3-p%d.html'),
        (u'北美洲', u'美国', u'华盛顿', u'http://you.ctrip.com/travels/washingtondc257/t3-p%d.html'),
        (u'北美洲', u'美国', u'西雅图', u'http://you.ctrip.com/travels/seattle253/t3-p%d.html'),
        (u'北美洲', u'美国', u'波士顿', u'http://you.ctrip.com/travels/boston442/t3-p%d.html'),
        (u'北美洲', u'美国', u'芝加哥', u'http://you.ctrip.com/travels/chicago254/t3-p%d.html'),
        (u'北美洲', u'美国', u'佛罗里达', u'http://you.ctrip.com/travels/florida941/t3-p%d.html'),
        (u'北美洲', u'美国', u'迈阿密', u'http://you.ctrip.com/travels/miami1920/t3-p%d.html'),
        (u'北美洲', u'美国', u'黄石国家公园', u'http://you.ctrip.com/travels/yellowstonenationalpark120415/t3-p%d.html'),
        (u'北美洲', u'加拿大', u'温哥华', u'http://you.ctrip.com/travels/vancouver354/t3-p%d.html'),
        (u'北美洲', u'加拿大', u'多伦多', u'http://you.ctrip.com/travels/toronto355/t3-p%d.html'),
        (u'北美洲', u'加拿大', u'蒙特利尔', u'http://you.ctrip.com/travels/montreal661/t3-p%d.html'),
        (u'北美洲', u'加拿大', u'维多利亚', u'http://you.ctrip.com/travels/victoria357/t3-p%d.html'),
        (u'北美洲', u'加拿大', u'班夫', u'http://you.ctrip.com/travels/banffnationalpark2045/t3-p%d.html'),
        (u'北美洲', u'加拿大', u'魁北克市', u'http://you.ctrip.com/travels/quebeccity1405/t3-p%d.html'),
        (u'北美洲', u'古巴', u'', u'http://you.ctrip.com/travels/cuba100113/t3-p%d.html'),
        (u'北美洲', u'墨西哥', u'', u'http://you.ctrip.com/travels/mexico100108/t3-p%d.html'),
        (u'大洋洲', u'澳大利亚', u'悉尼', u'http://you.ctrip.com/travels/sydney236/t3-p%d.html'),
        (u'大洋洲', u'澳大利亚', u'黄金海岸', u'http://you.ctrip.com/travels/goldcoast456/t3-p%d.html'),
        (u'大洋洲', u'澳大利亚', u'墨尔本', u'http://you.ctrip.com/travels/melbourne312/t3-p%d.html'),
        (u'大洋洲', u'澳大利亚', u'阿德莱德', u'http://you.ctrip.com/travels/adelaide626/t3-p%d.html'),
        (u'大洋洲', u'澳大利亚', u'凯恩斯', u'http://you.ctrip.com/travels/cairns453/t3-p%d.html'),
        (u'大洋洲', u'新西兰', u'奥克兰', u'http://you.ctrip.com/travels/auckland320/t3-p%d.html'),
        (u'大洋洲', u'新西兰', u'罗托鲁瓦', u'http://you.ctrip.com/travels/rorotua682/t3-p%d.html'),
        (u'大洋洲', u'新西兰', u'基督城', u'http://you.ctrip.com/travels/christchurch695/t3-p%d.html'),
        (u'大洋洲', u'新西兰', u'皇后镇', u'http://you.ctrip.com/travels/queenstown684/t3-p%d.html'),
        (u'大洋洲', u'新西兰', u'但尼丁', u'http://you.ctrip.com/travels/dunedin1192/t3-p%d.html'),
        (u'大洋洲', u'斐济', u'', u'http://you.ctrip.com/travels/fiji100102/t3-p%d.html'),
        (u'大洋洲', u'大溪地', u'', u'http://you.ctrip.com/travels/tahiti1354/t3-p%d.html'),
        (u'南美洲', u'巴西', u'', u'http://you.ctrip.com/travels/brazil100109/t3-p%d.html'),
        (u'南美洲', u'阿根廷', u'', u'http://you.ctrip.com/travels/argentina100111/t3-p%d.html'),
        (u'南美洲', u'秘鲁', u'', u'http://you.ctrip.com/travels/peru100112/t3-p%d.html'),
        (u'南美洲', u'智利', u'', u'http://you.ctrip.com/travels/chile100110/t3-p%d.html'),
        (u'非洲', u'埃及', u'', u'http://you.ctrip.com/travels/egypt100030/t3-p%d.html'),
        (u'非洲', u'摩洛哥', u'', u'http://you.ctrip.com/travels/morocco100132/t3-p%d.html'),
        (u'非洲', u'肯尼亚', u'', u'http://you.ctrip.com/travels/kenya100087/t3-p%d.html'),
        (u'非洲', u'南非', u'', u'http://you.ctrip.com/travels/southafrica100049/t3-p%d.html'),
        (u'非洲', u'塞舌尔', u'', u'http://you.ctrip.com/travels/seychelles100153/t3-p%d.html'),
        (u'非洲', u'毛里求斯', u'', u'http://you.ctrip.com/travels/mauritius444/t3-p%d.html'),
        (u'南极洲', u'南极', u'', u'http://you.ctrip.com/travels/antarctica120487/t3-p%d.html'),
    )


    HEADERS = {
        'Accept:' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }

    def start_requests(self):
        for api in self.youji_api:
            meta = {
                'main_class' : api[0],
                'second_class' : api[1],
                'third_class' : api[2],
                'api' : api[3],
                'first_page' : True
            }
            url = api[3] % 1
            yield Request(url, meta=meta, headers=self.HEADERS, callback=self.parse_list)

    def parse_list(self, response):
        meta = response.meta
        selector = Selector(response)

        # deal with pages
        if meta['first_page']:
            meta['first_page'] = False

            pages = selector.xpath('//b[@class="numpage"]/text()').extract_first()
            if pages:
                self.logger.info('pages : %s' % pages)
                for page in range(int(pages)-1):
                    yield Request(meta['api'] % (page+2), meta=meta, headers=self.HEADERS, callback=self.parse_list)

        for youji in selector.xpath('//a[@class="journal-item cf"]'):
            url = 'http://you.ctrip.com' + youji.xpath('./@href').extract_first()
            title = youji.xpath('.//dt[@class="ellipsis"]/text()').extract_first()
            author_info = youji.xpath('.//dd[@class="item-user"]/text()').extract_first()
            author_info_match = re.match(u'^(?P<author>.*?)发表于(?P<date>.*?)$',
                                         author_info,
                                         re.DOTALL)
            if not author_info_match:
                self.logger.info('invalid author info')
                continue
            author_info_data = author_info_match.groupdict()
            author = author_info_data.get('author')
            date = author_info_data.get('date')
            date = date.strip(' \r\n') + ' 00:00:00'
            view_count = youji.xpath('.//i[@class="numview"]/text()').extract_first()
            wan_d = view_count.find(u'万')
            if wan_d != -1:
                view_count = str(float(view_count[:wan_d]) * 10000)
            like_count = youji.xpath('.//i[@class="want"]/text()').extract_first()
            comment_count = youji.xpath('.//i[@class="numreply"]/text()').extract_first()
            result = {
                'main_class' : meta['main_class'],
                'second_class' : meta['second_class'],
                'third_class' : meta['third_class'],
                'url' : url,
                'title' : title,
                'author' : author,
                'date' : date,
                'view_count' : view_count,
                'like_count' : like_count,
                'comment_count' : comment_count
            }
            self.logger.info('ctrip youji : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))



