# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
from scrapy.selector import Selector
from utils.htmlutils import remove_tags
from utils.proxymanager import ProxyManager

class FixSpider(scrapy.Spider):
    name = "fix"

    HEADERS = {
        'Host' : 'travel.qunar.com',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    #good_proxys = {}

    #def check_proxy(self):
    #    self.logger.info('proxys size : %d' % len(self.good_proxys))
    #    def get_new_ips():
    #        ips = []
    #        api = 'http://api.zdaye.com/?api=201605051157596943&pw=123&checktime=1%D0%A1%CA%B1%C4%DA&gb=2'
    #        resp = fetch_html(api)
    #        try:
    #            for line in resp.split('\n'):
    #                ips.append('http://' + line)
    #            return ips
    #        except Exception:
    #            return ips
    #    for i in range(5):
    #        if len(self.good_proxys) < 30:
    #            ips = get_new_ips()
    #            for ip in ips:
    #                if ip in self.good_proxys.keys():
    #                    continue
    #                else:
    #                    self.good_proxys[ip] = 0
    #        else:
    #            break

    #def get_proxy(self):
    #    self.check_proxy()
    #    for i in range(30):
    #        proxy = random.choice(self.good_proxys.keys())
    #        if self.good_proxys[proxy] < -3:
    #            del self.good_proxys[proxy]
    #        else:
    #            return proxy

    def __init__(self, filename):
        self.filename=filename
        #self.requests = self.gen_requests()

    def load_tasks(self, filename):
        with open(filename, 'r') as f:
            for line in f.readlines():
                if not line:
                    continue
                try:
                    yield json.loads(line.strip('\n'))
                except Exception:
                    continue

    #def gen_requests(self):
    #    requests = []
    #    for task in self.load_tasks(self.filename):
    #        meta = {'task' : task}
    #        meta['task'] = task
    #        requests.append(Request(task['url'], meta=meta, headers=self.HEADERS, callback=self.get_content))
    #    return requests

    def start_requests(self):
        for task in self.load_tasks(self.filename):
            meta = {'task' : task}
            #meta['proxy'] = self.get_proxy()
            meta['task'] = task
            yield Request(task['url'], meta=meta, headers=self.HEADERS, callback=self.get_content)

    def get_content(self, response):
        meta = response.meta
        task = response.meta['task']
        selector = Selector(response)

        try:
            forward = ''.join(selector.xpath('//div[@id="b_foreword"]/node()').extract())
            scheduler = ''.join(selector.xpath('//div[@id="b_panel_schedule"]/node()').extract())
            content = remove_tags(forward+scheduler)
            if not content or len(content) == 0:
                content = remove_tags(''.join(selector.xpath('//div[@class="b_schedule"]/node()').extract()))
            if not content or len(content) ==0:
                self.good_proxys[meta['proxy']] -= 1
                self.logger.info('failed task : %s' % json.dumps(task, ensure_ascii=False).encode('utf-8'))
            else:
                self.good_proxys[meta['proxy']] += 1
                self.logger.info('success task : %s' % json.dumps(task, ensure_ascii=False).encode('utf-8'))
                task['content'] = content
                self.logger.info('success task result : %s' % json.dumps(task, ensure_ascii=False).encode('utf-8'))
        except Exception:
            self.logger.info('failed task : %s' % json.dumps(task, ensure_ascii=False).encode('utf-8'))



