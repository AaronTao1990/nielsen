# -*-coding:utf-8-*-
from scrapy.conf import settings
import redis
import logging

class KeywordsDao(object):

    def __init__(self, timeout=2):
        self.timeout = timeout
        self.REDIS_CONFIG = settings.get('REDIS_CONFIG')
        self.redis_cli = redis.Redis(host=self.REDIS_CONFIG['host'], port=self.REDIS_CONFIG['port'])
        logging.info('redis host : %s' % self.REDIS_CONFIG['host'])
        logging.info('redis queue: %s' % self.REDIS_CONFIG['ntasks'])

    def get_tasks(self):
        return self.redis_cli.srandmember(self.REDIS_CONFIG['ntasks'])

    def remove_task(self, task):
        self.redis_cli.srem(self.REDIS_CONFIG['ntasks'], task)

