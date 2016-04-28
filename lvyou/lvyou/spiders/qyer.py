# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
import json
import re

class QyerQYSpider(scrapy.Spider):
    name = 'qyer_qiongyou'

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
        for page in range(self.qiongyour_api[1]):
            formdata = {
                'action' : 'ajaxgpage',
                'page' : str(page+1),
                'overway' : ''
            }
            yield FormRequest(self.qiongyour_api[0], formdata=formdata, headers=self.POST_HEADERS, callback=self.parse_qiongyou)

    def parse_qiongyou(self, response):
        try:
            data = json.loads(response.body_as_unicode())
        except Exception:
            self.logger.error('invalid result for url : %s' % response.url)
            return
        else:
            if data.get('error_code') != 0:
                self.logger.error('invalid result for url : %s' % response.url)
                return
            html = data.get('data')
            selector = Selector(text=html)
            for qiongyou in selector.xpath('//li[@class="gui_jnlist_item"]'):
                url = qiongyou.xpath('./p[@class="gui_jnlist_item_tit"]/a/@href').extract_first()
                yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        selector = Selector(response)
        data_str = ''.join(selector.xpath('//div[@class="gui_info_text"]/node()').extract())
        match_result = re.match(u'^.*名称：</span>(?P<name>.*)<br.*?所属分类：</span>(?P<category>.*?)<br.*?更新时间：</span>(?P<date>.*?)<br.*?下载次数：</span><em class="number">(?P<download_count>.*?)</em.*$', data_str, re.DOTALL)
        if not match_result:
            self.logger.error('invalid result')
            return
        data = match_result.groupdict()
        name = data.get('name')
        date = data.get('date')
        download_count = data.get('download_count')

        if not name or not date or not download_count:
            self.logger.error('invalid result')
            return
        result = {
            'name' : name,
            'date' : date,
            'download_count' : download_count
        }
        self.logger.info('qyer qiongyou : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))


