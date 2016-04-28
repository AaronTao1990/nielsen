# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import json

class LYSpider(scrapy.Spider):
    name = "ly_gonglue"

    gonglue_api = ('http://go.ly.com/ajax/GetNewRaiderInfo?type=2&pageSize=12&pageindex=%d', 28)
    comment_api = 'http://www.tuniu.com/yii.php?r=trips/notesAjax/getreplylist'

    HEADERS = {
        'Host' : 'go.ly.com',
        'Accept' : '*/*',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
        'Referer' : 'http://go.ly.com/'
    }

    def start_requests(self):
        for page in range(self.gonglue_api[1]):
            yield Request(self.gonglue_api[0] % (page + 1), headers=self.HEADERS, dont_filter=True, callback=self.parse_gonglue)

    def parse_gonglue(self, response):
        selector = Selector(response)
        for gonglue in selector.xpath('//ul[@class="gonglueList clearfix"]/li'):
            title = gonglue.xpath('./a[@class="gonglueNameTit"]/@title').extract_first()
            author = gonglue.xpath('./div[@class="gonglueSource clearfix"]/a[@class="personName"]/@title').extract_first()
            view_count = gonglue.xpath('./div[@class="gonglueSource clearfix"]/span[@class="lookNub"]/text()').extract_first()
            like_count = gonglue.xpath('./div[@class="gonglueSource clearfix"]/span[@class="likeNub"]/text()').extract_first()
            url = gonglue.xpath('./a[@class="gongluePic"]/@href').extract_first()

            result = {
                'title' : title,
                'author' : author,
                'view_count' : view_count,
                'like_count' : like_count,
                'url' : url,
            }
            #self.logger.info('lv gonglue : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
            meta = response.meta.copy()
            meta['result'] = result
            yield Request(url, headers=self.HEADERS, meta=meta, dont_filter=True, callback=self.parse_content)

    def parse_content(self, response):
        selector = Selector(response)
        date = selector.xpath('//span[@id="subtime"]/text()').extract_first().replace(u'发表时间：', '').strip(' \n\r')
        content = ''.join(selector.xpath('//div[@id="content"]/node()').extract())

        result = response.meta['result']
        result['date'] = date
        result['content'] = content
        self.logger.info('lv gonglue : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
