# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from dateutil import parser
from finance.items import ReplyItem
from finance.utils.date_util import get_current_date
import json
import re

class Rong360Spider(scrapy.Spider):
    name = "rong360"

    cookies = {}

    custom_settings = {
        'ITEM_PIPELINES' : {
            'finance.pipelines.ReplyItemMongoOriginPipeline' : 100,
        }
    }

    def __init__(self, cookie_str=''):
        if not cookie_str:
            return
        for item in cookie_str.split(';'):
            k, v = item.split('=')
            self.cookies[k] = v


    def start_requests(self):
        api = 'https://www.rong360.com/licai-p2p/pingtai/rating'
        yield Request(api, cookies=self.cookies, callback=self.parse_list)

    def parse_list(self, response):
        selector = Selector(response)
        for item in selector.xpath("//tbody[@id='ui_product_list_tbody']/tr"):
            item_name = item.xpath(".//a[@class='doc-color-link']/text()").extract_first()

            item_id = item.xpath(".//a[@class='doc-color-link']/@href").extract_first()
            match = re.match("^.*?pingtai-(\d+).*$", item_id)
            if match:
                item_id = match.group(1)
            comments = item.xpath(".//span[@class='rate-num']/text()").extract_first()
            match = re.match("^.*?(\d+).*$", comments)
            if match:
                comments = int(match.group(1))
                for page in range(1, comments/8+1):
                    api = 'https://www.rong360.com/licai-p2p/pingtai-ajaxpostlist-c%s-t0/p%s' % (item_id, page)
                    meta = {
                        'item_name' : item_name
                    }
                    yield Request(api, meta=meta, callback=self.parse_comment)
                    #return #todo

    def parse_comment(self, response):
        selector = Selector(response)
        for item in selector.xpath("//div[@class='loan-score wrap-clear']"):
            text = item.xpath("./div[2]/table//p[@class='wrap-left']/text()").extract_first()
            authorname = item.xpath("./div/p/text()").extract_first()
            publishdate = item.xpath("./div[2]/dl/dd/span/text()").extract_first()
            match = re.match("^.*?(\d+-\d+-\d+).*?(\d+:\d+:\d+).*$", publishdate)
            if match:
                publishdate = match.group(1) + ' ' + match.group(2)
            publishdate = parser.parse(publishdate).strftime("%Y-%m-%d %H:%M:%S")

            reply_item = ReplyItem()
            reply_item['authorurl'] = ''
            reply_item['floornum'] = 0
            reply_item['host'] = 'rong360.com'
            reply_item['domain'] = 'rong360.com'
            reply_item['bankuaiid'] = ''
            reply_item['threadid'] = ''
            reply_item['threadurl'] = response.url
            reply_item['tieziid'] = ''
            reply_item['text'] = text.strip()
            reply_item['title'] = response.meta.get('item_name')
            reply_item['crawldate'] = get_current_date()
            reply_item['sourceurl'] = 'https://www.rong360.com/licai-p2p/pingtai/rating'
            reply_item['bankuainame'] = ''
            reply_item['authorname'] = authorname.strip()
            reply_item['publishdate'] = publishdate

            reply_item['threadid'] = ''
            #self.logger.info('got item : %s' % json.dumps(dict(reply_item), ensure_ascii=False).encode('utf-8'))
            yield reply_item
            #return # todo

