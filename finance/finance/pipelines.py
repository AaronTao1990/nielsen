# -*- coding: utf-8 -*-

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from scrapy.conf import settings
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread
from finance.utils.date_util import calculate, get_current_datetime
from finance.utils.mongo_util import MongoUtil
from pykafka import KafkaClient
import hashlib
import logging
import json

logger = logging.getLogger(__name__)

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


def gen_reply_id_from_url(item, pd):
    return hashlib.md5(item.get('threadurl')).hexdigest()

def gen_reply_id_for_wenda(item, pd):
    domain = item.get('domain', '')
    authorname = item.get('authorname', '')
    text = item.get('text', '')
    title = item.get('title', '')
    try:
        if isinstance(domain, basestring):
            domain = domain.encode('utf-8')
        if isinstance(authorname, basestring):
            authorname = authorname.encode('utf-8')
        if isinstance(text, basestring):
            text = text.encode('utf-8')
        if isinstance(title, basestring):
            title = title.encode('utf-8')
        key = "%s%s%s%s%s" % (domain, authorname, pd, text, title)
        return hashlib.md5(key).hexdigest()
    except Exception, e:
        logger.error('failed to gen reply_id for item : %s, exception : %s' % (json.dumps(dict(item), ensure_ascii=False), e))
        return ''

def gen_reply_id_from_content(item, pd):
    domain = item.get('domain', '')
    authorname = item.get('authorname', '')
    text = item.get('text', '')
    try:
        if isinstance(domain, basestring):
            domain = domain.encode('utf-8')
        if isinstance(authorname, basestring):
            authorname = authorname.encode('utf-8')
        if isinstance(text, basestring):
            text = text.encode('utf-8')
        key = "%s%s%s%s" % (domain, authorname, pd, text)
        return hashlib.md5(key).hexdigest()
    except Exception, e:
        logger.error('failed to gen reply_id for item : %s, exception : %s' % (json.dumps(dict(item), ensure_ascii=False), e))
        return ''

def gen_reply_id(item, pd):
    if item.get('tp') in ['3', '5', '6', '8', '9', '10', '11']:
        return gen_reply_id_from_url(item, pd)
    elif item.get('tp') in ['4']:
        return gen_reply_id_for_wenda(item, pd)
    else:
        return gen_reply_id_from_content(item, pd) # 1 2 7

def gen_origin_item(item):
    pm, pw, pk, pd = calculate(item.get('publishdate'))
    replyid = gen_reply_id(item, pd)
    data = {
        'authorurl' : item.get('authorurl', ''),
        'type' : item.get('tp', '2'), # 1 for blog, 2 for bbs, 3 for news, 4 for wenda, 5 for wemedia, 6 for sales, 7 for koubei, 8 for nblog, 9 for daogou, 10 for baike, 11 for pingce
        'floornum' : int(item.get('floornum', 0)),
        'domain' : item.get('domain'),
        'threadurl' : item.get('threadurl'),
        'threadid' : item.get('threadid', ''),
        'replyid' : replyid,
        'text' : item.get('text'),
        'textquote' : item.get('textquote'),
        'textorg' : item.get('textorg'),
        'title' : item.get('title'),
        'crawldate' : item.get('crawldate', ''),
        'sourceurl' : item.get('sourceurl', ''),
        'bankuainame' : item.get('bankuainame', ''),
        'bankuaiid' : str(item.get('bankuaiid', '')),
        'authorname' : item.get('authorname'),
        'device' : item.get('so', ''),
        'publishdate' : item.get('publishdate'),
        'views' : int(item.get('views', 0)),
        'replies' : int(item.get('replies', 0)),
        'likes' : int(item.get('likes', 0)),
        'province' : item.get('province', ''),
        'level' : item.get('level', ''),
        'city' : item.get('city', ''),
        'desc' : item.get('desc', ''),
        'pm' : int(pm), # 发帖日期的当月1号
        'pw' : int(pw), # 发帖日起的周一
        'pk' : int(pk), # 发帖日期为周几
        'pd' : int(pd), # 发帖日期
        'meta' : item.get('meta')
    }
    return data


class ReplyItemKafkaOriginPipeline(object):

    def __init__(self):
        kafka_info = settings.get('KAFKA_INFO')
        self.kafka_client = KafkaClient(hosts=kafka_info['broker'])
        self.reply_topic = self.kafka_client.topics[kafka_info['replyorigintopic']]
        self.reply_producer = self.reply_topic.get_producer()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        self.domains_to_change_floornum = set()
        self.load_domains_to_change_floornum()

    def load_domains_to_change_floornum(self):
        with open('config/domains_to_change_floornum.conf', 'r') as f:
            for line in f.readlines():
                self.domains_to_change_floornum.add(line.strip('\n'))

    def spider_closed(self, spider):
        logger.info('stopping producer for reply item')
        self.reply_producer.stop()

    def process_floornum(self, item):
        if item.get('domain') in self.domains_to_change_floornum and int(item.get('floornum', 0)) == 1:
            item['floornum'] = 0

    def process_item(self, item, spider):
        self.process_floornum(item)
        data = gen_origin_item(item)
        #logger.info('reply item : %s' % json.dumps(data, ensure_ascii=False, indent=2))
        message = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.reply_producer.produce(message)

        return item


class ReplyItemMongoOriginPipeline(object):

    def __init__(self):
        self.encoder = ScrapyJSONEncoder()
        mongo_conf = settings.get('MONGO_CONF')
        self.mongo_client = MongoUtil(
            mongo_conf['host_backup'],
            mongo_conf['db'],
            mongo_conf['coll']['reply']
        )

    def process_item(self, item, spider):
        data = gen_origin_item(item)
        #logger.info('reply item : %s' % json.dumps(data, ensure_ascii=False))
        self.mongo_client.save(data)
        return item
