# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from utils.htmlutils import remove_tags
import json
import re

class QyerQYSpider(scrapy.Spider):
    name = 'qyer_qiongyou'

    qiongyour_api = ('http://guide.qyer.com/index.php', 17)

    POST_HEADERS = {
        'Host' : 'guide.qyer.com',
        'Accept' : 'application/json, text/javascript, */*; q=0.01',
        'Origin' : 'http://guide.qyer.com',
        'X-Requested-With' : 'XMLHttpRequest',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Referer' : 'http://guide.qyer.com/',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def start_requests(self):
        for page in range(self.qiongyour_api[1]):
            formdata = {
                'action' : 'ajaxgpage',
                'page' : str(page+1),
                'overway' : ''
            }
            yield FormRequest(self.qiongyour_api[0], formdata=formdata, headers=self.POST_HEADERS, callback=self.parse_qiongyou)

    def parse_qiongyou(self, response):
        try:
            data = json.loads(response.body_as_unicode())
        except Exception:
            self.logger.error('invalid result for url : %s' % response.url)
            return
        else:
            if data.get('error_code') != 0:
                self.logger.error('invalid result for url : %s' % response.url)
                return
            html = data.get('data')
            selector = Selector(text=html)
            for qiongyou in selector.xpath('//li[@class="gui_jnlist_item"]'):
                url = qiongyou.xpath('./p[@class="gui_jnlist_item_tit"]/a/@href').extract_first()
                yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        selector = Selector(response)
        data_str = ''.join(selector.xpath('//div[@class="gui_info_text"]/node()').extract())
        match_result = re.match(u'^.*名称：</span>(?P<name>.*)<br.*?所属分类：</span>(?P<category>.*?)<br.*?更新时间：</span>(?P<date>.*?)<br.*?下载次数：</span><em class="number">(?P<download_count>.*?)</em.*$', data_str, re.DOTALL)
        if not match_result:
            self.logger.error('invalid result')
            return
        data = match_result.groupdict()
        name = data.get('name')
        date = data.get('date')
        download_count = data.get('download_count')

        if not name or not date or not download_count:
            self.logger.error('invalid result')
            return
        result = {
            'name' : name,
            'date' : date,
            'download_count' : download_count
        }
        self.logger.info('qyer qiongyou : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))


class QyerBBSSpider(scrapy.Spider):
    name = 'qyer_bbs'

    custom_settings = {
        'DOWNLOAD_TIMEOUT' : 10,
        'DOWNLOAD_DELAY' : 0.3
    }

    bbs_api = (
        (u'欧洲', u'环游欧洲', u'http://bbs.qyer.com/forum-112-1-1-%d.html?#gotonav'),
        (u'欧洲', u'法国/摩纳哥', u'http://bbs.qyer.com/forum-14-1-%d.html?#gotonav'),
        (u'欧洲', u'德国', u'http://bbs.qyer.com/forum-12-1-%d.html?#gotonav'),
        (u'欧洲', u'瑞士/列支敦士登', u'http://bbs.qyer.com/forum-15-1-%d.html?#gotonav'),
        (u'欧洲', u'奥地利', u'http://bbs.qyer.com/forum-19-1-%d.html?#gotonav'),
        (u'欧洲', u'捷克/斯洛伐克/匈牙利', u'http://bbs.qyer.com/forum-24-1-%d.html?#gotonav'),
        (u'欧洲', u'西班牙/葡萄牙/安道尔', u'http://bbs.qyer.com/forum-18-1-%d.html?#gotonav'),
        (u'欧洲', u'希腊/塞浦路斯', u'http://bbs.qyer.com/forum-26-1-%d.html?#gotonav'),
        (u'欧洲', u'意大利/梵蒂冈/圣马力诺/马耳他', u'http://bbs.qyer.com/forum-13-1-%d.html?#gotonav'),
        (u'欧洲', u'英国/爱尔兰', u'http://bbs.qyer.com/forum-16-1-%d.html?#gotonav'),
        (u'欧洲', u'荷兰/比利时/卢森堡', u'http://bbs.qyer.com/forum-17-1-%d.html?#gotonav'),
        (u'欧洲', u'波兰/立陶宛/拉脱维亚/爱沙尼亚', u'http://bbs.qyer.com/forum-161-1-%d.html?#gotonav'),
        (u'欧洲', u'挪威/瑞典/芬兰/丹麦/冰岛', u'http://bbs.qyer.com/forum-25-1-%d.html?#gotonav'),
        (u'欧洲', u'俄罗斯/乌克兰/白俄罗斯', u'http://bbs.qyer.com/forum-158-1-%d.html?#gotonav'),
        (u'欧洲', u'外高加索三国', u'http://bbs.qyer.com/forum-160-1-%d.html?#gotonav'),
        (u'欧洲', u'土耳其', u'http://bbs.qyer.com/forum-162-1-%d.html?#gotonav'),
        (u'欧洲', u'东南欧地区', u'http://bbs.qyer.com/forum-159-1-%d.html?#gotonav'),
        (u'美洲', u'美国', u'http://bbs.qyer.com/forum-53-1-%d.html?#gotonav'),
        (u'美洲', u'加拿大', u'http://bbs.qyer.com/forum-54-1-%d.html?#gotonav'),
        (u'美洲', u'中美', u'http://bbs.qyer.com/forum-168-1-%d.html?#gotonav'),
        (u'美洲', u'南美/南极', u'http://bbs.qyer.com/forum-55-1-%d.html?#gotonav'),
        (u'大洋洲', u'澳大利亚', u'http://bbs.qyer.com/forum-56-1-%d.html?#gotonav'),
        (u'大洋洲', u'新西兰', u'http://bbs.qyer.com/forum-83-1-%d.html?#gotonav'),
        (u'大洋洲', u'太平洋海岛', u'http://bbs.qyer.com/forum-178-1-%d.html?#gotonav'),
        (u'非洲', u'北非', u'http://bbs.qyer.com/forum-86-1-%d.html?#gotonav'),
        (u'非洲', u'东非', u'http://bbs.qyer.com/forum-173-1-%d.html?#gotonav'),
        (u'非洲', u'非洲海岛', u'http://bbs.qyer.com/forum-174-1-%d.html?#gotonav'),
        (u'非洲', u'非洲其他', u'http://bbs.qyer.com/forum-60-1-%d.html?#gotonav'),
        (u'亚洲', u'环游亚洲', u'http://bbs.qyer.com/forum-58-1-%d.html?#gotonav'),
        (u'亚洲', u'日本', u'http://bbs.qyer.com/forum-57-1-%d.html?#gotonav'),
        (u'亚洲', u'韩国/朝鲜', u'http://bbs.qyer.com/forum-156-1-%d.html?#gotonav'),
        (u'亚洲', u'台湾', u'http://bbs.qyer.com/forum-52-1-%d.html?#gotonav'),
        (u'亚洲', u'香港/澳门', u'http://bbs.qyer.com/forum-163-1-%d.html?#gotonav'),
        (u'亚洲', u'泰国', u'http://bbs.qyer.com/forum-106-1-%d.html?#gotonav'),
        (u'亚洲', u'马来西亚/文莱', u'http://bbs.qyer.com/forum-108-1-%d.html?#gotonav'),
        (u'亚洲', u'新加坡', u'http://bbs.qyer.com/forum-164-1-%d.html?#gotonav'),
        (u'亚洲', u'菲律宾', u'http://bbs.qyer.com/forum-110-1-%d.html?#gotonav'),
        (u'亚洲', u'柬埔寨', u'http://bbs.qyer.com/forum-175-1-%d.html?#gotonav'),
        (u'亚洲', u'越南', u'http://bbs.qyer.com/forum-107-1-%d.html?#gotonav'),
        (u'亚洲', u'老挝', u'http://bbs.qyer.com/forum-176-1-%d.html?#gotonav'),
        (u'亚洲', u'缅甸', u'http://bbs.qyer.com/forum-177-1-%d.html?#gotonav'),
        (u'亚洲', u'尼泊尔', u'http://bbs.qyer.com/forum-102-1-%d.html?#gotonav'),
        (u'亚洲', u'不丹', u'http://bbs.qyer.com/forum-166-1-%d.html?#gotonav'),
        (u'亚洲', u'印度尼西亚/东帝汶', u'http://bbs.qyer.com/forum-111-1-%d.html?#gotonav'),
        (u'亚洲', u'马尔代夫', u'http://bbs.qyer.com/forum-104-1-%d.html?#gotonav'),
        (u'亚洲', u'斯里兰卡', u'http://bbs.qyer.com/forum-165-1-%d.html?#gotonav'),
        (u'亚洲', u'印度/孟加拉', u'http://bbs.qyer.com/forum-103-1-%d.html?#gotonav'),
        (u'亚洲', u'伊朗', u'http://bbs.qyer.com/forum-59-1-%d.html?#gotonav'),
        (u'亚洲', u'巴基斯坦/阿富汗', u'http://bbs.qyer.com/forum-169-1-%d.html?#gotonav'),
        (u'亚洲', u'阿联酋/卡塔尔', u'http://bbs.qyer.com/forum-171-1-%d.html?#gotonav'),
        (u'亚洲', u'以色列', u'http://bbs.qyer.com/forum-170-1-%d.html?#gotonav'),
        (u'亚洲', u'西亚及其他', u'http://bbs.qyer.com/forum-172-1-%d.html?#gotonav'),
        (u'亚洲', u'中亚各国', u'http://bbs.qyer.com/forum-105-1-%d.html?#gotonav'),
        (u'亚洲', u'蒙古', u'http://bbs.qyer.com/forum-167-1-%d.html?#gotonav'),
        (u'亚洲', u'中国内地', u'http://bbs.qyer.com/forum-51-1-%d.html?#gotonav'),
    )


    HEADERS = {
        'Host' : 'bbs.qyer.com',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def start_requests(self):
        for gonglue_item in self.bbs_api:
            meta = {}
            meta['main_class'] = gonglue_item[0]
            meta['second_class'] = gonglue_item[1]
            meta['api'] = gonglue_item[2]
            meta['list_first_page'] = True
            yield Request(gonglue_item[2] % 1, meta=meta, headers=self.HEADERS, dont_filter=True, callback=self.parse_list)

    def parse_list(self, response):
        meta = response.meta.copy()
        selector = Selector(response)
        for tiezi in selector.xpath('//ul[@id="list-id"]/li'):
            title = tiezi.xpath('.//dt[@class="title fontYaHei"]/a[@class="txt"]/text()').extract_first()
            author = tiezi.xpath('.//dd[@class="data"]/a[1]/text()').extract_first()
            date = tiezi.xpath('.//dd[@class="data"]/span[@class="date"]/text()').extract_first()
            view_count = tiezi.xpath('.//dd[@class="data"]/span[@class="poi"]/text()').extract_first()
            comment_count = tiezi.xpath('.//dd[@class="data"]/span[@class="reply"]/text()').extract_first()
            like_count = tiezi.xpath('.//dd[@class="data"]/span[@class="like"]/text()').extract_first()
            url = tiezi.xpath('.//dt[@class="title fontYaHei"]/a[@class="txt"]/@href').extract_first()

            self.logger.debug('title : %s, author : %s, date : %s, url : %s' % (title, author, date, url))
            if not title or not author or not date or not url:
                continue
            date += ' 00:00:00'
            data = {
                'host' : 'qyer',
                'main_class' : meta['main_class'],
                'second_class' : meta['second_class'],
                'title' : title,
                'author' : author,
                'date' : date,
                'view_count' : view_count,
                'comment_count' : comment_count,
                'like_count' : like_count,
                'url' : url
            }
            pages = int(like_count)/15 + 1
            self.logger.info('comment pages : %s' % pages)
            for page in range(pages):
                api = url.replace('-1.html', '-%d.html' % (page+1))
                yield Request(api, meta={'data':data, 'page' : page+1}, headers=self.HEADERS, dont_filter=True, callback=self.parse_content)

        # deal with pages
        pages = selector.xpath('//div[@class="ui_page"]/a[last()-1]/@data-page').extract_first()
        self.logger.info('list pages : %s' % pages)
        if not pages:
            pages = 1
            del meta['list_first_page']
            for page in range(int(pages)-1):
                yield Request(meta['api'] % (page+2), meta=meta, headers=self.HEADERS, callback=self.parse_list)

    def parse_content(self, response):
        data = response.meta['data']
        selector = Selector(response)
        replies = []
        for post in selector.xpath('//div[@class="bbs_detail_list"]/div[@class="bbs_detail_item"]'):
            date = post.xpath('./div[@class="bbs_detail_title clearfix"]/p[@class="texts"]/text()').extract_first()
            content = ''.join(post.xpath('./div[@class="bbs_detail_content"]/node()').extract())
            author = post.xpath('./div[@class="bbs_detail_title clearfix"]/h3[@class="titles"]/a/text()').extract_first()
            floor = post.xpath('./div[@class="bbs_detail_title clearfix"]/a[last()]/text()').extract_first()
            if not date or not content or not floor:
                continue
            date = date.replace(u'发表于 ', '') + ':00'
            floor = str(int(floor.replace(u'楼', '')) -1)
            content = remove_tags(content)
            content = re.sub(r'\s*\n\s*', '', content)
            replies.append({
                'date' : date,
                'content' : remove_tags(content).replace('\r\n', ''),
                'author' : author,
                'floor' : floor
            })

            result = data.copy()
            result.update({
                'content' : content,
                'floor' : floor,
            })
            if floor == '0':
                self.logger.info('qyer bbs: %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
            else:
                result.update({
                    'view_count' : 0,
                    'comment_count' : 0,
                    'like_count' : 0
                })
                self.logger.info('qyer bbs: %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
