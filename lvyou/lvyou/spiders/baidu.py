# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
import time
from datetime import datetime

class BaiduGonglueSpider(scrapy.Spider):
    name = "baidu_gonglue"

    gonglue_api = 'http://lvyou.baidu.com/destination/ajax/books?format=ajax&pn=%d&rn=16&type=0&keywords=&t=%d'

    HEADERS = {
        'Host' : 'lvyou.baidu.com',
        'X-Requested-With' : 'XMLHttpRequest',
        'Referer' : 'http://lvyou.baidu.com/guide/',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
    }

    def start_requests(self):
        for page in range(27):
            cur_time = int(time.time())
            page = (page+1)*16
            yield Request(self.gonglue_api % (page, cur_time))

    def __seconds_format(self, time_s, format_s='%Y-%m-%d %H:%M:%S'):
        return datetime.fromtimestamp(time_s).strftime(format_s)

    def parse(self, response):
        try:
            data = json.loads(response.body_as_unicode())
        except Exception:
            self.logger.error('invalid result')
            return
        else:
            if data.get('errno') != 0:
                self.logger.error('invalid result')
                return
            for book in data.get('data', {}).get('books_list', []):
                name = book.get('gname')
                date = self.__seconds_format(float(book.get('update_time')))
                download_count = book.get('download_total')
                result = {
                    'name' : name,
                    'date' : date,
                    'download_count' : download_count
                }
                self.logger.info('tripadvisor mudidi : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))

class BaiduMudidiGonglueSpider(scrapy.Spider):
    name = 'baidumudidi_gonglue'

    apis = (
        (u'亚洲', u'中国', u'拉萨', u'lasa'),
        (u'亚洲', u'中国', u'丽江', u'lijiang'),
        (u'亚洲', u'中国', u'成都', u'chengdu'),
        (u'亚洲', u'中国', u'九寨沟', u'jiuzhaigou'),
        (u'亚洲', u'中国', u'西双版纳', u'xishuangbanna'),
        (u'亚洲', u'中国', u'黔东南', u'qiandongnan'),
        (u'亚洲', u'中国', u'西安', u'xian'),
        (u'亚洲', u'中国', u'青海湖', u'qinghaihu'),
        (u'亚洲', u'中国', u'敦煌', u'dunhuang'),
        (u'亚洲', u'中国', u'银川', u'yinchuan'),
        (u'亚洲', u'中国', u'乌鲁木齐', u'wulumuqi'),
        (u'亚洲', u'中国', u'甘南', u'gannan'),
        (u'亚洲', u'中国', u'厦门', u'xiamen'),
        (u'亚洲', u'中国', u'杭州', u'hangzhou'),
        (u'亚洲', u'中国', u'黄山', u'huangshan'),
        (u'亚洲', u'中国', u'青岛', u'qingdao'),
        (u'亚洲', u'中国', u'乌镇', u'wuzhen'),
        (u'亚洲', u'中国', u'上海', u'shanghai'),
        (u'亚洲', u'中国', u'扬州', u'yangzhou'),
        (u'亚洲', u'中国', u'三亚', u'sanya'),
        (u'亚洲', u'中国', u'桂林', u'guilin'),
        (u'亚洲', u'中国', u'广州', u'guangzhou'),
        (u'亚洲', u'中国', u'汉口', u'haikou'),
        (u'亚洲', u'中国', u'南宁', u'nanning'),
        (u'亚洲', u'中国', u'珠海', u'zhuhai'),
        (u'亚洲', u'中国', u'张家界', u'zhangjiajie'),
        (u'亚洲', u'中国', u'武汉', u'wuhan'),
        (u'亚洲', u'中国', u'武当山', u'wudangshan'),
        (u'亚洲', u'中国', u'长沙', u'changsha'),
        (u'亚洲', u'中国', u'凤凰', u'fenghuang'),
        (u'亚洲', u'中国', u'洛阳', u'luoyang'),
        (u'亚洲', u'中国', u'开封', u'kaifeng'),
        (u'亚洲', u'中国', u'北京', u'beijing'),
        (u'亚洲', u'中国', u'秦皇岛', u'qinhuangdao'),
        (u'亚洲', u'中国', u'天津', u'tianjin'),
        (u'亚洲', u'中国', u'五台山', u'wutaishan'),
        (u'亚洲', u'中国', u'成都', u'chengde'),
        (u'亚洲', u'中国', u'平遥', u'pingyao'),
        (u'亚洲', u'中国', u'唐山', u'tangshan'),
        (u'亚洲', u'中国', u'长白山', u'changbaishan'),
        (u'亚洲', u'中国', u'沈阳', u'shenyang'),
        (u'亚洲', u'中国', u'哈尔滨', u'haerbin'),
        (u'亚洲', u'中国', u'长春', u'changchun'),
        (u'亚洲', u'中国', u'呼伦贝尔', u'hulunbeier'),
        (u'亚洲', u'中国', u'漠河', u'mohe'),
        (u'亚洲', u'中国', u'香港', u'xianggang'),
        (u'亚洲', u'中国', u'台北', u'taibei'),
        (u'亚洲', u'中国', u'澳门', u'aomen'),
        (u'亚洲', u'中国', u'台中', u'taizhong'),
        (u'亚洲', u'中国', u'垦丁', u'kending'),
        (u'亚洲', u'中国', u'阿里山', u'alishan'),
        (u'亚洲', u'中国', u'台南', u'tainan'),
        (u'亚洲', u'泰国', u'', u'taiguo'),
        (u'亚洲', u'巴厘岛', u'', u'balidao'),
        (u'亚洲', u'新加坡', u'', u'xinjiapo'),
        (u'亚洲', u'越南', u'', u'yuenan'),
        (u'亚洲', u'柬埔寨', u'', u'jianpuzhai'),
        (u'亚洲', u'普吉岛', u'', u'pujidao'),
        (u'亚洲', u'日本', u'', u'riben'),
        (u'亚洲', u'韩国', u'', u'hanguo'),
        (u'亚洲', u'朝鲜', u'', u'chaoxian'),
        (u'亚洲', u'济州岛', u'', u'jizhoudao'),
        (u'亚洲', u'首尔', u'', u'shouer'),
        (u'亚洲', u'北海道', u'', u'beihaidao'),
        (u'亚洲', u'东京', u'', u'dongjing'),
        (u'亚洲', u'马尔代夫', u'', u'maerdaifu'),
        (u'亚洲', u'尼泊尔', u'', u'niboer'),
        (u'亚洲', u'不丹', u'', u'budan'),
        (u'亚洲', u'印度', u'', u'yindu'),
        (u'亚洲', u'斯里兰卡', u'', u'sililanka'),
        (u'亚洲', u'迪拜', u'', u'dibai'),
        (u'亚洲', u'以色列', u'', u'yiselie'),
        (u'亚洲', u'以色列死海', u'', u'yiseliesihai'),
        (u'亚洲', u'伊朗', u'', u'yilang'),
        (u'亚洲', u'约旦', u'', u'yuedan'),
        (u'亚洲', u'沙特阿拉伯', u'', u'shatealabo'),
        (u'欧洲', u'法国', u'', u'faguo'),
        (u'欧洲', u'英国', u'', u'yingguo'),
        (u'欧洲', u'巴黎', u'', u'bali'),
        (u'欧洲', u'荷兰', u'', u'helan'),
        (u'欧洲', u'爱尔兰', u'', u'aierlan'),
        (u'欧洲', u'比利时', u'', u'bilishi'),
        (u'欧洲', u'卢森堡', u'', u'lusenbao'),
        (u'欧洲', u'希腊', u'', u'xila'),
        (u'欧洲', u'意大利', u'', u'yidali'),
        (u'欧洲', u'西班牙', u'', u'xibanya'),
        (u'欧洲', u'爱琴海', u'', u'aiqinhai'),
        (u'欧洲', u'威尼斯', u'', u'weinisi'),
        (u'欧洲', u'罗马', u'', u'luoma'),
        (u'欧洲', u'瑞士', u'', u'ruishi'),
        (u'欧洲', u'德国', u'', u'deguo'),
        (u'欧洲', u'奥地利', u'', u'aodili'),
        (u'欧洲', u'捷克', u'', u'jieke'),
        (u'欧洲', u'匈牙利', u'', u'xiongyali'),
        (u'欧洲', u'德国', u'慕尼黑', u'munihei'),
        (u'欧洲', u'波兰', u'', u'bolan'),
        (u'欧洲', u'冰岛', u'', u'bingdao'),
        (u'欧洲', u'瑞典', u'', u'ruidian'),
        (u'欧洲', u'芬兰', u'', u'fenlan'),
        (u'欧洲', u'丹麦', u'', u'danmai'),
        (u'欧洲', u'挪威', u'', u'nuowei'),
        (u'欧洲', u'荷兰', u'哥本哈根', u'gebenhagen'),
        (u'欧洲', u'奥斯陆', u'', u'aosilu'),
        (u'欧洲', u'俄罗斯', u'', u'eluosi'),
        (u'欧洲', u'土耳其', u'', u'tuerqi'),
        (u'欧洲', u'乌克兰', u'', u'wukelan'),
        (u'欧洲', u'俄罗斯', u'莫斯科', u'mosike'),
        (u'欧洲', u'拉托维亚', u'', u'latuoweiya'),
        (u'大洋洲', u'澳大利亚', u'悉尼', u'xini'),
        (u'大洋洲', u'澳大利亚', u'墨尔本', u'moerben'),
        (u'大洋洲', u'澳大利亚', u'大堡礁', u'dabaojiao'),
        (u'大洋洲', u'澳大利亚', u'布里斯班', u'bulisiban'),
        (u'大洋洲', u'澳大利亚', u'昆士兰黄金海岸', u'kunshilanhuangjinhaianyouji'),
        (u'大洋洲', u'新西兰', u'奥克兰', u'http:lvyou.baidu.comaokelan'),
        (u'大洋洲', u'新西兰', u'惠灵顿', u'huilingdun'),
        (u'大洋洲', u'新西兰', u'基督城', u'jiducheng'),
        (u'大洋洲', u'新西兰', u'皇后镇', u'huanghouzhen'),
        (u'大洋洲', u'夏威夷', u'', u'xiaweiyi'),
        (u'大洋洲', u'塞班岛', u'', u'saibandao'),
        (u'大洋洲', u'飞机', u'', u'feiji'),
        (u'大洋洲', u'关岛', u'', u'guandao'),
        (u'大洋洲', u'大溪地', u'', u'daxidi'),
        (u'大洋洲', u'帕劳', u'', u'palao'),
        (u'北美洲', u'美国', u'拉斯维加斯', u'lasiweijiasi'),
        (u'北美洲', u'美国', u'纽约', u'niuyue'),
        (u'北美洲', u'美国', u'旧金山', u'jiujinshan'),
        (u'北美洲', u'美国', u'洛杉矶', u'luoshanji'),
        (u'北美洲', u'美国', u'费城', u'feicheng'),
        (u'北美洲', u'加拿大', u'温哥华', u'wengehua'),
        (u'北美洲', u'加拿大', u'多伦多', u'duolunduo'),
        (u'北美洲', u'加拿大', u'蒙特利尔', u'mengtelier'),
        (u'北美洲', u'加拿大', u'魁北克', u'kuibeike'),
        (u'北美洲', u'加拿大', u'班夫', u'banfu'),
        (u'北美洲', u'古巴', u'', u'guba'),
        (u'北美洲', u'墨西哥', u'', u'moxige'),
        (u'北美洲', u'巴哈马', u'', u'bahama'),
        (u'北美洲', u'牙买加', u'', u'yamaijia'),
        (u'北美洲', u'哥斯达黎加', u'', u'gesidalijia'),
        (u'南美洲', u'巴西', u'里约热内卢', u'liyuereneilu'),
        (u'南美洲', u'巴西', u'圣保罗', u'baxishengbaoluo'),
        (u'南美洲', u'巴西', u'巴西利亚', u'baxiliya'),
        (u'南美洲', u'巴西', u'伊瓜苏', u'yiguasu'),
        (u'南美洲', u'阿根廷', u'布宜诺斯艾利斯', u'buyinuosiailisi'),
        (u'南美洲', u'阿根廷', u'乌斯怀亚', u'wusihuaiya'),
        (u'南美洲', u'阿根廷', u'福克兰群岛', u'fukelan'),
        (u'南美洲', u'玻利维亚', u'', u'boliweiya'),
        (u'南美洲', u'秘鲁', u'', u'bilu'),
        (u'南美洲', u'智利', u'', u'zhili'),
        (u'南美洲', u'委内瑞拉', u'', u'weineiruila'),
        (u'南美洲', u'哥伦比亚', u'', u'gelunbiya'),
        (u'非洲', u'埃及', u'', u'aiji'),
        (u'非洲', u'摩洛哥', u'', u'moluoge'),
        (u'非洲', u'突尼斯', u'', u'tunisi'),
        (u'非洲', u'利比亚', u'', u'libiya'),
        (u'非洲', u'阿尔及利亚', u'', u'aerjiliya'),
        (u'非洲', u'毛里求斯', u'', u'maoliqiusi'),
        (u'非洲', u'南非', u'', u'nanfei'),
        (u'非洲', u'马达加斯加', u'', u'madajiasijia'),
        (u'非洲', u'赞比亚', u'', u'zanbiya'),
        (u'非洲', u'肯尼亚', u'', u'kenniya'),
        (u'非洲', u'塞舌尔', u'', u'saisheer'),
        (u'非洲', u'坦桑尼亚', u'', u'tansangniya'),
        (u'非洲', u'埃塞俄比亚', u'', u'aisaiebiya'),
        (u'非洲', u'喀麦隆', u'', u'kamailong'),
        (u'非洲', u'尼日利亚', u'', u'niriliya'),
        (u'非洲', u'加纳', u'', u'jiana'),
        (u'非洲', u'冈比亚', u'', u'gangbiya'),
        (u'非洲', u'科特迪瓦', u'', u'ketediwa'),
    )

    HEADERS = {
        'Host' : 'lvyou.baidu.com',
        'X-Requested-With' : 'XMLHttpRequest',
        'Referer' : 'http://lvyou.baidu.com/guide/',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
    }

    main_api = 'http://lvyou.baidu.com/search/ajax/search?format=ajax&pn=%d&surl=%s&rn=10&t=%d'

    def __get_current_time(self):
        return int(time.time()*1000)

    def start_requests(self):
        for api in self.apis:
            meta = {}
            meta['main_class'] = api[0]
            meta['second_class'] = api[1]
            meta['third_class'] = api[2]
            meta['first_page'] = True
            meta['surl'] = api[3]
            url = self.main_api % (0, api[3], self.__get_current_time())
            yield Request(url, headers=self.HEADERS, meta=meta, dont_filter=True, callback=self.parse_first_page)

    def parse_first_page(self, response):
        meta = response.meta.copy()
        try:
            data = json.loads(response.body_as_unicode())
        except Exception:
            self.logger.error('invalid result')
            return
        else:
            if data.get('errno') != 0:
                self.logger.error('invalid result')
                return

            search_res = data.get('data', {}).get('search_res', {})
            if not search_res:
                self.logger.error('invalid result')
                return

            costs = {}
            for cost in search_res.get('costs', []):
                costs[cost.get('id')] = cost.get('name')

            for item in search_res.get('notes_list', []):
                title = item.get('title')
                author = item.get('nickname')
                destinations = item.get('destinations')
                cost = costs.get(str(item.get('avg_cost')))
                view_count = item.get('view_count')
                comment_count = item.get('common_posts_count')
                favorite_count = item.get('favorite_count')
                days = item.get('days')
                result = {
                    'first_class' : meta['first_class'],
                    'second_class' : meta['second_class'],
                    'third_class' : meta['third_class'],
                    'title' : title,
                    'author' : author,
                    'destinations' : destinations,
                    'cost' : cost,
                    'view_count' : view_count,
                    'comment_count' : comment_count,
                    'favorite_count' : favorite_count,
                    'days' : days
                }
                self.logger.info('baidu mudidi gonglue : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))
            if meta.get('first_page'):
                meta['first_page'] = False
                pages = search_res.get('pagelist', [])[-1][0]/10
                for page in range(pages-1):
                    url = self.main_api % ((page+2)*10, meta['surl'], self.__get_current_time())
                    yield Request(url, headers=self.HEADERS, meta=meta, dont_filter=True, callback=self.parse_first_page)



