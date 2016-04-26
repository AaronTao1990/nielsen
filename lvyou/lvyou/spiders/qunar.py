# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import json

class QunarSpider(scrapy.Spider):
    name = "qunar_gonglue"

    gonglue_api = (
        (u'热门游记', 'http://travel.qunar.com/travelbook/list.htm?page=1&order=hot_heat', 9999),
        (u'精华游记', 'http://travel.qunar.com/travelbook/list.htm?page=1&order=elite_ctime', 717),
        (u'行程计划', 'http://travel.qunar.com/travelbook/list.htm?page=1&order=start_heat', 9999)
    )

    def start_requests(self):
        for gonglue_item in self.gonglue_api:
            meta = {}
            meta['main_class'] = gonglue_item[0]
            for page in range(gonglue_item[2]):
            yield Request(gonglue_item[1], meta=meta)

    def parse(self, response):
        meta = response.meta
        selector = Selector(response)
        for gonglue in selector.xpath('//ul[@id="divGuideBookList"]/li'):
            name = gonglue.xpath('./a/@title').extract_first()
            download_count = gonglue.xpath('./span/em/text()').extract_first()
            result = {
                'main_class' : meta['main_class'],
                'second_class' : meta['second_class'],
                'gonglue_name' : name,
                'download_count' : download_count
            }
            #self.logger.info('攻略下载 : %s\t%s\t%s' % (name, download_count, meta['mark']))
            self.logger.info('ctrip gonglue : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))

class CtripYoujiSpider(scrapy.Spider):
    name = "ctrip_youji"

    youji_api = ('http://you.ctrip.com/TravelSite/Home/IndexTravelListHtml?p=%d&Idea=0&Type=1&Plate=0', 500)
    comments_api = ('http://you.ctrip.com/TravelSite/Home/TravelReplyListHtml?TravelId=2903586&IsReplyRefresh=0&ReplyPageNo=5&ReplyPageSize=10&_=1460903593336')

    def start_requests(self):
        url, total_pages = self.youji_api
        for page in range(total_pages):
            yield Request(url % (page+1), callback=self.parse_youji)

    def parse_youji(self, response):
        selector = Selector(response)
        for youji in selector.xpath('//div[@class="city"]'):
            city_name = youji.xpath('./div[@class="city-sub"]/a[@class="city-name"]/text()').extract_first()
            title = youji.xpath('./div[@class="city-sub"]/a[@class="cpt"]/text()').extract_first()
            view_count = youji.xpath('./div[@class="city-sub"]/p[@class="opts"]/i[@class="numview"]/text()').extract_first()
            love_count = youji.xpath('./div[@class="city-sub"]/p[@class="opts"]/i[@class="want"]/text()').extract_first()
            comment_count = youji.xpath('./div[@class="city-sub"]/p[@class="opts"]/i[@class="numreply"]/text()').extract_first()
            meta = {
                'city_name' : city_name,
                'title' : title,
                'view_count' : view_count,
                'love_count' : love_count,
                'comment_count' : comment_count
            }
            print json.dumps(meta, ensure_ascii=False).encode('utf-8')

#class CtripGentuanSpider(scrapy.Spider):
#    name = 'ctrip_gentuan'
#
#    get_dest_key_list_api = 'http://vacations.ctrip.com/grouptravel/'
#    get_dest_list_api = 'http://vacations.ctrip.com/Package-Booking-VacationsOnlineSiteUI/Handler/HotDestKeysNew.ashx?requestType=0&startCity=1&module=indexV2'

