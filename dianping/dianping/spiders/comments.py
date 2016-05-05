# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import Request
from scrapy.selector import Selector

class CommentsSpider(scrapy.Spider):
    name = "comments"

    api = 'http://www.dianping.com/shop/%s/review_more'

    HEADERS = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
        'Host' : 'www.dianping.com',
        'Referer' : 'http://www.dianping.com/citylist',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    def __init__(self, tasks_filename):
        self.tasks = self.__load_tasks(tasks_filename)

    def __load_tasks(self, filename):
        with open(filename, 'r') as f:
            for line in f.readlines():
                yield json.loads(line.strip('\n'))

    def __extract_dianpu_id(self, url):
        return re.search('\d+', url).group()

    def start_requests(self):
        for task in self.tasks:
            url = task['url']
            dianpu_id = self.__extract_dianpu_id(url)
            meta = {
                'task' : task,
                'dianpu_id' : dianpu_id,
                'first_page' : True
            }
            api =  self.api % dianpu_id
            yield Request(api, meta=meta, headers=self.HEADERS,  callback=self.parse_comment)
            #return # only parse one store

    def parse_comment(self, response):
        meta = response.meta
        selector = Selector(response)

        # deal with pages
        if meta.get('first_page'):
            meta['first_page'] = False
            total = selector.xpath('//div[@class="comment-tab"]//li[2]/span/em/text()').extract_first()
            if total:
                total = int(total.strip('()'))
                self.logger.info('got total numbers : %d' % total)
                if total > 20:
                    for page in range(total/20):
                        api = self.api % meta.get('dianpu_id') + ('?pageno=%d' % (page+2))
                        yield Request(api, meta=meta, headers=self.HEADERS, callback=self.parse_comment)
                        #return # only parse one page

        # deal with comments
        for comment in selector.xpath('//div[@class="comment-list"]/ul/li'):
            rating_total = comment.xpath('.//div[@class="user-info"]/span/@title').extract_first()
            rating_kouwei = comment.xpath('.//div[@class="comment-rst"]/span[1]/text()').extract_first()
            rating_huanjing = comment.xpath('.//div[@class="comment-rst"]/span[2]/text()').extract_first()
            rating_fuwu = comment.xpath('.//div[@class="comment-rst"]/span[3]/text()').extract_first()
            comment_content = comment.xpath('.//div[@class="J_brief-cont"]/text()').extract_first()
            if comment_content:
                comment_content = re.sub('\n\s*', '', comment_content)
            date = comment.xpath('.//div[@class="misc-info"]/span[@class="time"]/text()').extract_first()
            result = {
                'rating_total' : rating_total,
                'rating_kouwei' : rating_kouwei,
                'rating_huanjing' : rating_huanjing,
                'rating_fuwu' : rating_fuwu,
                'comment_content' : comment_content,
                'date' : date,
                'task' : meta['task']
            }
            self.logger.info('comment item : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
