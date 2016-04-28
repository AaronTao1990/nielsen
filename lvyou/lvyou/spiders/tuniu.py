# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
import json
import re

class TuniuSpider(scrapy.Spider):
    name = "tuniu_youji"

    youji_api = ('http://trips.tuniu.com/travelthread/t/0/%d/0', 281)

    HEADERS = {
        'Host' : 'trips.tuniu.com',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def start_requests(self):
        for page in range(self.youji_api[1]):
            yield Request(self.youji_api[0] % (page + 1), headers=self.HEADERS, dont_filter=True, callback=self.parse_youji)
            return

    def parse_youji(self, response):
        selector = Selector(response)
        for youji in selector.xpath('//div[@class="hot-main-square clearfix"]'):
            title = youji.xpath('./div[@class="hot-main-up"]/a/@title').extract_first()
            url = youji.xpath('./div[@class="hot-main-up"]/a/@href').extract_first()
            count_str = ''.join(youji.xpath('./div[@class="hot-main-middle"]/p[2]/node()').extract())
            match_result = re.match(r'^.*?(?P<view_count>\d+).*?(?P<love_count>\d+).*?(?P<comment_count>\d+).*?$',
                                    count_str,
                                    re.DOTALL)
            if not match_result:
                self.logger.error('failed to retrieve count data for url : %s' % response.url)
                continue
            counts = match_result.groupdict()
            view_count = counts.get('view_count')
            love_count = counts.get('love_count')
            comment_count = counts.get('comment_count')
            author = youji.xpath('./div[@class="hot-main-down"]/p/a/em/text()').extract_first()
            date = youji.xpath('./div[@class="hot-main-down"]/p/span/span/text()').extract_first()
            result = {
                'title' : title,
                'url' : url,
                'view_count' : view_count,
                'love_count' : love_count,
                'comment_count' : comment_count,
                'author' : author,
                'date' : date
            }
            if comment_count != '0':
                comment_api = 'http://www.tuniu.com/yii.php?r=trips/notesAjax/getreplylist'
                meta = response.meta.copy()
                meta['result'] = result

                travel_id_match = re.match('^.*trips/(\d+).*$', url)
                if not travel_id_match:
                    self.logger.error('failed to extract travel_id for url : %s' %  url)
                    continue
                travelId = travel_id_match.group(1)
                self.logger.info('travel id : %s' % travelId)
                formdata = {
                    'travelId' : travelId,
                    'page' : '1',
                    'IsLookAuthor' : '0',
                    'ReplyPageSize' : '30'
                }
                yield FormRequest(comment_api, headers=self.HEADERS.update({'Referer' : url}), formdata=formdata, meta=meta, callback=self.parse_comments)


    def parse_comments(self, response):
        meta = response.meta
        try:
            comment_data = json.loads(response.body_as_unicode())
        except Exception:
            self.logger.error('invalid result for tuniu comments')
            return
        else:
            if not comment_data.get('success'):
                self.logger.error('invalid result for tuniu comments')
                return
            html = comment_data.get('data')
            selector = Selector(text=html)
            comments = []
            for comment_item in selector.xpath('//div[@class="commentary-co clearfix"]'):
                author = comment_item.xpath('.//div[@class="commentary-center clearfix"]/p[@class="author-name"]/a/text()').extract_first()
                date = comment_item.xpath('.//div[@class="commentary-center clearfix"]/p[2]/em[2]/text()').extract_first()
                content = comment_item.xpath('.//div[@class="commentary-center clearfix"]/p[@class="commentary-txt"]/text()').extract_first()
                comments.append({
                    'author' : author,
                    'date' : date,
                    'content' : content
                })
            result = meta['result']
            result['comments'] = comments
            self.logger.info('tuniu youji : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))



#class QunarBBSSpider(scrapy.Spider):
#    name = 'qunar_bbs'
#
#    bbs_api = (
#        (u'聪明旅行家专区', u'分享', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=56&filter=typeid&typeid=28&orderby=views&page=%d', 13),
#        (u'聪明旅行家专区', u'组团', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=56&filter=typeid&typeid=29&orderby=views&page=%d', 17),
#        (u'旅游问答', u'国内', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=17&orderby=views&page=%d', 577),
#        (u'旅游问答', u'东南亚', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=18&orderby=views&page=%d', 135),
#        (u'旅游问答', u'欧洲', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=19&orderby=views&page=%d', 112),
#        (u'旅游问答', u'美洲', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=20&orderby=views&page=%d', 29),
#        (u'旅游问答', u'大洋洲', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=54&filter=typeid&typeid=21&orderby=views&page=%d', 24),
#        (u'精彩游记', u'国内游', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=42&typeid=3&orderby=views&typeid=3&orderby=views&filter=typeid&page=%d', 168),
#        (u'精彩游记', u'港澳台', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=42&filter=typeid&typeid=4&orderby=views&page=%d', 12),
#        (u'精彩游记', u'出境游', 'http://travel.qunar.com/bbs/forum.php?mod=forumdisplay&fid=42&filter=typeid&typeid=5&orderby=views&page=%d', 52),
#    )
#
#    HEADERS = {
#        'Host' : 'travel.qunar.com',
#        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#        'Accept-Encoding' : 'gzip, deflate, sdch',
#        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
#    }
#
#    def start_requests(self):
#        for gonglue_item in self.bbs_api:
#            meta = {}
#            meta['main_class'] = gonglue_item[0]
#            meta['second_class'] = gonglue_item[1]
#            for page in range(gonglue_item[3]):
#                yield Request(gonglue_item[2] % (page + 1), meta=meta, headers=self.HEADERS, dont_filter=True, callback=self.parse_list)
#
#    def parse_list(self, response):
#        meta = response.meta
#        body = re.sub(r'(<tbody id="normalthread_\d+")', r'\g<1>>', response.body_as_unicode())
#        selector = Selector(text=body)
#        for tiezi in selector.xpath('//table[@id="threadlisttableid"]/tbody[position()>1]/tr/th'):
#            title = tiezi.xpath('./span[@class="xst"]/a/text()').extract_first()
#            author = tiezi.xpath('./p[@class="mtn xg1"]/a[1]/text()').extract_first()
#            date = tiezi.xpath('./p[@class="mtn xg1"]/span/text()').extract_first()
#            view_count_text = ''.join(tiezi.xpath('./p[@class="mtn xg1"]/node()').extract())
#            view_count = re.search(u'(?<=查看: )\d+', view_count_text).group(0)
#            reply_count = tiezi.xpath('./p[@class="mtn xg1"]/a[2]/text()').extract_first()
#            url = 'http://travel.qunar.com/bbs/' + tiezi.xpath('./span[@class="xst"]/a/@href').extract_first()
#            data = {
#                'main_class' : meta['main_class'],
#                'second_class' : meta['second_class'],
#                'title' : title,
#                'author' : author,
#                'date' : date,
#                'view_count' : view_count,
#                'reply_count' : reply_count,
#                'url' : url
#            }
#            yield Request(url, meta={'data':data}, headers=self.HEADERS, dont_filter=True, callback=self.parse_content)
#
#    def parse_content(self, response):
#        data = response.meta['data']
#        selector = Selector(response)
#        replies = []
#        for post in selector.xpath('//div[@id="postlist"]//td[@class="plc"]'):
#            time = post.xpath('.//div[@class="authi"]/em/text()').extract_first()
#            content = ''.join(post.xpath('.//div[@class="t_fsz"]/node()').extract())
#            if not time or not content:
#                continue
#            replies.append({
#                'time' : time,
#                'content' : content
#            })
#        if replies:
#            data['content'] = replies[0]['content']
#            data['replies'] = replies[1:]
#        self.logger.info('qunar bbs: %s' % json.dumps(data, ensure_ascii=False).encode('utf-8'))
#
#
