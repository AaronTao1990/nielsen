# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import json

class CtripSpider(scrapy.Spider):
    name = "ctrip_gonglue"

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

#class CtripYoujiSpider(scrapy.Spider):
#    name = "ctrip_youji"
#
#    youji_api = ('http://you.ctrip.com/TravelSite/Home/IndexTravelListHtml?p=%d&Idea=0&Type=1&Plate=0', 500)
#    comments_api = ('http://you.ctrip.com/TravelSite/Home/TravelReplyListHtml?TravelId=2903586&IsReplyRefresh=0&ReplyPageNo=5&ReplyPageSize=10&_=1460903593336')
#
#    def start_requests(self):
#        url, total_pages = self.youji_api
#        for page in range(total_pages):
#            yield Request(url % (page+1), callback=self.parse_youji)
#
#    def parse_youji(self, response):
#        selector = Selector(response)
#        for youji in selector.xpath('//div[@class="city"]'):
#            city_name = youji.xpath('./div[@class="city-sub"]/a[@class="city-name"]/text()').extract_first()
#            title = youji.xpath('./div[@class="city-sub"]/a[@class="cpt"]/text()').extract_first()
#            view_count = youji.xpath('./div[@class="city-sub"]/p[@class="opts"]/i[@class="numview"]/text()').extract_first()
#            love_count = youji.xpath('./div[@class="city-sub"]/p[@class="opts"]/i[@class="want"]/text()').extract_first()
#            comment_count = youji.xpath('./div[@class="city-sub"]/p[@class="opts"]/i[@class="numreply"]/text()').extract_first()
#            meta = {
#                'city_name' : city_name,
#                'title' : title,
#                'view_count' : view_count,
#                'love_count' : love_count,
#                'comment_count' : comment_count
#            }
#            print json.dumps(meta, ensure_ascii=False).encode('utf-8')
#
