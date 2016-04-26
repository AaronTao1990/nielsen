# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import json

class QunarSpider(scrapy.Spider):
    name = "qunar_gonglue"

    gonglue_api = (
        (u'热门游记', 'http://travel.qunar.com/travelbook/list.htm?page=%d&order=hot_heat', 9999),
        (u'精华游记', 'http://travel.qunar.com/travelbook/list.htm?page=%d&order=elite_ctime', 717),
        (u'行程计划', 'http://travel.qunar.com/travelbook/list.htm?page=%d&order=start_heat', 9999),
    )

    HEADERS = {
        'Host' : 'travel.qunar.com',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def start_requests(self):
        for gonglue_item in self.gonglue_api:
            meta = {}
            meta['main_class'] = gonglue_item[0]
            for page in range(gonglue_item[2]):
                yield Request(gonglue_item[1] % (page + 1), meta=meta, headers=self.HEADERS, dont_filter=True)

    def parse(self, response):
        meta = response.meta
        selector = Selector(response)
        for gonglue in selector.xpath('//ul[@class="b_strategy_list "]/li'):
            view_count = gonglue.xpath('./div[@class="nums"]/span[@class="icon_view"]/text()').extract_first()
            love_count = gonglue.xpath('./div[@class="nums"]/span[@class="icon_love"]/text()').extract_first()
            comment_count = gonglue.xpath('./div[@class="nums"]/span[@class="icon_comment"]/text()').extract_first()
            title = gonglue.xpath('./h2[@class="tit"]/a/text()').extract_first()
            username = gonglue.xpath('./p[@class="user_info"]/span[@class="user_name"]/a/text()').extract_first()
            date = gonglue.xpath('./p[@class="user_info"]/span[@class="date"]/text()').extract_first()
            days = gonglue.xpath('./p[@class="user_info"]/span[@class="days"]/text()').extract_first()
            content = ''.join(gonglue.xpath('./p[@class="places"]/node()').extract())
            result = {
                'main_class' : meta['main_class'],
                'title' : title,
                'view_count' : view_count,
                'love_count' : love_count,
                'comment_count' : comment_count,
                'username' : username,
                'date' : date,
                'days' : days,
                'content' : content
            }
            #self.logger.info('攻略下载 : %s\t%s\t%s' % (name, download_count, meta['mark']))
            self.logger.info('qunar gonglue : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
