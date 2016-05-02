# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import json

class MafengwoSpider(scrapy.Spider):
    name = "mafengwo_gonglue"

    custom_settings = {
        'DOWNLOAD_DELAY' : 0.3
    }

    gonglue_api = (
        (u'欧洲', u'英国', 'http://www.mafengwo.cn/gonglve/mdd-oz_yg-0-0-0.html#list'),
        (u'欧洲', u'土耳其', 'http://www.mafengwo.cn/gonglve/mdd-oz_teq-0-0-0.html#list'),
        (u'欧洲', u'法国', 'http://www.mafengwo.cn/gonglve/mdd-oz_fg-0-0-0.html#list'),
        (u'欧洲', u'西班牙', 'http://www.mafengwo.cn/gonglve/mdd-oz_xby-0-0-0.html#list'),
        (u'欧洲', u'意大利', 'http://www.mafengwo.cn/gonglve/mdd-oz_ydl-0-0-0.html#list'),
        (u'欧洲', u'德国', 'http://www.mafengwo.cn/gonglve/mdd-oz_dg-0-0-0.html#list'),
        (u'欧洲', u'希腊', 'http://www.mafengwo.cn/gonglve/mdd-oz_xl-0-0-0.html#list'),
        (u'欧洲', u'俄罗斯', 'http://www.mafengwo.cn/gonglve/mdd-oz_els-0-0-0.html#list'),
        (u'欧洲', u'荷兰', 'http://www.mafengwo.cn/gonglve/mdd-oz_hl-0-0-0.html#list'),
        (u'欧洲', u'葡萄牙', 'http://www.mafengwo.cn/gonglve/mdd-oz_pty-0-0-0.html#list'),
        (u'欧洲', u'瑞士', 'http://www.mafengwo.cn/gonglve/mdd-oz_rs-0-0-0.html#list'),
        (u'欧洲', u'瑞典', 'http://www.mafengwo.cn/gonglve/mdd-oz_rd-0-0-0.html#list'),
        (u'欧洲', u'比利时', 'http://www.mafengwo.cn/gonglve/mdd-oz_bls-0-0-0.html#list'),
        (u'欧洲', u'奥地利', 'http://www.mafengwo.cn/gonglve/mdd-oz_adl-0-0-0.html#list'),
        (u'欧洲', u'丹麦', 'http://www.mafengwo.cn/gonglve/mdd-oz_dm-0-0-0.html#list'),
        (u'欧洲', u'捷克', 'http://www.mafengwo.cn/gonglve/mdd-oz_jk-0-0-0.html#list'),
        (u'欧洲', u'挪威', 'http://www.mafengwo.cn/gonglve/mdd-oz_nw-0-0-0.html#list'),
        (u'欧洲', u'爱尔兰', 'http://www.mafengwo.cn/gonglve/mdd-oz_ael-0-0-0.html#list'),
        (u'欧洲', u'冰岛', 'http://www.mafengwo.cn/gonglve/mdd-oz_bd-0-0-0.html#list'),
        (u'欧洲', u'芬兰', 'http://www.mafengwo.cn/gonglve/mdd-oz_fl-0-0-0.html#list'),
        (u'欧洲', u'匈牙利', 'http://www.mafengwo.cn/gonglve/mdd-oz_xyl-0-0-0.html#list'),
        (u'欧洲', u'卢森堡', 'http://www.mafengwo.cn/gonglve/mdd-oz_lsb-0-0-0.html#list'),
        (u'欧洲', u'马耳他', 'http://www.mafengwo.cn/gonglve/mdd-oz_met-0-0-0.html#list'),
        (u'东南亚', u'泰国', 'http://www.mafengwo.cn/gonglve/mdd-dny_tg-0-0-0.html#list'),
        (u'东南亚', u'马来西亚', 'http://www.mafengwo.cn/gonglve/mdd-dny_mlxy-0-0-0.html#list'),
        (u'东南亚', u'越南', 'http://www.mafengwo.cn/gonglve/mdd-dny_yn-0-0-0.html#list'),
        (u'东南亚', u'菲律宾', 'http://www.mafengwo.cn/gonglve/mdd-dny_flb-0-0-0.html#list'),
        (u'东南亚', u'缅甸', 'http://www.mafengwo.cn/gonglve/mdd-dny_md-0-0-0.html#list'),
        (u'东南亚', u'柬埔寨', 'http://www.mafengwo.cn/gonglve/mdd-dny_jpz-0-0-0.html#list'),
        (u'东南亚', u'新加坡', 'http://www.mafengwo.cn/gonglve/mdd-dny_xjp-0-0-0.html#list'),
        (u'东南亚', u'印度尼西亚', 'http://www.mafengwo.cn/gonglve/mdd-dny_ydnxy-0-0-0.html#list'),
        (u'东南亚', u'老挝', 'http://www.mafengwo.cn/gonglve/mdd-dny_lw-0-0-0.html#list'),
        (u'东南亚', u'文莱', 'http://www.mafengwo.cn/gonglve/mdd-dny_wl-0-0-0.html#list'),
        (u'北美', u'美国', 'http://www.mafengwo.cn/gonglve/mdd-bmz_mg-0-0-0.html#list'),
        (u'北美', u'加拿大', 'http://www.mafengwo.cn/gonglve/mdd-bmz_jnd-0-0-0.html#list'),
        (u'北美', u'古巴', 'http://www.mafengwo.cn/gonglve/mdd-bmz_gb-0-0-0.html#list'),
        (u'北美', u'墨西哥', 'http://www.mafengwo.cn/gonglve/mdd-bmz_mxg-0-0-0.html#list'),
        (u'大洋洲', u'澳大利亚', 'http://www.mafengwo.cn/gonglve/mdd-dyz_adly-0-0-0.html#list'),
        (u'大洋洲', u'新西兰', 'http://www.mafengwo.cn/gonglve/mdd-dyz_xxl-0-0-0.html#list'),
        (u'大洋洲', u'法属波利尼西亚', 'http://www.mafengwo.cn/gonglve/mdd-dyz_blnxy-0-0-0.html#list'),
        (u'大洋洲', u'帕劳', 'http://www.mafengwo.cn/gonglve/mdd-dyz_pl-0-0-0.html#list'),
        (u'大洋洲', u'斐济', 'http://www.mafengwo.cn/gonglve/mdd-dyz_fj-0-0-0.html#list'),
        (u'非洲', u'埃及', 'http://www.mafengwo.cn/gonglve/mdd-fz_aj-0-0-0.html#list'),
        (u'非洲', u'南非', 'http://www.mafengwo.cn/gonglve/mdd-fz_nf-0-0-0.html#list'),
        (u'非洲', u'坦桑尼亚', 'http://www.mafengwo.cn/gonglve/mdd-fz_tsny-0-0-0.html#list'),
        (u'非洲', u'突尼斯', 'http://www.mafengwo.cn/gonglve/mdd-fz_tns-0-0-0.html#list'),
        (u'非洲', u'肯尼亚', 'http://www.mafengwo.cn/gonglve/mdd-fz_kny-0-0-0.html#list'),
        (u'非洲', u'马达加斯加', 'http://www.mafengwo.cn/gonglve/mdd-fz_mdjsj-0-0-0.html#list'),
        (u'非洲', u'毛里求斯', 'http://www.mafengwo.cn/gonglve/mdd-fz_mlqs-0-0-0.html#list'),
        (u'非洲', u'塞舌尔', 'http://www.mafengwo.cn/gonglve/mdd-fz_sse-0-0-0.html#list'),
        (u'西亚', u'阿联酋', 'http://www.mafengwo.cn/gonglve/mdd-xy_alq-0-0-0.html#list'),
        (u'西亚', u'伊朗', 'http://www.mafengwo.cn/gonglve/mdd-xy_yl-0-0-0.html#list'),
        (u'西亚', u'以色列', 'http://www.mafengwo.cn/gonglve/mdd-xy_ysl-0-0-0.html#list'),
        (u'南美', u'巴西', 'http://www.mafengwo.cn/gonglve/mdd-nmz_bx-0-0-0.html#list'),
        (u'南美', u'秘鲁', 'http://www.mafengwo.cn/gonglve/mdd-nmz_bl-0-0-0.html#list'),
        (u'东亚', u'日本', 'http://www.mafengwo.cn/gonglve/mdd-dy_rb-0-0-0.html#list'),
        (u'东亚', u'韩国', 'http://www.mafengwo.cn/gonglve/mdd-dy_hg-0-0-0.html#list'),
        (u'东亚', u'朝鲜', 'http://www.mafengwo.cn/gonglve/mdd-dy_cx-0-0-0.html#list'),
        (u'南亚', u'印度', 'http://www.mafengwo.cn/gonglve/mdd-ny_yd-0-0-0.html#list'),
        (u'南亚', u'尼泊尔', 'http://www.mafengwo.cn/gonglve/mdd-ny_nbe-0-0-0.html#list'),
        (u'南亚', u'不丹', 'http://www.mafengwo.cn/gonglve/mdd-ny_bd-0-0-0.html#list'),
        (u'南亚', u'马尔代夫', 'http://www.mafengwo.cn/gonglve/mdd-ny_medf-0-0-0.html#list'),
        (u'南亚', u'斯里兰卡', 'http://www.mafengwo.cn/gonglve/mdd-ny_sllk-0-0-0.html#list'),
        (u'中国', u'云南', 'http://www.mafengwo.cn/gonglve/mdd-yn-0-0-1.html#list'),
        (u'中国', u'四川', 'http://www.mafengwo.cn/gonglve/mdd-sc-0-0-1.html#list'),
        (u'中国', u'江苏', 'http://www.mafengwo.cn/gonglve/mdd-js-0-0-1.html#list'),
        (u'中国', u'浙江', 'http://www.mafengwo.cn/gonglve/mdd-zj-0-0-1.html#list'),
        (u'中国', u'北京', 'http://www.mafengwo.cn/gonglve/mdd-bj-0-0-1.html#list'),
        (u'中国', u'广东', 'http://www.mafengwo.cn/gonglve/mdd-gd-0-0-1.html#list'),
        (u'中国', u'河北', 'http://www.mafengwo.cn/gonglve/mdd-heb-0-0-1.html#list'),
        (u'中国', u'台湾', 'http://www.mafengwo.cn/gonglve/mdd-tw-0-0-1.html#list'),
        (u'中国', u'内蒙古', 'http://www.mafengwo.cn/gonglve/mdd-nm-0-0-1.html#list'),
        (u'中国', u'贵州', 'http://www.mafengwo.cn/gonglve/mdd-gz-0-0-1.html#list'),
        (u'中国', u'山东', 'http://www.mafengwo.cn/gonglve/mdd-sd-0-0-1.html#list'),
        (u'中国', u'广西', 'http://www.mafengwo.cn/gonglve/mdd-gx-0-0-1.html#list'),
        (u'中国', u'青海', 'http://www.mafengwo.cn/gonglve/mdd-qh-0-0-1.html#list'),
        (u'中国', u'河南', 'http://www.mafengwo.cn/gonglve/mdd-hn-0-0-1.html#list'),
        (u'中国', u'江西', 'http://www.mafengwo.cn/gonglve/mdd-jx-0-0-1.html#list'),
        (u'中国', u'安徽', 'http://www.mafengwo.cn/gonglve/mdd-ah-0-0-1.html#list'),
        (u'中国', u'福建', 'http://www.mafengwo.cn/gonglve/mdd-fj-0-0-1.html#list'),
        (u'中国', u'吉林', 'http://www.mafengwo.cn/gonglve/mdd-jl-0-0-1.html#list'),
        (u'中国', u'新疆', 'http://www.mafengwo.cn/gonglve/mdd-xj-0-0-1.html#list'),
        (u'中国', u'海南', 'http://www.mafengwo.cn/gonglve/mdd-hainan-0-0-1.html#list'),
        (u'中国', u'黑龙江', 'http://www.mafengwo.cn/gonglve/mdd-hlj-0-0-1.html#list'),
        (u'中国', u'山西', 'http://www.mafengwo.cn/gonglve/mdd-s1x-0-0-1.html#list'),
        (u'中国', u'湖北', 'http://www.mafengwo.cn/gonglve/mdd-hub-0-0-1.html#list'),
        (u'中国', u'甘肃', 'http://www.mafengwo.cn/gonglve/mdd-gs-0-0-1.html#list'),
        (u'中国', u'湖南', 'http://www.mafengwo.cn/gonglve/mdd-hunan-0-0-1.html#list'),
        (u'中国', u'辽宁', 'http://www.mafengwo.cn/gonglve/mdd-ln-0-0-1.html#list'),
        (u'中国', u'上海', 'http://www.mafengwo.cn/gonglve/mdd-sh-0-0-1.html#list'),
        (u'中国', u'香港', 'http://www.mafengwo.cn/gonglve/mdd-hk-0-0-1.html#list'),
        (u'中国', u'重庆', 'http://www.mafengwo.cn/gonglve/mdd-cq-0-0-1.html#list'),
        (u'中国', u'澳门', 'http://www.mafengwo.cn/gonglve/mdd-mc-0-0-1.html#list'),
        (u'中国', u'宁夏', 'http://www.mafengwo.cn/gonglve/mdd-nx-0-0-1.html#list'),
        (u'中国', u'天津', 'http://www.mafengwo.cn/gonglve/mdd-tj-0-0-1.html#list'),
        (u'中国', u'西藏', 'http://www.mafengwo.cn/gonglve/mdd-xz-0-0-1.html#list'),
        (u'中国', u'陕西', 'http://www.mafengwo.cn/gonglve/mdd-s3x-0-0-1.html#list'),
    )

    HEADERS = {
        'Host' : 'www.mafengwo.cn',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    def start_requests(self):
        for gonglue_item in self.gonglue_api:
            meta = {}
            meta['main_class'] = gonglue_item[0]
            meta['second_class'] = gonglue_item[1]
            yield Request(gonglue_item[2], meta=meta, headers=self.HEADERS, dont_filter=True)

    def parse(self, response):
        meta = response.meta
        selector = Selector(response)
        for gonglue in selector.xpath('//div[@class="gl_list"]'):
            gonglue_name = gonglue.xpath('./a/@title').extract_first()
            url = 'http://www.mafengwo.cn' + gonglue.xpath('./a/@href').extract_first()
            update_time = gonglue.xpath('./div[@class="update_time"]/text()').extract_first().replace(u'更新时间：', ' 00:00:00')
            download_count = gonglue.xpath('./div[@class="down_cout"]/p/text()').extract_first().replace(u'人下载', '')
            result = {
                'main_class' : meta['main_class'],
                'second_class' : meta['second_class'],
                'gonglue_name' : gonglue_name,
                'date' : update_time,
                'download_count' : download_count,
                'url' : url
            }
            self.logger.info('mafengwo gonglue : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))


