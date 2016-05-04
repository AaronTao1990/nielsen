# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from scrapy.http import Request
from scrapy.selector import Selector
import json
import urllib

class VendorSpider(scrapy.Spider):
    name = "vendor"
    allowed_domains = ["dianping.com"]
    start_urls = (
        'http://www.dianping.com/',
    )

    #search_api = 'http://www.dianping.com/search/keyword/%s/0_%s'
    search_api = 'http://localhost:5000/search/keyword/%s/0_%s'

    targets = (
        u'肯德基',
        #u'麦当劳',
    )

    HEADERS = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
        'Host' : 'www.dianping.com',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    def __init__(self):
        self.citycode_file = settings.get('CITYCODE_FILE')

    def __load_cities(self):
        with open(self.citycode_file, 'r') as f:
            for line in f.readlines():
                yield json.loads(line.strip('\n'))

    def start_requests(self):
        for city in self.__load_cities():
            for target in self.targets:
                api = self.search_api % (city['citycode'], urllib.quote(target.encode('utf-8')))
                headers = self.HEADERS.copy()
                headers['Referer'] = city.get('url')
                yield Request(api, meta={'city' : city, 'api_confirmed' : False, 'first_page' : True, 'target' : target}, headers=headers, callback=self.parse_first_page)
                return # only one city

    def parse_first_page(self, response):
        meta = response.meta
        selector = Selector(response)

        # try to find the offical branch api
        if not meta.get('api_confirmed'):
            fendian_api = selector.xpath('//div[@class="shop-wrap"]//a[@class="shop-branch"]/@href').extract_first()
            if fendian_api:
                meta['api_confirmed'] = True
                meta['api_confirmed_fendian'] = True
                fendian_api = 'http://www.dianping.com' + fendian_api
                headers = self.HEADERS.copy()
                headers['Referer'] = response.url
                yield Request(fendian_api, meta=response.meta, headers=headers, callback=self.parse_first_page)
                return

        # may fail to get fendian api, confirm to use current api
        meta['api_confirmed'] = True

        # deal with pages
        if meta.get('first_page'):
            meta['first_page'] = False
            pages = selector.xpath('//div[@class="page"]/a[@class="PageLink"]/text()').extract_first()
            self.logger.debug('pages : %s' % pages)
            for pages in range(int(pages)):
                api = self.search_api % (meta['city']['citycode'], urllib.quote(meta.get('target').encode('utf-8')))
                headers = self.HEADERS.copy()
                headers['Referer'] = meta['city']['url']
                yield Request(api, meta=meta, headers=headers, callback=self.parse_first_page)
                return # only one page
            return

        # deal with real dianpu
        for dianpu in selector.xpath('//div[@id="shop-all-list"]/ul/li'):
            dianpu_name = dianpu.xpath('.//div[@class="tit"]/a[1]/@title').extract_first()
            url = 'http://www.dianping.com' + dianpu.xpath('.//div[@class="tit"]/a[1]/@href').extract_first()
            fendian_icon = dianpu.xpath('.//div[@class="tit"]/a[@class="shop-branch"]/text()').extract_first()
            promo_icon = '|'.join(dianpu.xpath('.//div[@class="promo-icon"]/a/@title').extract())
            star = dianpu.xpath('.//div[@class="comment"]/span/@title').extract_first()
            comments_count = dianpu.xpath('.//div[@class="comment"]/a[@class="review-num"]/b/text()').extract_first()
            mean_price = dianpu.xpath('.//div[@class="comment"]/a[@class="mean-price"]/b/text()').extract_first()

            category = dianpu.xpath('.//div[@class="tag-addr"]/a[1]/span/text()').extract_first()
            addr_first = dianpu.xpath('.//div[@class="tag-addr"]/a[2]/span/text()').extract_first()
            addr_second = dianpu.xpath('.//div[@class="tag-addr"]/span[@class="addr"]/text()').extract_first()
            addr = str(addr_first) + str(addr_second)

            data = {
                'city_area' : meta['city']['area'],
                'city_name' : meta['city']['name'],
                'city_province' : meta['city']['province'],
                'confirmed_fendian' : meta.get('api_confirmed_fendian'),
                'dianpu_name' : dianpu_name,
                'url' : url,
                'fendian_icon' : fendian_icon,
                'promo_icon' : promo_icon,
                'star' : star,
                'comments_count' : comments_count,
                'mean_price' : mean_price,
                'category' : category,
                'addr' : addr
            }
            self.logger.info('dianpu item : %s' % json.dumps(data, ensure_ascii=False).encode('utf-8'))

