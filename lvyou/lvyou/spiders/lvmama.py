# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
import json
import re

class LvmamaJingdianSpider(scrapy.Spider):
    name = "lvmama_jingdian"

    jingdian_api = (
        (u'亚洲', u'中国', '/lvyou/scenery/d-zhongguo3548.html', '3548'),
        (u'亚洲', u'泰国', '/lvyou/scenery/d-taiguo3542.html', '3542'),
        (u'亚洲', u'韩国', '/lvyou/scenery/d-hanguo3544.html', '3544'),
        (u'亚洲', u'日本', '/lvyou/scenery/d-riben3543.html', '3543'),
        (u'亚洲', u'新加坡', '/lvyou/scenery/d-xinjiapo3569.html', '3569'),
        (u'亚洲', u'菲律宾', '/lvyou/scenery/d-feilvbin3576.html', '3576'),
        (u'亚洲', u'印度尼西亚', '/lvyou/scenery/d-yindunixiya3619.html', '3619'),
        (u'亚洲', u'马来西亚', '/lvyou/scenery/d-malaixiya3570.html', '3570'),
        (u'亚洲', u'柬埔寨', '/lvyou/scenery/d-jianpuzhai3623.html', '3623'),
        (u'亚洲', u'尼泊尔', '/lvyou/scenery/d-niboer3626.html', '3626'),
        (u'亚洲', u'越南', '/lvyou/scenery/d-yuenan3624.html', '3624'),
        (u'亚洲', u'马尔代夫', '/lvyou/scenery/d-maerdaifu3546.html', '3546'),
        (u'亚洲', u'阿联酋', '/lvyou/scenery/d-alianqiu3575.html', '3575'),
        (u'亚洲', u'土耳其', '/lvyou/scenery/d-tuerqi3574.html', '3574'),
        (u'亚洲', u'印度', '/lvyou/scenery/d-yindu3627.html', '3627'),
        (u'亚洲', u'缅甸', '/lvyou/scenery/d-miandian3872.html', '3872'),
        (u'亚洲', u'斯里兰卡', '/lvyou/scenery/d-sililanka3656.html', '3656'),
        (u'亚洲', u'朝鲜', '/lvyou/scenery/d-chaoxian3640.html', '3640'),
        (u'亚洲', u'老挝', '/lvyou/scenery/d-laowo3670.html', '3670'),
        (u'亚洲', u'文莱', '/lvyou/scenery/d-wenlai3616.html', '3616'),
        (u'亚洲', u'以色列', '/lvyou/scenery/d-yiselie3631.html', '3631'),
        (u'亚洲', u'伊朗', '/lvyou/scenery/d-yilang203280.html', '203280'),
        (u'亚洲', u'沙特阿拉伯', '/lvyou/scenery/d-shatealabo203267.html', '203267'),
        (u'亚洲', u'哈萨克斯坦', '/lvyou/scenery/d-hasakesitan203251.html', '203251'),
        (u'亚洲', u'蒙古', '/lvyou/scenery/d-menggu203261.html', '203261'),
        (u'亚洲', u'不丹', '/lvyou/scenery/d-budan203246.html', '203246'),
        (u'亚洲', u'巴林', '/lvyou/scenery/d-balin203245.html', '203245'),
        (u'亚洲', u'伊拉克', '/lvyou/scenery/d-yilake203279.html', '203279'),
        (u'亚洲', u'叙利亚', '/lvyou/scenery/d-xuliya203276.html', '203276'),
        (u'亚洲', u'阿富汗', '/lvyou/scenery/d-afuhan203239.html', '203239'),
        (u'亚洲', u'卡塔尔', '/lvyou/scenery/d-kataer203255.html', '203255'),
        (u'亚洲', u'巴基斯坦', '/lvyou/scenery/d-bajisitan203243.html', '203243'),
        (u'亚洲', u'约旦', '/lvyou/scenery/d-yuedan3914.html', '3914'),
        (u'亚洲', u'孟加拉国', '/lvyou/scenery/d-mengjialaguo203262.html', '203262'),
        (u'亚洲', u'乌兹别克斯坦', '/lvyou/scenery/d-wuzibiekesitan203274.html', '203274'),
        (u'亚洲', u'阿曼', '/lvyou/scenery/d-aman203241.html', '203241'),
        (u'亚洲', u'也门', '/lvyou/scenery/d-yemen203278.html', '203278'),
        (u'亚洲', u'吉尔吉斯斯坦', '/lvyou/scenery/d-jierjisisitan203253.html', '203253'),
        (u'亚洲', u'格鲁吉亚', '/lvyou/scenery/d-gelujiya203250.html', '203250'),
        (u'亚洲', u'科威特', '/lvyou/scenery/d-keweite203256.html', '203256'),
        (u'亚洲', u'土库曼斯坦', '/lvyou/scenery/d-tukumansitan203272.html', '203272'),
        (u'亚洲', u'巴勒斯坦', '/lvyou/scenery/d-balesitan203244.html', '203244'),
        (u'亚洲', u'黎巴嫩', '/lvyou/scenery/d-libanen203258.html', '203258'),
        (u'亚洲', u'塔吉克斯坦', '/lvyou/scenery/d-tajikesitan203269.html', '203269'),
        (u'亚洲', u'塞浦路斯', '/lvyou/scenery/d-saipulusi203266.html', '203266'),
        (u'亚洲', u'东帝汶', '/lvyou/scenery/d-dongdiwen203248.html', '203248'),
        (u'亚洲', u'阿塞拜疆', '/lvyou/scenery/d-asaibaijiang203242.html', '203242'),
        (u'亚洲', u'亚美尼亚', '/lvyou/scenery/d-yameiniya203277.html', '203277'),
        (u'欧洲', u'意大利', '/lvyou/scenery/d-yidali3562.html', '3562'),
        (u'欧洲', u'法国', '/lvyou/scenery/d-faguo3559.html', '3559'),
        (u'欧洲', u'英国', '/lvyou/scenery/d-yingguo3558.html', '3558'),
        (u'欧洲', u'西班牙', '/lvyou/scenery/d-xibanya3636.html', '3636'),
        (u'欧洲', u'荷兰', '/lvyou/scenery/d-helan3635.html', '3635'),
        (u'欧洲', u'德国', '/lvyou/scenery/d-deguo3561.html', '3561'),
        (u'欧洲', u'希腊', '/lvyou/scenery/d-xila3634.html', '3634'),
        (u'欧洲', u'奥地利', '/lvyou/scenery/d-aodili3637.html', '3637'),
        (u'欧洲', u'俄罗斯', '/lvyou/scenery/d-eluosi3638.html', '3638'),
        (u'欧洲', u'丹麦', '/lvyou/scenery/d-danmai3763.html', '3763'),
        (u'欧洲', u'瑞士', '/lvyou/scenery/d-ruishi3560.html', '3560'),
        (u'欧洲', u'梵蒂冈', '/lvyou/scenery/d-fandigang3790.html', '3790'),
        (u'欧洲', u'比利时', '/lvyou/scenery/d-bilishi3753.html', '3753'),
        (u'欧洲', u'卢森堡', '/lvyou/scenery/d-lusenbao203310.html', '203310'),
        (u'欧洲', u'捷克', '/lvyou/scenery/d-jieke3795.html', '3795'),
        (u'欧洲', u'瑞典', '/lvyou/scenery/d-ruidian3617.html', '3617'),
        (u'欧洲', u'芬兰', '/lvyou/scenery/d-fenlan3615.html', '3615'),
        (u'欧洲', u'摩纳哥', '/lvyou/scenery/d-monage3797.html', '3797'),
        (u'欧洲', u'挪威', '/lvyou/scenery/d-nuowei3618.html', '3618'),
        (u'欧洲', u'列支敦士登', '/lvyou/scenery/d-liezhidunshideng3796.html', '3796'),
        (u'欧洲', u'匈牙利', '/lvyou/scenery/d-xiongyali3799.html', '3799'),
        (u'欧洲', u'葡萄牙', '/lvyou/scenery/d-putaoya3798.html', '3798'),
        (u'欧洲', u'波兰', '/lvyou/scenery/d-bolan203296.html', '203296'),
        (u'欧洲', u'斯洛伐克', '/lvyou/scenery/d-siluofake203322.html', '203322'),
        (u'欧洲', u'爱尔兰', '/lvyou/scenery/d-aierlan3913.html', '3913'),
        (u'欧洲', u'冰岛', '/lvyou/scenery/d-bingdao3614.html', '3614'),
        (u'欧洲', u'克罗地亚', '/lvyou/scenery/d-keluodiya203306.html', '203306'),
        (u'欧洲', u'乌克兰', '/lvyou/scenery/d-wukelan203324.html', '203324'),
        (u'欧洲', u'斯洛文尼亚', '/lvyou/scenery/d-siluowenniya203323.html', '203323'),
        (u'欧洲', u'保加利亚', '/lvyou/scenery/d-baojialiya203292.html', '203292'),
        (u'欧洲', u'罗马尼亚', '/lvyou/scenery/d-luomaniya203311.html', '203311'),
        (u'欧洲', u'塞尔维亚', '/lvyou/scenery/d-saierweiya203320.html', '203320'),
        (u'欧洲', u'马其顿', '/lvyou/scenery/d-maqidun203313.html', '203313'),
        (u'欧洲', u'黑山', '/lvyou/scenery/d-heishan203304.html', '203304'),
        (u'欧洲', u'波黑', '/lvyou/scenery/d-bohei203295.html', '203295'),
        (u'欧洲', u'阿尔巴尼亚', '/lvyou/scenery/d-aerbaniya203286.html', '203286'),
        (u'欧洲', u'爱沙尼亚', '/lvyou/scenery/d-aishaniya3750.html', '3750'),
        (u'欧洲', u'拉脱维亚', '/lvyou/scenery/d-latuoweiya203307.html', '203307'),
        (u'欧洲', u'圣马力诺', '/lvyou/scenery/d-shengmalinuo203321.html', '203321'),
        (u'欧洲', u'马耳他', '/lvyou/scenery/d-maerta203312.html', '203312'),
        (u'欧洲', u'立陶宛', '/lvyou/scenery/d-litaowan203308.html', '203308'),
        (u'欧洲', u'安道尔', '/lvyou/scenery/d-andaoer203289.html', '203289'),
        (u'欧洲', u'白俄罗斯', '/lvyou/scenery/d-baieluosi203291.html', '203291'),
        (u'欧洲', u'摩尔多瓦', '/lvyou/scenery/d-moerduowa203314.html', '203314'),
        (u'北美洲', u'美国', '/lvyou/scenery/d-meiguo3571.html', '3571'),
        (u'北美洲', u'加拿大', '/lvyou/scenery/d-jianada3651.html', '3651'),
        (u'北美洲', u'古巴', '/lvyou/scenery/d-guba3702.html', '3702'),
        (u'北美洲', u'墨西哥', '/lvyou/scenery/d-moxige3701.html', '3701'),
        (u'北美洲', u'海地', '/lvyou/scenery/d-haidi203423.html', '203423'),
        (u'北美洲', u'巴拿马', '/lvyou/scenery/d-banama203415.html', '203415'),
        (u'北美洲', u'巴哈马', '/lvyou/scenery/d-bahama203414.html', '203414'),
        (u'北美洲', u'波多黎各', '/lvyou/scenery/d-boduolige203416.html', '203416'),
        (u'北美洲', u'牙买加', '/lvyou/scenery/d-yamaijia203436.html', '203436'),
        (u'北美洲', u'哥斯达黎加', '/lvyou/scenery/d-gesidalijia203420.html', '203420'),
        (u'北美洲', u'多米尼加', '/lvyou/scenery/d-duominijia203418.html', '203418'),
        (u'北美洲', u'洪都拉斯', '/lvyou/scenery/d-hongdulasi203425.html', '203425'),
        (u'北美洲', u'危地马拉', '/lvyou/scenery/d-weidimala203435.html', '203435'),
        (u'北美洲', u'特立尼达和多巴哥', '/lvyou/scenery/d-telinidaheduobage203434.html', '203434'),
        (u'北美洲', u'安提瓜和巴布达', '/lvyou/scenery/d-antiguahebabuda203412.html', '203412'),
        (u'北美洲', u'伯利兹', '/lvyou/scenery/d-bolizi203417.html', '203417'),
        (u'北美洲', u'尼加拉瓜', '/lvyou/scenery/d-nijialagua203429.html', '203429'),
        (u'北美洲', u'巴巴多斯', '/lvyou/scenery/d-babaduosi203413.html', '203413'),
        (u'北美洲', u'多米尼克', '/lvyou/scenery/d-duominike203419.html', '203419'),
        (u'北美洲', u'圣文森特和格林纳丁斯', '/lvyou/scenery/d-shengwensentehegelinnadingsi203433.html', '203433'),
        (u'北美洲', u'格林纳达', '/lvyou/scenery/d-gelinnada203421.html', '203421'),
        (u'北美洲', u'萨尔瓦多', '/lvyou/scenery/d-saerwaduo203430.html', '203430'),
        (u'北美洲', u'圣卢西亚', '/lvyou/scenery/d-shengluxiya203432.html', '203432'),
        (u'北美洲', u'圣基茨和尼维斯', '/lvyou/scenery/d-shengjiciheniweisi203431.html', '203431'),
        (u'南美洲', u'巴西', '/lvyou/scenery/d-baxi3703.html', '3703'),
        (u'南美洲', u'阿根廷', '/lvyou/scenery/d-agenting3704.html', '3704'),
        (u'南美洲', u'玻利维亚', '/lvyou/scenery/d-boliweiya203333.html', '203333'),
        (u'南美洲', u'智利', '/lvyou/scenery/d-zhili3705.html', '3705'),
        (u'南美洲', u'秘鲁', '/lvyou/scenery/d-bilu3700.html', '3700'),
        (u'南美洲', u'厄瓜多尔', '/lvyou/scenery/d-eguaduoer203334.html', '203334'),
        (u'南美洲', u'哥伦比亚', '/lvyou/scenery/d-gelunbiya203335.html', '203335'),
        (u'南美洲', u'德雷克海峡', '/lvyou/scenery/d-deleikehaixia250318.html', '250318'),
        (u'南美洲', u'利马尔水道', '/lvyou/scenery/d-limaershuidao250321.html', '250321'),
        (u'南美洲', u'尼高港', '/lvyou/scenery/d-nigaogang250322.html', '250322'),
        (u'南美洲', u'南瑟特兰群岛', '/lvyou/scenery/d-nansetelanqundao250323.html', '250323'),
        (u'南美洲', u'委内瑞拉', '/lvyou/scenery/d-weineiruila203339.html', '203339'),
        (u'南美洲', u'乌拉圭', '/lvyou/scenery/d-wulagui203340.html', '203340'),
        (u'南美洲', u'巴拉圭', '/lvyou/scenery/d-balagui203331.html', '203331'),
        (u'南美洲', u'圭亚那', '/lvyou/scenery/d-guiyana203336.html', '203336'),
        (u'南美洲', u'苏里南', '/lvyou/scenery/d-sulinan203338.html', '203338'),
        (u'大洋洲', u'澳大利亚', '/lvyou/scenery/d-aodaliya3596.html', '3596'),
        (u'大洋洲', u'新西兰', '/lvyou/scenery/d-xinxilan3597.html', '3597'),
        (u'大洋洲', u'斐济', '/lvyou/scenery/d-feiji3628.html', '3628'),
        (u'大洋洲', u'帕劳', '/lvyou/scenery/d-palao3983.html', '3983'),
        (u'大洋洲', u'库克群岛', '/lvyou/scenery/d-kukequndao203400.html', '203400'),
        (u'大洋洲', u'瓦努阿图', '/lvyou/scenery/d-wanuatu203410.html', '203410'),
        (u'大洋洲', u'巴布亚新几内亚', '/lvyou/scenery/d-babuyaxinjineiya203397.html', '203397'),
        (u'大洋洲', u'萨摩亚', '/lvyou/scenery/d-samoya203406.html', '203406'),
        (u'大洋洲', u'马绍尔群岛', '/lvyou/scenery/d-mashaoerqundao203401.html', '203401'),
        (u'大洋洲', u'汤加', '/lvyou/scenery/d-tangjia203408.html', '203408'),
        (u'大洋洲', u'密克罗尼西亚', '/lvyou/scenery/d-mikeluonixiya203402.html', '203402'),
        (u'大洋洲', u'基里巴斯', '/lvyou/scenery/d-jilibasi203399.html', '203399'),
        (u'大洋洲', u'纽埃', '/lvyou/scenery/d-niuai203404.html', '203404'),
        (u'大洋洲', u'所罗门群岛', '/lvyou/scenery/d-suoluomenqundao203407.html', '203407'),
        (u'大洋洲', u'瑙鲁', '/lvyou/scenery/d-naolu203403.html', '203403'),
        (u'大洋洲', u'图瓦卢', '/lvyou/scenery/d-tuwalu203409.html', '203409'),
        (u'非洲', u'埃及', '/lvyou/scenery/d-aiji3572.html', '3572'),
        (u'非洲', u'南非', '/lvyou/scenery/d-nanfei3573.html', '3573'),
        (u'非洲', u'毛里求斯', '/lvyou/scenery/d-maoliqiusi3629.html', '3629'),
        (u'非洲', u'肯尼亚', '/lvyou/scenery/d-kenniya3630.html', '3630'),
        (u'非洲', u'塞舌尔', '/lvyou/scenery/d-saisheer3707.html', '3707'),
        (u'非洲', u'马达加斯加', '/lvyou/scenery/d-madajiasijia3741.html', '3741'),
        (u'非洲', u'摩洛哥', '/lvyou/scenery/d-moluoge3650.html', '3650'),
        (u'非洲', u'津巴布韦', '/lvyou/scenery/d-jinbabuwei203362.html', '203362'),
        (u'非洲', u'莫桑比克', '/lvyou/scenery/d-mosangbike203377.html', '203377'),
        (u'非洲', u'厄立特里亚', '/lvyou/scenery/d-eliteliya203352.html', '203352'),
        (u'非洲', u'埃塞俄比亚', '/lvyou/scenery/d-aisaiebiya203344.html', '203344'),
        (u'非洲', u'坦桑尼亚', '/lvyou/scenery/d-tansangniya203390.html', '203390'),
        (u'非洲', u'突尼斯', '/lvyou/scenery/d-tunisi3911.html', '3911'),
        (u'非洲', u'尼日利亚', '/lvyou/scenery/d-niriliya203382.html', '203382'),
        (u'非洲', u'喀麦隆', '/lvyou/scenery/d-kamailong203363.html', '203363'),
        (u'非洲', u'阿尔及利亚', '/lvyou/scenery/d-aerjiliya203342.html', '203342'),
        (u'非洲', u'加纳', '/lvyou/scenery/d-jiana203360.html', '203360'),
        (u'非洲', u'索马里', '/lvyou/scenery/d-suomali203389.html', '203389'),
        (u'非洲', u'赞比亚', '/lvyou/scenery/d-zanbiya203393.html', '203393'),
        (u'非洲', u'苏丹', '/lvyou/scenery/d-sudan203388.html', '203388'),
    )

    gonglue_api = (
        (u'热门游记', 'http://travel.qunar.com/travelbook/list.htm?page=%d&order=hot_heat', 9999),
        (u'精华游记', 'http://travel.qunar.com/travelbook/list.htm?page=%d&order=elite_ctime', 717),
        (u'行程计划', 'http://travel.qunar.com/travelbook/list.htm?page=%d&order=start_heat', 9999),
    )

    HEADERS = {
        'Host' : 'www.lvmama.com',
        'Cache-Control' : 'max-age=0',
        'Accept' : 'application/json, text/javascript, */*; q=0.01',
        'Origin' : 'http://www.lvmama.com',
        'X-Requested-With' : 'XMLHttpRequest',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2'
    }

    jingdian_post_api = 'http://www.lvmama.com/lvyou/dest_content/AjaxGetViewSpotList'

    def __gen_request(self, meta, page, dest_id, request_uri, callback):
        formdata = {
            'page' : str(page),
            'dest_id' : dest_id,
            'search_key' : '',
            'request_uri' : request_uri,
            'type' : 'scenery'
        }
        return FormRequest(self.jingdian_post_api, headers=self.HEADERS, formdata=formdata, meta=meta, callback=callback)

    def start_requests(self):
        for jingdian_item in self.jingdian_api:
            meta = {}
            meta['main_class'] = jingdian_item[0]
            meta['second_class'] = jingdian_item[1]
            meta['request_uri'] = jingdian_item[2]
            meta['dest_id'] = jingdian_item[3]
            meta['first_page'] = True
            referer = 'http://www.lvmama.com' + jingdian_item[2]
            meta['referer'] = referer
            self.HEADERS.update({'Referer' : referer})
            yield self.__gen_request(meta, 1, jingdian_item[3], jingdian_item[2], self.parse)

    def parse(self, response):
        meta = response.meta.copy()
        try:
            jingdian_data = json.loads(response.body_as_unicode())
        except Exception:
            self.logger.error('invalid result for lvmama jingdian')
            return
        else:
            if jingdian_data.get('code') != 200:
                self.logger.error('invalid result for lvmama jingdian')
                return
            html = jingdian_data.get('data', {}).get('html')
            selector = Selector(text=html)
            for jingdian in selector.xpath('//dl[@class="has_id poi_price"]'):
                name = jingdian.xpath('./dd/h6/a/text()').extract_first()
                jiaoyin_count = jingdian.xpath('./dd/p[@class="city_info"]/span/text()').extract_first()
                url = jingdian.xpath('./dd/h6/a/@href').extract_first()
                result = {
                    'main_class' : meta['main_class'],
                    'second_class' : meta['second_class'],
                    'jingdian_name' : name,
                    'jiaoyin_count' : jiaoyin_count,
                    'url' : url
                }
                self.logger.info('lvmama jingdian : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))

            # deal with more pages
            if meta.get('first_page'):
                del meta['first_page']
                page_links = selector.xpath('//div[@class="wy_state_page"]/p/a')
                pages = None
                if len(page_links) > 2:
                    pages = page_links[-2].xpath('./text()').extract_first()
                if pages:
                    for page in range(int(pages)-1):
                        self.HEADERS.update({'Referer' : meta['referer']})
                        yield self.__gen_request(meta, page+2, meta['dest_id'], meta['request_uri'], self.parse)
                else:
                    self.logger.error('failed to get pages for item : %s' % response.url)


class LvmamaBBSSpider(scrapy.Spider):
    name = 'lvmama_bbs'

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
                return

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


