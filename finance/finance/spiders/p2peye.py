# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from dateutil import parser
from finance.items import ReplyItem
from finance.utils.date_util import get_current_date

class P2peyeSpider(scrapy.Spider):
    name = "p2peye"

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
        api = 'http://www.p2peye.com/platform/all/'
        yield Request(api, cookies=self.cookies, callback=self.parse_list)
        for page in range(2, 200):
            api = 'http://www.p2peye.com/platform/all/p%s/' % page
            yield Request(api, cookies=self.cookies, callback=self.parse_list)

    def parse_list(self, response):
        selector = Selector(response)
        for item in selector.xpath("//li[@class='ui-result-item']"):
            item_name = item.xpath(".//a[@class='ui-result-pname']/text()").extract_first()
            item_url = item.xpath(".//a[@class='ui-result-pname']/@href").extract_first()
            comments = item.xpath(".//p[@class='ui-result-text']/span[last()]/text()").extract_first()
            comments = int(comments)

            self.logger.info('item_name : %s, comments : %s' % (item_name, comments))

            for page in range(1, comments/10+2):
                api = '%s/comment/list-0-0-%s.html' % (item_url, page)
                meta = {
                    'item_name' : item_name
                }
                yield Request(api, meta=meta, callback=self.parse_comment)

    def parse_comment(self, response):
        selector = Selector(response)
        for item in selector.xpath("//ul[@id='comment']/li[@class='feed-detail clearfix']"):
            text = item.xpath(".//div[@class='link']/a/text()").extract_first()
            authorname = item.xpath(".//a[@class='qt-gl username']/text()").extract_first()
            if not authorname:
                authorname = ''
            publishdate = item.xpath(".//div[@class='qt-gl time']/text()").extract_first()
            publishdate = parser.parse(publishdate).strftime("%Y-%m-%d %H:%M:%S")

            reply_item = ReplyItem()
            reply_item['authorurl'] = ''
            reply_item['floornum'] = 0
            reply_item['host'] = 'p2peye.com'
            reply_item['domain'] = 'p2peye.com'
            reply_item['bankuaiid'] = ''
            reply_item['threadid'] = ''
            reply_item['threadurl'] = response.url
            reply_item['tieziid'] = ''
            reply_item['text'] = text.strip()
            reply_item['title'] = response.meta.get('item_name')
            reply_item['crawldate'] = get_current_date()
            reply_item['sourceurl'] = 'http://www.p2peye.com/platform/all/'
            reply_item['bankuainame'] = ''
            reply_item['authorname'] = authorname.strip()
            reply_item['publishdate'] = publishdate

            reply_item['threadid'] = ''
            #self.logger.info('got item : %s' % json.dumps(dict(reply_item), ensure_ascii=False).encode('utf-8'))
            yield reply_item

