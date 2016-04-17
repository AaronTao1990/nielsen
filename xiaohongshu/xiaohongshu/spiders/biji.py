# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
import time

class BijiSpider(scrapy.Spider):
    name = "biji"

    APIS = (
        ('护肤', '56fbfae8d2c8a56ae333afd2', 'http://www.xiaohongshu.com/api/discovery/list2?&_r=%d&start=%s&num=40&oid=category.52ce1c02b4c4d649b58b892c'),
        ('彩妆', '56fbe0da14de41480de0154c', 'http://www.xiaohongshu.com/api/discovery/list2?&_r=%d&start=%s&num=40&oid=category.52ce1c02b4c4d649b58b8930')
    )

    API_GET_COMMENTS = 'http://www.xiaohongshu.com/api/discovery/get_comment?&_r=%d&discovery_id=%s'


    HEADERS = {
        'Host' : 'www.xiaohongshu.com',
        'Accept' : 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With' : 'XMLHttpRequest',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def __get_current_time(self):
        return int(time.time()*1000)

    def start_requests(self):
        for api in self.APIS:
            meta = {
                'source' : api[0],
                'api' : api[2]
            }
            headers = self.HEADERS.update({'Referer':'http://www.xiaohongshu.com/discovery/recommend'})
            yield Request(url=api[2] % (self.__get_current_time(), api[1]), meta=meta, headers=headers)

    def parse(self, response):
        meta = response.meta
        try:
            data = json.loads(response.body_as_unicode())
        except Exception, e:
            self.logger.error('invalid result : %s' % e)
            return
        else:
            for item in data.get('array', []):
                # get comments
                if item.get('comments') > 0:
                    biji_id = item.get('id')
                    meta = meta.copy()
                    meta['item'] = item
                    headers = self.HEADERS.update({'Referer' : response.url})
                    yield Request(self.API_GET_COMMENTS % (self.__get_current_time(), biji_id),
                                  meta=meta,
                                  headers=headers,
                                  callback=self.parse_comment)
                # dump biji
                else:
                    self.logger.info('got item [%s] : %s' % (meta['source'], json.dumps(item, ensure_ascii=False).encode('utf-8')))
            try:
                last_id = data.get('array', [])[-1].get('id')
                api = meta['api']
                headers = self.HEADERS.update({'Referer':response.url})
                yield Request(url=api % (self.__get_current_time(), last_id), meta=meta, headers=headers)
            except Exception, e:
                self.logger.error('failed to get more : %s, url : %s' % (e, response.url))

    def parse_comment(self, response):
        meta = response.meta
        try:
            data = json.loads(response.body_as_unicode())
        except Exception, e:
            self.logger.error('invalid result in parse_comment : %s, url : %s' % (e, response.url))
            return
        else:
            item = meta['item']
            item['comments'] = data.get('comments')
            self.logger.info('got item [%s] : %s' % (meta['source'], json.dumps(item, ensure_ascii=False).encode('utf-8')))
