# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from utils.timeutil import get_current_date
from utils.htmlutils import remove_tags
import json

class TripAdvisorSpider(scrapy.Spider):
    name = "tripadvisor_mudidi"

    custom_settings = {
        'DOWNLOAD_DELAY' : 0.3
    }

    mudidi_api = (
        (u'亚洲', u'阿富汗', u'http://www.tripadvisor.cn/Tourism-g659499-Afghanistan-Vacations.html'),
        (u'亚洲', u'阿塞拜疆', u'http://www.tripadvisor.cn/Tourism-g293933-Azerbaijan-Vacations.html'),
        (u'亚洲', u'巴基斯坦', u'http://www.tripadvisor.cn/Tourism-g293959-Pakistan-Vacations.html'),
        (u'亚洲', u'不丹', u'http://www.tripadvisor.cn/Tourism-g293844-Bhutan-Vacations.html'),
        (u'亚洲', u'东帝汶', u'http://www.tripadvisor.cn/Tourism-g295117-East_Timor-Vacations.html'),
        (u'亚洲', u'菲律宾', u'http://www.tripadvisor.cn/Tourism-g294245-Philippines-Vacations.html'),
        (u'亚洲', u'韩国', u'http://www.tripadvisor.cn/Tourism-g294196-South_Korea-Vacations.html'),
        (u'亚洲', u'朝鲜', u'http://www.tripadvisor.cn/Tourism-g294443-North_Korea-Vacations.html'),
        (u'亚洲', u'哈萨克斯坦', u'http://www.tripadvisor.cn/Tourism-g293943-Kazakhstan-Vacations.html?pid=39631'),
        (u'亚洲', u'柬埔寨', u'http://www.tripadvisor.cn/Tourism-g293939-Cambodia-Vacations.html'),
        (u'亚洲', u'吉尔吉斯斯坦', u'http://www.tripadvisor.cn/Tourism-g293947-Kyrgyzstan-Vacations.html'),
        (u'亚洲', u'老挝', u'http://www.tripadvisor.cn/Tourism-g293949-Laos-Vacations.html'),
        (u'亚洲', u'马尔代夫', u'http://www.tripadvisor.cn/Tourism-g293953-Maldives-Vacations.html'),
        (u'亚洲', u'马来西亚', u'http://www.tripadvisor.cn/Tourism-g293951-Malaysia-Vacations.html'),
        (u'亚洲', u'亚美尼亚', u'http://www.tripadvisor.cn/Tourism-g293931-Armenia-Vacations.html'),
        (u'亚洲', u'孟加拉国', u'http://www.tripadvisor.cn/Tourism-g293935-Bangladesh-Vacations.html'),
        (u'亚洲', u'蒙古', u'http://www.tripadvisor.cn/Tourism-g293955-Mongolia-Vacations.html'),
        (u'亚洲', u'缅甸', u'http://www.tripadvisor.cn/Tourism-g294190-Myanmar-Vacations.html'),
        (u'亚洲', u'尼泊尔', u'http://www.tripadvisor.cn/Tourism-g293889-Nepal-Vacations.html'),
        (u'亚洲', u'日本', u'http://www.tripadvisor.cn/Tourism-g294232-Japan-Vacations.html'),
        (u'亚洲', u'斯里兰卡', u'http://www.tripadvisor.cn/Tourism-g293961-Sri_Lanka-Vacations.html'),
        (u'亚洲', u'泰国', u'http://www.tripadvisor.cn/Tourism-g293915-Thailand-Vacations.html'),
        (u'亚洲', u'台湾', u'http://www.tripadvisor.cn/Tourism-g293910-Taiwan-Vacations.html'),
        (u'亚洲', u'塔吉克斯坦', u'http://www.tripadvisor.cn/Tourism-g293963-Tajikistan-Vacations.html'),
        (u'亚洲', u'土库曼斯坦', u'http://www.tripadvisor.cn/Tourism-g293965-Turkmenistan-Vacations.html'),
        (u'亚洲', u'文莱达鲁萨兰', u'http://www.tripadvisor.cn/Tourism-g293937-Brunei_Darussalam-Vacations.html'),
        (u'亚洲', u'乌兹别克斯坦', u'http://www.tripadvisor.cn/Tourism-g293967-Uzbekistan-Vacations.html'),
        (u'亚洲', u'新加坡', u'http://www.tripadvisor.cn/Tourism-g294262-Singapore-Vacations.html'),
        (u'亚洲', u'印度尼西亚', u'http://www.tripadvisor.cn/Tourism-g294225-Indonesia-Vacations.html'),
        (u'亚洲', u'印度洋', u'http://www.tripadvisor.cn/Tourism-g670819-Indian_Ocean-Vacations.html'),
        (u'亚洲', u'印度', u'http://www.tripadvisor.cn/Tourism-g293860-India-Vacations.html'),
        (u'亚洲', u'越南', u'http://www.tripadvisor.cn/Tourism-g293921-Vietnam-Vacations.html'),
        (u'亚洲', u'中国', u'http://www.tripadvisor.cn/Tourism-g294211-China-Vacations.html'),
        (u'欧洲', u'爱尔兰', u'http://www.tripadvisor.cn/Tourism-g186591-Ireland-Vacations.html'),
        (u'欧洲', u'爱沙尼亚', u'http://www.tripadvisor.cn/Tourism-g274952-Estonia-Vacations.html'),
        (u'欧洲', u'奥地利', u'http://www.tripadvisor.cn/Tourism-g190410-Austria-Vacations.html'),
        (u'欧洲', u'保加利亚', u'http://www.tripadvisor.cn/Tourism-g294451-Bulgaria-Vacations.html'),
        (u'欧洲', u'比利时', u'http://www.tripadvisor.cn/Tourism-g188634-Belgium-Vacations.html'),
        (u'欧洲', u'冰岛', u'http://www.tripadvisor.cn/Tourism-g189952-Iceland-Vacations.html'),
        (u'欧洲', u'波兰', u'http://www.tripadvisor.cn/Tourism-g274723-Poland-Vacations.html'),
        (u'欧洲', u'丹麦', u'http://www.tripadvisor.cn/Tourism-g189512-Denmark-Vacations.html'),
        (u'欧洲', u'德国', u'http://www.tripadvisor.cn/Tourism-g187275-Germany-Vacations.html'),
        (u'欧洲', u'俄罗斯', u'http://www.tripadvisor.cn/Tourism-g294459-Russia-Vacations.html'),
        (u'欧洲', u'法国', u'http://www.tripadvisor.cn/Tourism-g187070-France-Vacations.html'),
        (u'欧洲', u'芬兰', u'http://www.tripadvisor.cn/Tourism-g189896-Finland-Vacations.html'),
        (u'欧洲', u'荷兰', u'http://www.tripadvisor.cn/Tourism-g188553-The_Netherlands-Vacations.html'),
        (u'欧洲', u'捷克共和国', u'http://www.tripadvisor.cn/Tourism-g274684-Czech_Republic-Vacations.html'),
        (u'欧洲', u'克罗地亚', u'http://www.tripadvisor.cn/Tourism-g294453-Croatia-Vacations.html'),
        (u'欧洲', u'拉脱维亚', u'http://www.tripadvisor.cn/Tourism-g274960-Latvia-Vacations.html'),
        (u'欧洲', u'立陶宛', u'http://www.tripadvisor.cn/Tourism-g274947-Lithuania-Vacations.html'),
        (u'欧洲', u'罗马尼亚', u'http://www.tripadvisor.cn/Tourism-g294457-Romania-Vacations.html'),
        (u'欧洲', u'卢森堡', u'http://www.tripadvisor.cn/Tourism-g190340-Luxembourg-Vacations.html'),
        (u'欧洲', u'马耳他', u'http://www.tripadvisor.cn/Tourism-g190311-Malta-Vacations.html'),
        (u'欧洲', u'摩纳哥', u'http://www.tripadvisor.cn/Tourism-g190405-Monaco-Vacations.html'),
        (u'欧洲', u'挪威', u'http://www.tripadvisor.cn/Tourism-g190455-Norway-Vacations.html'),
        (u'欧洲', u'葡萄牙', u'http://www.tripadvisor.cn/Tourism-g189100-Portugal-Vacations.html'),
        (u'欧洲', u'瑞典', u'http://www.tripadvisor.cn/Tourism-g189806-Sweden-Vacations.html'),
        (u'欧洲', u'瑞士', u'http://www.tripadvisor.cn/Tourism-g188045-Switzerland-Vacations.html'),
        (u'欧洲', u'塞尔维亚', u'http://www.tripadvisor.cn/Tourism-g294471-Serbia-Vacations.html'),
        (u'欧洲', u'塞浦路斯', u'http://www.tripadvisor.cn/Tourism-g190372-Cyprus-Vacations.html'),
        (u'欧洲', u'斯洛文尼亚', u'http://www.tripadvisor.cn/Tourism-g274862-Slovenia-Vacations.html'),
        (u'欧洲', u'斯洛伐克', u'http://www.tripadvisor.cn/Tourism-g274922-Slovakia-Vacations.html'),
        (u'欧洲', u'土耳其', u'http://www.tripadvisor.cn/Tourism-g293969-Turkey-Vacations.html'),
        (u'欧洲', u'乌克兰', u'http://www.tripadvisor.cn/Tourism-g294473-Ukraine-Vacations.html'),
        (u'欧洲', u'西班牙', u'http://www.tripadvisor.cn/Tourism-g187427-Spain-Vacations.html'),
        (u'欧洲', u'希腊', u'http://www.tripadvisor.cn/Tourism-g189398-Greece-Vacations.html'),
        (u'欧洲', u'匈牙利', u'http://www.tripadvisor.cn/Tourism-g274881-Hungary-Vacations.html'),
        (u'欧洲', u'意大利', u'http://www.tripadvisor.cn/Tourism-g187768-Italy-Vacations.html'),
        (u'欧洲', u'英国', u'http://www.tripadvisor.cn/Tourism-g186216-United_Kingdom-Vacations.html'),
        (u'美洲', u'阿根廷', u'http://www.tripadvisor.cn/Tourism-g294266-Argentina-Vacations.html'),
        (u'美洲', u'巴拉圭', u'http://www.tripadvisor.cn/Tourism-g294079-Paraguay-Vacations.html'),
        (u'美洲', u'巴拿马', u'http://www.tripadvisor.cn/Tourism-g294479-Panama-Vacations.html'),
        (u'美洲', u'巴西', u'http://www.tripadvisor.cn/Tourism-g294280-Brazil-Vacations.html'),
        (u'美洲', u'秘鲁', u'http://www.tripadvisor.cn/Tourism-g294311-Peru-Vacations.html'),
        (u'美洲', u'玻利维亚', u'http://www.tripadvisor.cn/Tourism-g294071-Bolivia-Vacations.html'),
        (u'美洲', u'伯利兹', u'http://www.tripadvisor.cn/Tourism-g291959-Belize-Vacations.html'),
        (u'美洲', u'厄瓜多尔', u'http://www.tripadvisor.cn/Tourism-g294307-Ecuador-Vacations.html'),
        (u'美洲', u'复活节岛', u'http://www.tripadvisor.cn/Tourism-g316040-Easter_Island-Vacations.html'),
        (u'美洲', u'福克兰群岛', u'http://www.tripadvisor.cn/Tourism-g294270-Falkland_Islands-Vacations.html'),
        (u'美洲', u'格陵兰岛', u'http://www.tripadvisor.cn/Tourism-g295111-Greenland-Vacations.html'),
        (u'美洲', u'哥伦比亚', u'http://www.tripadvisor.cn/Tourism-g294073-Colombia-Vacations.html'),
        (u'美洲', u'哥斯达黎加', u'http://www.tripadvisor.cn/Tourism-g291982-Costa_Rica-Vacations.html'),
        (u'美洲', u'危地马拉', u'http://www.tripadvisor.cn/Tourism-g292002-Guatemala-Vacations.html'),
        (u'美洲', u'圭亚那', u'http://www.tripadvisor.cn/Tourism-g294077-Guyana-Vacations.html'),
        (u'美洲', u'法属圭亚那', u'http://www.tripadvisor.cn/Tourism-g294075-French_Guiana-Vacations.html'),
        (u'美洲', u'洪都拉斯', u'http://www.tripadvisor.cn/Tourism-g292016-Honduras-Vacations.html'),
        (u'美洲', u'加勒比', u'http://www.tripadvisor.cn/Tourism-g147237-Caribbean-Vacations.html'),
        (u'美洲', u'加拿大', u'http://www.tripadvisor.cn/Tourism-g153339-Canada-Vacations.html'),
        (u'美洲', u'马丘比丘', u'http://www.tripadvisor.cn/Tourism-g294318-Machu_Picchu_Sacred_Valley_Cusco_Region-Vacations.html'),
        (u'美洲', u'美国', u'http://www.tripadvisor.cn/Tourism-g191-United_States-Vacations.html'),
        (u'美洲', u'墨西哥', u'http://www.tripadvisor.cn/Tourism-g150768-Mexico-Vacations.html'),
        (u'美洲', u'尼加拉瓜', u'http://www.tripadvisor.cn/Tourism-g294477-Nicaragua-Vacations.html'),
        (u'美洲', u'萨尔瓦多', u'http://www.tripadvisor.cn/Tourism-g294475-El_Salvador-Vacations.html'),
        (u'美洲', u'圣皮埃尔和密克隆', u'http://www.tripadvisor.cn/Tourism-g183815-Saint_Pierre_and_Miquelon-Vacations.html'),
        (u'美洲', u'苏里南', u'http://www.tripadvisor.cn/Tourism-g294081-Suriname-Vacations.html'),
        (u'美洲', u'委内瑞拉', u'http://www.tripadvisor.cn/Tourism-g294324-Venezuela-Vacations.html'),
        (u'美洲', u'乌拉圭', u'http://www.tripadvisor.cn/Tourism-g294064-Uruguay-Vacations.html'),
        (u'美洲', u'智利', u'http://www.tripadvisor.cn/Tourism-g294291-Chile-Vacations.html'),
        (u'大洋洲', u'澳大利亚', u'http://www.tripadvisor.cn/Tourism-g255055-Australia-Vacations.html'),
        (u'大洋洲', u'巴布亚新几内亚', u'http://www.tripadvisor.cn/Tourism-g294115-Papua_New_Guinea-Vacations.html'),
        (u'大洋洲', u'法属波利尼西亚', u'http://www.tripadvisor.cn/Tourism-g294338-French_Polynesia-Vacations.html'),
        (u'大洋洲', u'大堡礁', u'http://www.tripadvisor.cn/Tourism-g255074-Great_Barrier_Reef_Queensland-Vacations.html'),
        (u'大洋洲', u'大溪地', u'http://www.tripadvisor.cn/Tourism-g309679-Tahiti_Society_Islands-Vacations.html'),
        (u'大洋洲', u'斐济', u'http://www.tripadvisor.cn/Tourism-g294331-Fiji-Vacations.html'),
        (u'大洋洲', u'黄金海岸', u'http://www.tripadvisor.cn/Tourism-g255337-Gold_Coast_Queensland-Vacations.html'),
        (u'大洋洲', u'基里巴斯共和国', u'http://www.tripadvisor.cn/Tourism-g294121-Republic_of_Kiribati-Vacations.html'),
        (u'大洋洲', u'库克群岛', u'http://www.tripadvisor.cn/Tourism-g294328-Cook_Islands-Vacations.html'),
        (u'大洋洲', u'维拉港', u'http://www.tripadvisor.cn/Tourism-g294144-Port_Vila_Efate-Vacations.html'),
        (u'大洋洲', u'马里亚那群岛', u'http://www.tripadvisor.cn/Tourism-g1487275-Mariana_Islands-Vacations.html'),
        (u'大洋洲', u'马绍尔群岛', u'http://www.tripadvisor.cn/Tourism-g301392-Marshall_Islands-Vacations.html'),
        (u'大洋洲', u'美属萨摩亚', u'http://www.tripadvisor.cn/Tourism-g60665-American_Samoa-Vacations.html'),
        (u'大洋洲', u'密克罗尼西亚联邦', u'http://www.tripadvisor.cn/Tourism-g294198-Federated_States_of_Micronesia-Vacations.html'),
        (u'大洋洲', u'瑙鲁', u'http://www.tripadvisor.cn/Tourism-g294127-Nauru-Vacations.html'),
        (u'大洋洲', u'纽埃', u'http://www.tripadvisor.cn/Tourism-g294131-Niue-Vacations.html'),
        (u'大洋洲', u'帕劳', u'http://www.tripadvisor.cn/Tourism-g294135-Palau-Vacations.html'),
        (u'大洋洲', u'皮特凯恩群岛', u'http://www.tripadvisor.cn/Tourism-g673774-Pitcairn_Islands-Vacations.html'),
        (u'大洋洲', u'塞班岛', u'http://www.tripadvisor.cn/Tourism-g60716-Saipan_Northern_Mariana_Islands-Vacations.html'),
        (u'大洋洲', u'萨摩亚', u'http://www.tripadvisor.cn/Tourism-g294137-Samoa-Vacations.html'),
        (u'大洋洲', u'所罗门群岛', u'http://www.tripadvisor.cn/Tourism-g294139-Solomon_Islands-Vacations.html'),
        (u'大洋洲', u'汤加', u'http://www.tripadvisor.cn/Tourism-g294141-Tonga-Vacations.html'),
        (u'大洋洲', u'托克劳', u'http://www.tripadvisor.cn/Tourism-g295114-Tokelau-Vacations.html'),
        (u'大洋洲', u'图瓦卢', u'http://www.tripadvisor.cn/Tourism-g294481-Tuvalu-Vacations.html'),
        (u'大洋洲', u'瓦努阿图', u'http://www.tripadvisor.cn/Tourism-g294143-Vanuatu-Vacations.html'),
        (u'大洋洲', u'威克岛', u'http://www.tripadvisor.cn/Tourism-g60667-Wake_Island-Vacations.html'),
        (u'大洋洲', u'瓦利斯和富图纳群岛', u'http://www.tripadvisor.cn/Tourism-g1746897-Wallis_and_Futuna-Vacations.html'),
        (u'大洋洲', u'新喀里多尼亚', u'http://www.tripadvisor.cn/Tourism-g294129-New_Caledonia-Vacations.html'),
        (u'大洋洲', u'新西兰', u'http://www.tripadvisor.cn/Tourism-g255104-New_Zealand-Vacations.html'),
        (u'大洋洲', u'约翰斯顿岛', u'http://www.tripadvisor.cn/Tourism-g60666-Johnston_Atoll-Vacations.html'),
        (u'非洲', u'阿尔及利亚', u'http://www.tripadvisor.cn/Tourism-g293717-Algeria-Vacations.html'),
        (u'非洲', u'埃及', u'http://www.tripadvisor.cn/Tourism-g294200-Egypt-Vacations.html'),
        (u'非洲', u'埃塞俄比亚', u'http://www.tripadvisor.cn/Tourism-g293790-Ethiopia-Vacations.html'),
        (u'非洲', u'安哥拉', u'http://www.tripadvisor.cn/Tourism-g293762-Angola-Vacations.html'),
        (u'非洲', u'贝宁', u'http://www.tripadvisor.cn/Tourism-g293764-Benin-Vacations.html'),
        (u'非洲', u'博茨瓦纳', u'http://www.tripadvisor.cn/Tourism-g293766-Botswana-Vacations.html'),
        (u'非洲', u'布基纳法索', u'http://www.tripadvisor.cn/Tourism-g293768-Burkina_Faso-Vacations.html'),
        (u'非洲', u'布隆迪', u'http://www.tripadvisor.cn/Tourism-g293770-Burundi-Vacations.html'),
        (u'非洲', u'赤道几内亚', u'http://www.tripadvisor.cn/Tourism-g294437-Equatorial_Guinea-Vacations.html'),
        (u'非洲', u'多哥', u'http://www.tripadvisor.cn/Tourism-g293838-Togo-Vacations.html'),
        (u'非洲', u'厄立特里亚', u'http://www.tripadvisor.cn/Tourism-g293788-Eritrea-Vacations.html'),
        (u'非洲', u'佛得角', u'http://www.tripadvisor.cn/Tourism-g293774-Cape_Verde-Vacations.html'),
        (u'非洲', u'冈比亚', u'http://www.tripadvisor.cn/Tourism-g293794-Gambia-Vacations.html'),
        (u'非洲', u'刚果民主共和国', u'http://www.tripadvisor.cn/Tourism-g294186-Democratic_Republic_of_the_Congo-Vacations.html'),
        (u'非洲', u'刚果共和国', u'http://www.tripadvisor.cn/Tourism-g294188-Republic_of_the_Congo-Vacations.html'),
        (u'非洲', u'加纳', u'http://www.tripadvisor.cn/Tourism-g293796-Ghana-Vacations.html'),
        (u'非洲', u'加蓬', u'http://www.tripadvisor.cn/Tourism-g293792-Gabon-Vacations.html'),
        (u'非洲', u'吉布提', u'http://www.tripadvisor.cn/Tourism-g293786-Djibouti-Vacations.html'),
        (u'非洲', u'津巴布韦', u'http://www.tripadvisor.cn/Tourism-g293759-Zimbabwe-Vacations.html'),
        (u'非洲', u'几内亚', u'http://www.tripadvisor.cn/Tourism-g293798-Guinea-Vacations.html'),
        (u'非洲', u'几内亚比绍', u'http://www.tripadvisor.cn/Tourism-g293800-Guinea_Bissau-Vacations.html'),
        (u'非洲', u'喀麦隆', u'http://www.tripadvisor.cn/Tourism-g293772-Cameroon-Vacations.html'),
        (u'非洲', u'科摩罗', u'http://www.tripadvisor.cn/Tourism-g294435-Comoros-Vacations.html'),
        (u'非洲', u'肯尼亚', u'http://www.tripadvisor.cn/Tourism-g294206-Kenya-Vacations.html'),
        (u'非洲', u'科特迪瓦', u'http://www.tripadvisor.cn/Tourism-g294192-Cote_d_Ivoire-Vacations.html'),
        (u'非洲', u'莱索托', u'http://www.tripadvisor.cn/Tourism-g293802-Lesotho-Vacations.html'),
        (u'非洲', u'利比里亚', u'http://www.tripadvisor.cn/Tourism-g293804-Liberia-Vacations.html'),
        (u'非洲', u'利比亚', u'http://www.tripadvisor.cn/Tourism-g293806-Libya-Vacations.html'),
        (u'非洲', u'留尼旺岛', u'http://www.tripadvisor.cn/Tourism-g293826-Reunion_Island-Vacations.html'),
        (u'非洲', u'卢旺达', u'http://www.tripadvisor.cn/Tourism-g293828-Rwanda-Vacations.html'),
        (u'非洲', u'马达加斯加', u'http://www.tripadvisor.cn/Tourism-g293808-Madagascar-Vacations.html'),
        (u'非洲', u'马拉维', u'http://www.tripadvisor.cn/Tourism-g293810-Malawi-Vacations.html'),
        (u'非洲', u'马里', u'http://www.tripadvisor.cn/Tourism-g293812-Mali-Vacations.html'),
        (u'非洲', u'毛里求斯', u'http://www.tripadvisor.cn/Tourism-g293816-Mauritius-Vacations.html'),
        (u'非洲', u'毛里塔尼亚', u'http://www.tripadvisor.cn/Tourism-g293814-Mauritania-Vacations.html'),
        (u'非洲', u'马约特岛', u'http://www.tripadvisor.cn/Tourism-g295116-Mayotte-Vacations.html'),
        (u'中东', u'阿布扎比', u'http://www.tripadvisor.cn/Tourism-g294013-Abu_Dhabi_Emirate_of_Abu_Dhabi-Vacations.html'),
        (u'中东', u'埃拉特', u'http://www.tripadvisor.cn/Tourism-g293980-Eilat_Southern_District-Vacations.html'),
        (u'中东', u'阿勒颇', u'http://www.tripadvisor.cn/Tourism-g295416-Aleppo_Aleppo_Governorate-Vacations.html'),
        (u'中东', u'阿联酋', u'http://www.tripadvisor.cn/Tourism-g294012-United_Arab_Emirates-Vacations.html'),
        (u'中东', u'阿曼', u'http://www.tripadvisor.cn/Tourism-g294006-Oman-Vacations.html'),
        (u'中东', u'安曼', u'http://www.tripadvisor.cn/Tourism-g293986-Amman_Amman_Governorate-Vacations.html'),
        (u'中东', u'巴尔米拉', u'http://www.tripadvisor.cn/Tourism-g297902-Palmyra_Homs_Governorate-Vacations.html'),
        (u'中东', u'巴林', u'http://www.tripadvisor.cn/Tourism-g293996-Bahrain-Vacations.html'),
        (u'中东', u'贝鲁特', u'http://www.tripadvisor.cn/Tourism-g294005-Beirut-Vacations.html'),
        (u'中东', u'大马士革', u'http://www.tripadvisor.cn/Tourism-g294011-Damascus-Vacations.html'),
        (u'中东', u'德黑兰', u'http://www.tripadvisor.cn/Tourism-g293999-Tehran_Tehran_Province-Vacations.html'),
        (u'中东', u'迪拜', u'http://www.tripadvisor.cn/Tourism-g295424-Dubai_Emirate_of_Dubai-Vacations.html'),
        (u'中东', u'多哈', u'http://www.tripadvisor.cn/Tourism-g294009-Doha-Vacations.html'),
        (u'中东', u'吉达', u'http://www.tripadvisor.cn/Tourism-g295419-Jeddah_Makkah_Province-Vacations.html'),
        (u'中东', u'卡塔尔', u'http://www.tripadvisor.cn/Tourism-g294008-Qatar-Vacations.html'),
        (u'中东', u'科威特', u'http://www.tripadvisor.cn/Tourism-g294002-Kuwait-Vacations.html'),
        (u'中东', u'黎巴嫩', u'http://www.tripadvisor.cn/Tourism-g294004-Lebanon-Vacations.html'),
        (u'中东', u'佩特拉', u'http://www.tripadvisor.cn/Tourism-g318895-Petra_Wadi_Musa_Ma_in_Governorate-Vacations.html'),
        (u'中东', u'沙迦', u'http://www.tripadvisor.cn/Tourism-g298064-Sharjah_Emirate_of_Sharjah-Vacations.html'),
        (u'中东', u'沙特阿拉伯', u'http://www.tripadvisor.cn/Tourism-g293991-Saudi_Arabia-Vacations.html'),
        (u'中东', u'叙利亚', u'http://www.tripadvisor.cn/Tourism-g294010-Syria-Vacations.html'),
        (u'中东', u'亚喀巴', u'http://www.tripadvisor.cn/Tourism-g298101-Aqaba_Al_Aqabah_Governorate-Vacations.html'),
        (u'中东', u'利雅德', u'http://www.tripadvisor.cn/Tourism-g293995-Riyadh_Riyadh_Province-Vacations.html'),
        (u'中东', u'耶路撒冷', u'http://www.tripadvisor.cn/Tourism-g293983-Jerusalem_Jerusalem_District-Vacations.html'),
        (u'中东', u'也门', u'http://www.tripadvisor.cn/Tourism-g294014-Yemen-Vacations.html'),
        (u'中东', u'伊拉克', u'http://www.tripadvisor.cn/Tourism-g294000-Iraq-Vacations.html'),
        (u'中东', u'伊朗', u'http://www.tripadvisor.cn/Tourism-g293998-Iran-Vacations.html'),
        (u'中东', u'以色列', u'http://www.tripadvisor.cn/Tourism-g293977-Israel-Vacations.html'),
        (u'中东', u'约旦', u'http://www.tripadvisor.cn/Tourism-g293985-Jordan-Vacations.html'),
    )

    HEADERS = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
        'Cache-Control' : 'max-age=0',
        'Host' : 'www.tripadvisor.cn'
    }

    def start_requests(self):
        for mudidi in self.mudidi_api:
            meta = {}
            meta['main_class'] = mudidi[0]
            meta['second_class'] = mudidi[1]
            meta['url'] = mudidi[2]
            yield Request(mudidi[2], meta=meta, headers=self.HEADERS, dont_filter=True)

    def parse(self, response):
        meta = response.meta
        selector = Selector(response)

        dianping_and_advisor_count = selector.xpath('//div[@class="totalContentCount"]/b/text()').extract_first().replace(',', '')

        try:
            hotel_count = selector.xpath('//li[@class="hotels twoLines"]//span[@class="typeQty"]/text()').extract_first().replace('(', '').replace(')', '')
            hotel_dianping_count = selector.xpath('//li[@class="hotels twoLines"]//span[@class="contentCount"]/text()').extract_first().replace(',', '').replace(u'条点评', '')

            jingdian_count = selector.xpath('//li[@class="attractions twoLines"]//span[@class="typeQty"]/text()').extract_first().replace('(', '').replace(')', '')
            jingdian_dianping_count = selector.xpath('//li[@class="attractions twoLines"]//span[@class="contentCount"]/text()').extract_first().replace(',', '').replace(u'条点评', '')

            restaurants_count = selector.xpath('//li[@class="restaurants twoLines"]//span[@class="typeQty"]/text()').extract_first().replace('(', '').replace(')', '')
            restaurants_dianping_count = selector.xpath('//li[@class="restaurants twoLines"]//span[@class="contentCount"]/text()').extract_first().replace(',', '').replace(u'条点评', '')
        except Exception:
            hotel_count = 0
            hotel_dianping_count = 0

            jingdian_count = 0
            jingdian_dianping_count = 0

            restaurants_count = 0
            restaurants_dianping_count = 0

        #if not hotel_count or not jingdian_count:
        #    self.warn('no hotel count for url : %s' % meta['url'])
        #    return

        result = {
            'main_class' : meta['main_class'],
            'second_class' : meta['second_class'],
            'url' : meta['url'],
            'dianping_and_advisor_count' : dianping_and_advisor_count,
            'hotel_count' : hotel_count,
            'hotel_dianping_count' : hotel_dianping_count,
            'jingdian_count' : jingdian_count,
            'jingdian_dianping_count' : jingdian_dianping_count,
            'restaurants_count' : restaurants_count,
            'restaurants_dianping_count' : restaurants_dianping_count,
            'date' : get_current_date()
        }
        self.logger.info('tripadvisor mudidi : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))



class TripAdvisorYoujiSpider(scrapy.Spider):
    name = 'tripadvisor_youji'

    custom_settings = {
        'DOWNLOAD_DELAY' : 0.3
    }

    youji_api = (
        (u'港澳', u'http://www.tripadvisor.cn/TourismBlog-g294217-Hong_Kong.html'),
        (u'台湾', u'http://www.tripadvisor.cn/TourismBlog-g293910-Taiwan.html'),
        (u'国内', u'http://www.tripadvisor.cn/TourismBlog-g294211-China.html'),
        (u'日本', u'http://www.tripadvisor.cn/TourismBlog-g294232-Japan.html'),
        (u'泰国', u'http://www.tripadvisor.cn/TourismBlog-g293915-Thailand.html'),
        (u'韩国', u'http://www.tripadvisor.cn/TourismBlog-g294196-South_Korea.html'),
        (u'美国', u'http://www.tripadvisor.cn/TourismBlog-g191-United_States.html'),
        (u'马来西亚', u'http://www.tripadvisor.cn/TourismBlog-g293951-Malaysia.html'),
        (u'印度尼西亚', u'http://www.tripadvisor.cn/TourismBlog-g294225-Indonesia.html'),
        (u'法国', u'http://www.tripadvisor.cn/TourismBlog-g187070-France.html'),
        (u'澳大利亚', u'http://www.tripadvisor.cn/TourismBlog-g255055-Australia.html'),
        (u'斯里兰卡', u'http://www.tripadvisor.cn/TourismBlog-g293961-Sri_Lanka.html'),
        (u'菲律宾', u'http://www.tripadvisor.cn/TourismBlog-g294245-Philippines.html'),
        (u'新加坡', u'http://www.tripadvisor.cn/TourismBlog-g294262-Singapore.html'),
        (u'柬埔寨', u'http://www.tripadvisor.cn/TourismBlog-g293939-Cambodia.html'),
        (u'意大利', u'http://www.tripadvisor.cn/TourismBlog-g187768-Italy.html'),
        (u'希腊', u'http://www.tripadvisor.cn/TourismBlog-g189398-Greece.html'),
        (u'新西兰', u'http://www.tripadvisor.cn/TourismBlog-g255104-New_Zealand.html'),
        (u'越南', u'http://www.tripadvisor.cn/TourismBlog-g293921-Vietnam.html'),
        (u'瑞士', u'http://www.tripadvisor.cn/TourismBlog-g188045-Switzerland.html'),
        (u'土耳其', u'http://www.tripadvisor.cn/TourismBlog-g293969-Turkey.html'),
        (u'德国', u'http://www.tripadvisor.cn/TourismBlog-g187275-Germany.html'),
        (u'西班牙', u'http://www.tripadvisor.cn/TourismBlog-g187427-Spain.html'),
        (u'奥地利', u'http://www.tripadvisor.cn/TourismBlog-g190410-Austria.html'),
        (u'英国', u'http://www.tripadvisor.cn/TourismBlog-g186216-United_Kingdom.html'),
        (u'马里亚那群岛', u'http://www.tripadvisor.cn/TourismBlog-g1487275-Mariana_Islands.html'),
        (u'尼泊尔', u'http://www.tripadvisor.cn/TourismBlog-g293889-Nepal.html'),
        (u'马尔代夫', u'http://www.tripadvisor.cn/TourismBlog-g293953-Maldives.html'),
        (u'阿联酋', u'http://www.tripadvisor.cn/TourismBlog-g294012-United_Arab_Emirates.html'),
        (u'毛里求斯', u'http://www.tripadvisor.cn/TourismBlog-g293816-Mauritius.html'),
        (u'印度尼西亚', u'http://www.tripadvisor.cn/TourismBlog-g293860-India.html'),
        (u'缅甸', u'http://www.tripadvisor.cn/TourismBlog-g294190-Myanmar.html'),
        (u'捷克共和国', u'http://www.tripadvisor.cn/TourismBlog-g274684-Czech_Republic.html'),
        (u'加拿大', u'http://www.tripadvisor.cn/TourismBlog-g153339-Canada.html'),
        (u'俄罗斯', u'http://www.tripadvisor.cn/TourismBlog-g294459-Russia.html'),
        (u'挪威', u'http://www.tripadvisor.cn/TourismBlog-g190455-Norway.html'),
        (u'塞舌尔', u'http://www.tripadvisor.cn/TourismBlog-g293738-Seychelles.html'),
        (u'冰岛', u'http://www.tripadvisor.cn/TourismBlog-g189952-Iceland.html'),
        (u'摩纳哥', u'http://www.tripadvisor.cn/TourismBlog-g190405-Monaco.html'),
        (u'瑞典', u'http://www.tripadvisor.cn/TourismBlog-g189806-Sweden.html'),
        (u'丹麦', u'http://www.tripadvisor.cn/TourismBlog-g189512-Denmark.html'),
        (u'斐济', u'http://www.tripadvisor.cn/TourismBlog-g294331-Fiji.html'),
        (u'帕劳', u'http://www.tripadvisor.cn/TourismBlog-g294135-Palau.html'),
        (u'匈牙利', u'http://www.tripadvisor.cn/TourismBlog-g274881-Hungary.html'),
        (u'加勒比', u'http://www.tripadvisor.cn/TourismBlog-g147237-Caribbean.html'),
        (u'荷兰', u'http://www.tripadvisor.cn/TourismBlog-g188553-The_Netherlands.html'),
        (u'葡萄牙', u'http://www.tripadvisor.cn/TourismBlog-g189100-Portugal.html'),
        (u'波兰', u'http://www.tripadvisor.cn/TourismBlog-g274723-Poland.html'),
        (u'埃及', u'http://www.tripadvisor.cn/TourismBlog-g294200-Egypt.html'),
        (u'南非', u'http://www.tripadvisor.cn/TourismBlog-g293740-South_Africa.html'),
        (u'芬兰', u'http://www.tripadvisor.cn/TourismBlog-g189896-Finland.html'),
        (u'墨西哥', u'http://www.tripadvisor.cn/TourismBlog-g150768-Mexico.html'),
        (u'法属波利尼西亚', u'http://www.tripadvisor.cn/TourismBlog-g294338-French_Polynesia.html'),
        (u'比利时', u'http://www.tripadvisor.cn/TourismBlog-g188634-Belgium.html'),
        (u'爱尔兰', u'http://www.tripadvisor.cn/TourismBlog-g186591-Ireland.html'),
        (u'肯尼亚', u'http://www.tripadvisor.cn/TourismBlog-g294206-Kenya.html'),
        (u'约旦', u'http://www.tripadvisor.cn/TourismBlog-g293985-Jordan.html'),
        (u'老挝', u'http://www.tripadvisor.cn/TourismBlog-g293949-Laos.html'),
        (u'以色列', u'http://www.tripadvisor.cn/TourismBlog-g293977-Israel.html'),
        (u'伊朗', u'http://www.tripadvisor.cn/TourismBlog-g293998-Iran.html'),
        (u'文莱达鲁萨兰', u'http://www.tripadvisor.cn/TourismBlog-g293937-Brunei_Darussalam.html'),
        (u'摩洛哥', u'http://www.tripadvisor.cn/TourismBlog-g293730-Morocco.html'),
        (u'卡塔尔', u'http://www.tripadvisor.cn/TourismBlog-g294008-Qatar.html'),
        (u'卢森堡', u'http://www.tripadvisor.cn/TourismBlog-g190340-Luxembourg.html'),
        (u'斯洛伐克', u'http://www.tripadvisor.cn/TourismBlog-g274922-Slovakia.html'),
        (u'瓦努阿图', u'http://www.tripadvisor.cn/TourismBlog-g294143-Vanuatu.html'),
        (u'阿尔及利亚', u'http://www.tripadvisor.cn/TourismBlog-g293717-Algeria.html'),
        (u'坦桑尼亚', u'http://www.tripadvisor.cn/TourismBlog-g293747-Tanzania.html'),
        (u'阿根廷', u'http://www.tripadvisor.cn/TourismBlog-g294266-Argentina.html'),
        (u'埃塞俄比亚', u'http://www.tripadvisor.cn/TourismBlog-g293790-Ethiopia.html'),
        (u'不丹', u'http://www.tripadvisor.cn/TourismBlog-g293844-Bhutan.html'),
        (u'阿塞拜疆', u'http://www.tripadvisor.cn/TourismBlog-g293933-Azerbaijan.html'),
        (u'孟加拉国', u'http://www.tripadvisor.cn/TourismBlog-g293935-Bangladesh.html'),
        (u'亚美尼亚', u'http://www.tripadvisor.cn/TourismBlog-g293931-Armenia.html'),
        (u'朝鲜', u'http://www.tripadvisor.cn/TourismBlog-g294443-North_Korea.html'),
        (u'格鲁吉亚', u'http://www.tripadvisor.cn/TourismBlog-g294194-Georgia.html'),
        (u'保加利亚', u'http://www.tripadvisor.cn/TourismBlog-g294451-Bulgaria.html'),
        (u'尼加拉瓜', u'http://www.tripadvisor.cn/TourismBlog-g294477-Nicaragua.html'),
        (u'巴拿马', u'http://www.tripadvisor.cn/TourismBlog-g294479-Panama.html'),
        (u'萨尔瓦多', u'http://www.tripadvisor.cn/TourismBlog-g294475-El_Salvador.html'),
        (u'马耳他', u'http://www.tripadvisor.cn/TourismBlog-g190311-Malta.html'),
        (u'直布罗陀', u'http://www.tripadvisor.cn/TourismBlog-g187510-Gibraltar.html'),
        (u'突尼斯', u'http://www.tripadvisor.cn/TourismBlog-g293753-Tunisia.html'),
        (u'叙利亚', u'http://www.tripadvisor.cn/TourismBlog-g294010-Syria.html'),
        (u'哥斯达黎加', u'http://www.tripadvisor.cn/TourismBlog-g291982-Costa_Rica.html'),
        (u'巴西', u'http://www.tripadvisor.cn/TourismBlog-g294280-Brazil.html'),
        (u'布基纳法索', u'http://www.tripadvisor.cn/TourismBlog-g293768-Burkina_Faso.html'),
        (u'列支敦士登', u'http://www.tripadvisor.cn/TourismBlog-g190357-Liechtenstein.html'),
        (u'厄立特里亚', u'http://www.tripadvisor.cn/TourismBlog-g293788-Eritrea.html'),
        (u'秘鲁', u'http://www.tripadvisor.cn/TourismBlog-g294311-Peru.html'),
        (u'塞浦路斯', u'http://www.tripadvisor.cn/TourismBlog-g190372-Cyprus.html'),
        (u'厄瓜多尔', u'http://www.tripadvisor.cn/TourismBlog-g294307-Ecuador.html'),
        (u'马里', u'http://www.tripadvisor.cn/TourismBlog-g293812-Mali.html'),
        (u'玻利维亚', u'http://www.tripadvisor.cn/TourismBlog-g294071-Bolivia.html'),
        (u'乌拉圭', u'http://www.tripadvisor.cn/TourismBlog-g294064-Uruguay.html'),
        (u'库克群岛', u'http://www.tripadvisor.cn/TourismBlog-g294328-Cook_Islands.html'),
        (u'South Georgia', u'http://www.tripadvisor.cn/TourismBlog-g1593026-South_Georgia.html'),
    )


    HEADERS = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
        'Cache-Control' : 'max-age=0',
        'Host' : 'www.tripadvisor.cn'
    }

    def start_requests(self):
        for mudidi in self.youji_api:
            meta = {}
            meta['main_class'] = mudidi[0]
            meta['url'] = mudidi[1]
            yield Request(mudidi[1], meta=meta, headers=self.HEADERS, dont_filter=True, callback=self.parse_list)

    def parse_list(self, response):
        meta = response.meta.copy()
        selector = Selector(response)

        for youji in selector.xpath('//ul[@class="stb-item multi-column"]/li/div[@class="stb-detail"]'):
            title = youji.xpath('.//a[@class="title"]/@title').extract_first()
            url = 'http://www.tripadvisor.cn' + youji.xpath('.//a[@class="title"]/@href').extract_first()
            meta['title'] = title
            meta['url'] = url
            yield Request(url, meta=meta, headers=self.HEADERS, dont_filter=True, callback=self.parse_content)

    def parse_content(self, response):
        meta = response.meta
        selector = Selector(response)

        contents = selector.xpath('//div[@class="strategy-content "]/node()').extract()
        content = remove_tags(''.join(contents)).replace('\n', '')
        result = {
            'main_class' : meta['main_class'],
            'title' : meta['title'],
            'url' : meta['url'],
            'content' : content,
            'date' : get_current_date()
        }
        self.logger.info('tripadvisor youji : %s' % json.dumps(result, ensure_ascii=False).encode('utf-8'))

