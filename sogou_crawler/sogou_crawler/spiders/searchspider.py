# -*- coding: utf-8 -*-
import scrapy
from sogou_crawler.dao.keywords_dao import KeywordsDao
from scrapy.selector import Selector
from utils.htmlutils import remove_tags
import json

class BaseSpider(scrapy.Spider):

    HEADERS = {
        'Host' : 'travel.qunar.com',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def __init__(self):
        self.keywords_dao = KeywordsDao()
        self.failed_times = {}

    def check_result(self, response, snuid):
        if 'antispider' in response.url or 'http://pb.sogou.com/pv.gif?uigs_productid=weixin&type=article&status=fail' in response.body:
            self.keywords_dao.remove_snuid(snuid)

    def save_doc(self, url, response):
        raise NotImplementedError()

    def failed_proxy(self, proxy):
        if proxy not in self.failed_times.keys():
            self.failed_times[proxy] = 0
        self.failed_times[proxy] += 1
        if self.failed_times.get('proxy', 0) > 10:
            self.keywords_dao.remove_proxy(proxy)

class QunarSpider(BaseSpider):
    name = 'qunar'
    custom_settings = {
        'SCHEDULER' : 'sogou_crawler.scheduler.NielsenScheduler',
    }

    def __init__(self):
        super(QunarSpider, self).__init__()

    def save_doc(self, url, response):
        pass

    def parse_api(self, response):
        task = response.meta['task']
        selector = Selector(response)

        try:
            forward = ''.join(selector.xpath('//div[@id="b_foreword"]/node()').extract())
            scheduler = ''.join(selector.xpath('//div[@id="b_panel_schedule"]/node()').extract())
            content = remove_tags(forward+scheduler)
            if not content or len(content) == 0:
                content = remove_tags(''.join(selector.xpath('//div[@class="b_schedule"]/node()').extract()))
            if not content or len(content) ==0:
                self.logger.info('failed task : %s' % json.dumps(task, ensure_ascii=False).encode('utf-8'))
            else:
                self.logger.info('success task : %s' % json.dumps(task, ensure_ascii=False).encode('utf-8'))
                task['content'] = content
                self.logger.info('success task result : %s' % json.dumps(task, ensure_ascii=False).encode('utf-8'))
                self.keywords_dao.remove_task(response.meta['task_str'])
        except Exception:
            self.logger.info('failed task : %s' % json.dumps(task, ensure_ascii=False).encode('utf-8'))


