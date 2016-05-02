# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from utils.htmlutils import remove_tags
import json
import re

class QunarSpider(scrapy.Spider):
    name = "qunar_gonglue"

    gonglue_api = (
        (u'热门游记', 'http://travel.qunar.com/travelbook/list.htm?page=%d&order=hot_heat', 9999),
        (u'精华游记', 'http://travel.qunar.com/travelbook/list.htm?page=%d&order=elite_ctime', 717),
        (u'行程计划', 'http://travel.qunar.com/travelbook/list.htm?page=%d&order=start_heat', 9999),
    )

    HEADERS = {
        'Host' : 'travel.qunar.com',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def start_requests(self):
        for gonglue_item in self.gonglue_api:
            meta = {}
            meta['main_class'] = gonglue_item[0]
            for page in range(gonglue_item[2]):
                yield Request(gonglue_item[1] % (page + 1), meta=meta, headers=self.HEADERS, dont_filter=True, callback=self.parse_list)

    def parse_list(self, response):
        meta = response.meta
        selector = Selector(response)
        for gonglue in selector.xpath('//ul[@class="b_strategy_list "]/li'):
            view_count = gonglue.xpath('./div[@class="nums"]/span[@class="icon_view"]/text()').extract_first()
            love_count = gonglue.xpath('./div[@class="nums"]/span[@class="icon_love"]/text()').extract_first()
            comment_count = gonglue.xpath('./div[@class="nums"]/span[@class="icon_comment"]/text()').extract_first()
            title = gonglue.xpath('./h2[@class="tit"]/a/text()').extract_first()
            url = 'http://travel.qunar.com' + gonglue.xpath('./h2[@class="tit"]/a/@href').extract_first()
            username = gonglue.xpath('./p[@class="user_info"]/span[@class="user_name"]/a/text()').extract_first()
            date = gonglue.xpath('./p[@class="user_info"]/span[@class="date"]/text()').extract_first().replace(u'出发', '00:00:00')
            days = gonglue.xpath('./p[@class="user_info"]/span[@class="days"]/text()').extract_first()
            content = ''.join(gonglue.xpath('./p[@class="places"]/node()').extract())
            content = remove_tags(content)
            result = {
                'main_class' : meta['main_class'],
                'title' : title,
                'view_count' : view_count,
                'love_count' : love_count,
                'comment_count' : comment_count,
                'username' : username,
                'date' : date,
                'days' : days,
                'content' : content,
                'url' : url
            }
            #self.logger.info('qunar gonglue : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
            yield Request(url, meta={'result' : result}, headers=self.HEADERS, dont_filter=True, callback=self.parse_content)

    def parse_content(self, response):
        meta = response.meta
        selector = Selector(response)
        forward = ''.join(selector.xpath('//div[@id="b_foreword"]/node()').extract())
        scheduler = ''.join(selector.xpath('//div[@id="b_panel_schedule"]/node()').extract())
        content = remove_tags(forward+scheduler)
        result = meta['result']
        result['content'] = content
        self.logger.info('qunar gonglue : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))


class QunarBBSSpider(scrapy.Spider):
    name = 'qunar_bbs'

    bbs_api = (
        (u'聪明旅行家专区', u'分享', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=56&filter=typeid&typeid=28&orderby=views&page=%d', 13),
        (u'聪明旅行家专区', u'组团', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=56&filter=typeid&typeid=29&orderby=views&page=%d', 17),
        (u'旅游问答', u'国内', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=17&orderby=views&page=%d', 577),
        (u'旅游问答', u'东南亚', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=18&orderby=views&page=%d', 135),
        (u'旅游问答', u'欧洲', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=19&orderby=views&page=%d', 112),
        (u'旅游问答', u'美洲', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=20&orderby=views&page=%d', 29),
        (u'旅游问答', u'大洋洲', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=21&orderby=views&page=%d', 24),
        (u'精彩游记', u'国内游', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=42&typeid=3&orderby=views&typeid=3&orderby=views&filter=typeid&page=%d', 168),
        (u'精彩游记', u'港澳台', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=42&filter=typeid&typeid=4&orderby=views&page=%d', 12),
        (u'精彩游记', u'出境游', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=42&filter=typeid&typeid=5&orderby=views&page=%d', 52),
    )

    HEADERS = {
        'Host' : 'travel.qunar.com',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def start_requests(self):
        for gonglue_item in self.bbs_api:
            meta = {}
            meta['main_class'] = gonglue_item[0]
            meta['second_class'] = gonglue_item[1]
            for page in range(gonglue_item[3]):
                yield Request(gonglue_item[2] % (page + 1), meta=meta, headers=self.HEADERS, dont_filter=True, callback=self.parse_list)

    def parse_list(self, response):
        meta = response.meta
        body = re.sub(r'(<tbody id="normalthread_\d+")', r'\g<1>>', response.body_as_unicode())
        selector = Selector(text=body)
        for tiezi in selector.xpath('//table[@id="threadlisttableid"]/tbody[position()>1]/tr/th'):
            title = tiezi.xpath('./span[@class="xst"]/a/text()').extract_first()
            author = tiezi.xpath('./p[@class="mtn xg1"]/a[1]/text()').extract_first()
            date = tiezi.xpath('./p[@class="mtn xg1"]/span/text()').extract_first()
            view_count_text = ''.join(tiezi.xpath('./p[@class="mtn xg1"]/node()').extract())
            view_count = re.search(u'(?<=查看: )\d+', view_count_text).group(0)
            reply_count = tiezi.xpath('./p[@class="mtn xg1"]/a[2]/text()').extract_first()
            url = 'http://travel.qunar.com/bbs/' + tiezi.xpath('./span[@class="xst"]/a/@href').extract_first()
            data = {
                'main_class' : meta['main_class'],
                'second_class' : meta['second_class'],
                'title' : title,
                'author' : author,
                'date' : date,
                'view_count' : view_count,
                'reply_count' : reply_count,
                'url' : url
            }
            yield Request(url, meta={'data':data}, headers=self.HEADERS, dont_filter=True, callback=self.parse_content)

    def parse_content(self, response):
        data = response.meta['data']
        selector = Selector(response)
        replies = []
        for post in selector.xpath('//div[@id="postlist"]//td[@class="plc"]'):
            time = post.xpath('.//div[@class="authi"]/em/text()').extract_first()
            content = ''.join(post.xpath('.//div[@class="t_fsz"]/node()').extract())
            if not time or not content:
                continue
            replies.append({
                'time' : time,
                'content' : content
            })
        if replies:
            data['content'] = replies[0]['content']
            data['replies'] = replies[1:]
        self.logger.info('qunar bbs: %s' % json.dumps(data, ensure_ascii=False).encode('utf-8'))


