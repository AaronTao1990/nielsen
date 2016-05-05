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

    def get_tasks(self, queue):
        return self.redis_cli.srandmember(queue)

    def get_proxy(self):
        return self.redis_cli.srandmember(self.REDIS_CONFIG['proxy'])

    def remove_proxy(self, proxy):
        self.redis_cli.srem(self.REDIS_CONFIG['proxy'], proxy)

    def remove_task(self, task, queue):
        self.redis_cli.srem(queue, task)

