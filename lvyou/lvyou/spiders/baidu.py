# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
import time
from datetime import datetime

class BaiduGonglueSpider(scrapy.Spider):
    name = "baidu_gonglue"

    gonglue_api = 'http://lvyou.baidu.com/destination/ajax/books?format=ajax&pn=%d&rn=16&type=0&keywords=&t=%d'

    HEADERS = {
        'Host' : 'lvyou.baidu.com',
        'X-Requested-With' : 'XMLHttpRequest',
        'Referer' : 'http://lvyou.baidu.com/guide/',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
    }

    def start_requests(self):
        for page in range(27):
            cur_time = int(time.time())
            page = (page+1)*16
            yield Request(self.gonglue_api % (page, cur_time))

    def __seconds_format(self, time_s, format_s='%Y-%m-%d %H:%M:%S'):
        return datetime.fromtimestamp(time_s).strftime(format_s)

    def parse(self, response):
        try:
            data = json.loads(response.body_as_unicode())
        except Exception:
            self.logger.error('invalid result')
            return
        else:
            if data.get('errno') != 0:
                self.logger.error('invalid result')
                return
            for book in data.get('data', {}).get('books_list', []):
                name = book.get('gname')
                date = self.__seconds_format(float(book.get('update_time')))
                download_count = book.get('download_total')
                result = {
                    'name' : name,
                    'date' : date,
                    'download_count' : download_count
                }
                self.logger.info('tripadvisor mudidi : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
