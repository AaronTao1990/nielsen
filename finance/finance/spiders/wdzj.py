# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.selector import Selector
from dateutil import parser
from finance.items import ReplyItem
from finance.utils.date_util import get_current_date
import json
import re

class WdzjSpider(scrapy.Spider):
    name = "wdzj"
    allowed_domains = ["wdzj.com"]



    cookies = {}

    custom_settings = {
        'ITEM_PIPELINES' : {
            'finance.pipelines.ReplyItemMongoOriginPipeline' : 100,
        }
    }

    def __init__(self, cookie_str):
        for item in cookie_str.split(';'):
            k, v = item.split('=')
            self.cookies[k] = v


    def start_requests(self):
        for page in range(1, 194):
            api = 'http://www.wdzj.com/front_select-plat'
            data = {
                'params' : '',
                'sort' : '0',
                'currPage' : 'page'
            }
            yield FormRequest(api, formdata=data, cookies=self.cookies, callback=self.parse_list, dont_filter=True)
            #return #todo

    def parse_list(self, response):
        try:
            data = json.loads(response.body_as_unicode())
        except Exception:
            pass
        else:
            for item in data.get('list'):
                item_id = item.get('platId')

                api = 'http://www.wdzj.com/front/dianpingInfo/%s/20/1'  % (item_id)
                meta = {
                    'item_id' : item_id,
                    'item_name' : item.get('platName')
                }
                data = {
                    'type' : '',
                    'sort' : '0'
                }
                yield FormRequest(api, meta=meta, formdata=data, cookies=self.cookies, callback=self.parse_comment, dont_filter=True)
                #return #todo

    def parse_comment(self, response):
        selector = Selector(response)
        for item in selector.xpath("//ul[@class='commentList']"):
            text = item.xpath(".//p[@class='font']/text()").extract_first()
            authorname = item.xpath(".//span[@class='name']/a/text()").extract_first()
            publishdate = item.xpath(".//span[@class='date']/text()").extract_first()
            publishdate = parser.parse(publishdate).strftime("%Y-%m-%d %H:%M:%S")

            reply_item = ReplyItem()
            reply_item['authorurl'] = ''
            reply_item['floornum'] = 0
            reply_item['host'] = 'www.wdzj.com'
            reply_item['domain'] = 'www.wdzj.com'
            reply_item['bankuaiid'] = ''
            reply_item['threadid'] = ''
            reply_item['threadurl'] = response.url
            reply_item['tieziid'] = ''
            reply_item['text'] = text.strip()
            reply_item['title'] = response.meta.get('item_name')
            reply_item['crawldate'] = get_current_date()
            reply_item['sourceurl'] = 'http://www.wdzj.com/dangan/'
            reply_item['bankuainame'] = ''
            reply_item['authorname'] = authorname.strip()
            reply_item['publishdate'] = publishdate

            reply_item['threadid'] = ''
            #self.logger.info('got item : %s' % json.dumps(dict(reply_item), ensure_ascii=False).encode('utf-8'))
            yield reply_item


        # paging
        if 'paged' in response.meta:
            return

        pages_str = selector.xpath("//div[@class='pageList']//span[@class='all']/text()").extract_first()
        match = re.match('^.*?/(\d+).*$', pages_str)
        if match:
            pages = int(match.group(1))
            for page in range(2, pages+1):
                api = 'http://www.wdzj.com/front/dianpingInfo/%s/20/%s'  % (response.meta.get('item_id'), page)
                new_meta = response.meta.copy()
                new_meta['paged'] = True
                data = {
                    'type' : '',
                    'sort' : '0'
                }
                yield FormRequest(api, meta=new_meta, formdata=data, cookies=self.cookies, callback=self.parse_comment, dont_filter=True)




