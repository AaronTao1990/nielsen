# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
import json


class CitycodeSpider(scrapy.Spider):
    name = "citycode"

    api = 'http://www.dianping.com/citylist/citylist?citypage=1'

    HEADERS = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
        'Host' : 'www.dianping.com',
        'Referer' : 'http://www.dianping.com/citylist',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    def start_requests(self):
        yield Request(self.api, headers=self.HEADERS, callback=self.parse_city_list)

    def parse_city_list(self, response):
        selector = Selector(response)
        for area in selector.xpath('//ul[@id="divArea"]/li'):
            area_name = area.xpath('./strong/text()').extract_first()
            for special_area in area.xpath('./div[@class="terms"]/a'):
                url = 'http://www.dianping.com' + special_area.xpath('./@href').extract_first()
                name = special_area.xpath('./strong/text()').extract_first()
                if not name:
                    name = special_area.xpath('./text()').extract_first()
                city = {
                    'area' : area_name,
                    'url' : url,
                    'name' : name
                }
                self.logger.info('got special spot city : %s' % json.dumps(city, ensure_ascii=False).encode('utf-8'))
                yield Request(url, meta={'city' : city}, headers=self.HEADERS, callback=self.parse_city_code)
            for province in area.xpath('./dl[@class="terms"]'):
                province_name = province.xpath('./dt/text()').extract_first()
                for city in province.xpath('./dd/a'):
                    url = 'http://www.dianping.com' + city.xpath('./@href').extract_first()
                    name = city.xpath('./strong/text()').extract_first()
                    city = {
                        'area' : area_name,
                        'url' : url,
                        'name' : name,
                        'province' : province_name
                    }
                    self.logger.debug('got province city : %s' % json.dumps(city, ensure_ascii=False).encode('utf-8'))
                    yield Request(url, meta={'city' : city}, headers=self.HEADERS, callback=self.parse_city_code)

    def parse_city_code(self, response):
        city = response.meta['city']
        selector = Selector(response)
        city_code = selector.xpath('//input[@id="G_s"]/@data-s-cityid').extract_first()
        city['citycode'] = city_code
        self.logger.info('got city : %s' % json.dumps(city, ensure_ascii=False).encode('utf-8'))
